#!/usr/bin/env python3
"""KBLD9 validation candidate R3. Additive extension; does not modify sealed GitHub source.
Exact MAD, explicit rejected observations, directional units, LF canonical framing,
process-locked single-event supersession, chain verification. POSIX flock required.
"""
from __future__ import annotations
import hashlib, json, math, os, fcntl, tempfile, threading, random
from contextlib import contextmanager
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

class ValidationError(ValueError): pass
class IntegrityError(ValidationError): pass
SCALE=Fraction(7413,5000) # exact representation of the declared 1.4826 factor, not probabilistic sigma

def number(x):
    if isinstance(x,bool): raise ValidationError('boolean numeric input')
    if isinstance(x,Fraction): return x
    if isinstance(x,int): return Fraction(x)
    if isinstance(x,str):
        try:
            if not x.strip() or len(x)>10000: raise ValueError()
            return Fraction(x)
        except (ValueError,ZeroDivisionError,OverflowError) as e: raise ValidationError('invalid numeric text') from e
    # Floats are prohibited at the precise entry door: a float may already be rounded.
    raise ValidationError('numeric input must be integer, decimal string, or fraction')

def add_units(base,magnitude,direction,unit,base_unit):
    if not isinstance(unit,str) or not unit or unit!=base_unit: raise ValidationError('unit mismatch')
    if type(direction) is not int or direction not in (-1,1): raise ValidationError('invalid direction')
    m=number(magnitude)
    if m<0: raise ValidationError('negative magnitude')
    return number(base)+m*direction

def truncate(v,places):
    if type(places) is not int or not 0<=places<=1000: raise ValidationError('invalid precision')
    x=number(v); factor=10**places; k=abs(x.numerator)*factor//x.denominator
    sign='-' if x<0 and k else ''
    if places==0:return sign+str(k)
    a,b=divmod(k,factor); return f'{sign}{a}.{b:0{places}d}'

def ratio(x):
    f=number(x);return f'{f.numerator}/{f.denominator}'

def median(seq):
    a=sorted(seq); n=len(a)
    if not n:raise ValidationError('empty median')
    return a[n//2] if n%2 else (a[n//2-1]+a[n//2])/2

def mad_guard(values,multiplier='10',zero_mad='flag_different'):
    if not isinstance(values,(list,tuple)):raise ValidationError('sequence required')
    n=number(multiplier)
    if n<=0:raise ValidationError('positive multiplier required')
    if zero_mad not in ('flag_different','keep_all'):raise ValidationError('zero MAD policy')
    good=[]; rejected=[]
    for i,x in enumerate(values):
        try: good.append((i,number(x)))
        except ValidationError as e:rejected.append({'index':i,'reason':str(e),'raw_type':type(x).__name__,'raw_repr':repr(x)})
    if not good:return {'kept':[],'flagged':[],'rejected':rejected,'median':None,'mad':None,'threshold':None}
    med=median([v for _,v in good]); mad=median([abs(v-med) for _,v in good]); threshold=n*SCALE*mad
    kept=[];flagged=[]
    for i,v in good:
        flag=(abs(v-med)>threshold) if mad else (zero_mad=='flag_different' and v!=med)
        (flagged if flag else kept).append({'index':i,'value':ratio(v)})
    if len(kept)+len(flagged)+len(rejected)!=len(values):raise IntegrityError('count conservation')
    return {'kept':kept,'flagged':flagged,'rejected':rejected,'median':ratio(med),'mad':ratio(mad),'threshold':ratio(threshold),'scale':'7413/5000','sigma_probability_claim':False}

def _validate_json(x,seen=None,depth=0):
    if depth>100:raise ValidationError('JSON nesting limit')
    if x is None or type(x) in (bool,int,str):
        if type(x) is str:x.encode('utf-8','strict')
        return
    if type(x) is float:raise ValidationError('floats prohibited in canonical ledger')
    if type(x) not in (list,dict):raise ValidationError('unsupported JSON type')
    seen=set() if seen is None else seen
    if id(x) in seen:raise ValidationError('cyclic JSON')
    seen.add(id(x))
    if type(x) is dict:
        for k,v in x.items():
            if type(k) is not str:raise ValidationError('nonstring key')
            k.encode('utf-8','strict');_validate_json(v,seen,depth+1)
    else:
        for v in x:_validate_json(v,seen,depth+1)
    seen.remove(id(x))

def canonical(x):
    try:
        _validate_json(x)
        return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8','strict')
    except (UnicodeError,RecursionError,OverflowError) as e:raise ValidationError('invalid JSON encoding') from e

def digest(x):return hashlib.sha256(canonical(x)).hexdigest()

def utc():return datetime.now(timezone.utc).isoformat()

class Ledger:
    def __init__(self,path):self.path=Path(path);self.lockpath=Path(str(path)+'.lock')
    @contextmanager
    def locked(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(self.lockpath,os.O_CREAT|os.O_RDWR,0o600)
        try:
            fcntl.flock(fd,fcntl.LOCK_EX)
            yield
        finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
    def _read(self):
        if not self.path.exists():return []
        raw=self.path.read_bytes()
        if raw and not raw.endswith(b'\n'):raise IntegrityError('unterminated tail')
        if b'\r' in raw:raise IntegrityError('CR or CRLF framing not canonical')
        rows=[];prev=None
        for line in raw.split(b'\n')[:-1]:
            try:
                obj=json.loads(line,parse_float=lambda _: (_ for _ in ()).throw(ValidationError('float JSON')),
                               parse_constant=lambda _: (_ for _ in ()).throw(ValidationError('nonfinite JSON')),
                               object_pairs_hook=_unique_keys)
                if canonical(obj)!=line:raise IntegrityError('noncanonical JSONL')
                h=obj['hash'];body={k:v for k,v in obj.items() if k!='hash'}
                if digest(body)!=h or body['previous_hash']!=prev or body['sequence']!=len(rows)+1:raise IntegrityError('chain mismatch')
                rows.append(obj);prev=h
            except (ValueError,TypeError,KeyError,UnicodeError) as e:raise IntegrityError('invalid ledger record') from e
        return rows
    def read(self):
        with self.locked():return self._read()
    def _append(self,kind,payload):
        canonical(payload) # preflight before opening file
        rows=self._read()
        obj={'schema':'kbld9-validation-r3','kind':kind,'payload':payload,'time':utc(),
             'previous_hash':rows[-1]['hash'] if rows else None,'sequence':len(rows)+1}
        obj['hash']=digest(obj);line=canonical(obj)+b'\n'
        fd=os.open(self.path,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
        try:
            written=os.write(fd,line)
            if written!=len(line):raise IntegrityError('short append: manual recovery required')
            os.fsync(fd)
        finally:os.close(fd)
        if self._read()[-1]!=obj:raise IntegrityError('readback mismatch')
        return obj
    def append_active(self,record_id,value):
        with self.locked():
            if not isinstance(record_id,str) or not record_id:raise ValidationError('record ID')
            if record_id in self._all_ids(self._read()):raise ValidationError('duplicate ID')
            return self._append('ACTIVE',{'record_id':record_id,'value':value})
    @staticmethod
    def _all_ids(rows):
        return ({r['payload']['record_id'] for r in rows if r['kind']=='ACTIVE'} | {r['payload']['new_id'] for r in rows if r['kind']=='SUPERSEDE'})
    def supersede(self,old_id,new_id,value):
        # Single append event: no notice/replacement gap, even on crash.
        with self.locked():
            rows=self._read(); view=self._view(rows)
            if not isinstance(old_id,str) or not isinstance(new_id,str) or not old_id or not new_id or old_id==new_id:raise ValidationError('IDs')
            if old_id not in view or new_id in self._all_ids(rows):raise ValidationError('missing active old or duplicate new')
            return self._append('SUPERSEDE',{'old_id':old_id,'new_id':new_id,'value':value})
    @staticmethod
    def _view(rows):
        active={}; all_ids=set()
        for r in rows:
            p=r['payload'];k=r['kind']
            if k=='ACTIVE':
                rid=p['record_id']
                if rid in all_ids:raise IntegrityError('duplicate ID')
                all_ids.add(rid);active[rid]=p['value']
            elif k=='SUPERSEDE':
                old,new=p['old_id'],p['new_id']
                if old not in active or new in all_ids or old==new:raise IntegrityError('invalid supersession')
                del active[old];all_ids.add(new);active[new]=p['value']
            elif k=='QUARANTINE':pass
            else:raise IntegrityError('unknown event')
        return active
    def view(self):
        with self.locked():return self._view(self._read())
    def quarantine(self,reason,original):
        with self.locked():return self._append('QUARANTINE',{'reason':reason,'original':original})

def _unique_keys(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise IntegrityError('duplicate JSON key')
        d[k]=v
    return d

def normalize_transport_jsonl(raw):
    """Opt-in CRLF -> LF at ingestion boundary only. Never normalize a sealed ledger.
    Refuse bare CR and unterminated tail; returns canonical LF bytes plus counts.
    """
    if not isinstance(raw,bytes):raise ValidationError('bytes required')
    if raw and not raw.endswith(b'\n'):raise ValidationError('unterminated transport input')
    crlf=raw.count(b'\r\n')
    normalized=raw.replace(b'\r\n',b'\n')
    if b'\r' in normalized:raise ValidationError('bare CR')
    for line in normalized.split(b'\n')[:-1]:
        try:json.loads(line,object_pairs_hook=_unique_keys,parse_constant=lambda _: (_ for _ in ()).throw(ValidationError('nonfinite')))
        except (ValueError,UnicodeError) as e:raise ValidationError('malformed input line') from e
    return normalized,{'crlf_converted':crlf,'original_sha256':hashlib.sha256(raw).hexdigest(),'normalized_sha256':hashlib.sha256(normalized).hexdigest()}

def selftest():
    tests=0
    def check(cond,label):
        nonlocal tests
        if not cond:raise AssertionError(label)
        tests+=1
    def reject(fn,kind=ValidationError):
        try:fn()
        except kind:return True
        return False
    check(number('1/3')*3==1,'fraction');check(reject(lambda:number(0.1)),'reject float')
    check(add_units('10','3/7',-1,'m','m')==Fraction(67,7),'direction')
    check(reject(lambda:add_units(1,2,1,'m','s')),'units')
    check(truncate('1/3',6)=='0.333333','truncation')
    check(truncate('-1/3',6)=='-0.333333','signed truncation')
    check(len(mad_guard(['10','10','10','1000000000000000000000'])['flagged'])==1,'outlier')
    check(mad_guard(['1','bad','2'])['rejected'][0]['index']==1,'quarantine index')
    check(mad_guard(['1','2','3'])['median']=='2/1','median')
    check(mad_guard(['1','1','1','2'])['mad']=='0/1','zero MAD')
    check(reject(lambda:canonical({'x':float('nan')})),'nonfinite')
    check(reject(lambda:canonical({'x':'\ud800'})),'surrogate')
    a=[];a.append(a);check(reject(lambda:canonical(a)),'cycle')
    raw=b'{"x":1}\r\n{"x":2}\r\n';norm,info=normalize_transport_jsonl(raw)
    check(norm==b'{"x":1}\n{"x":2}\n' and info['crlf_converted']==2,'CRLF')
    check(reject(lambda:normalize_transport_jsonl(b'{"x":1}\r{"x":2}\n')),'bare CR')
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'j.jsonl';j=Ledger(p);j.append_active('a','1/3');before=p.read_bytes()
        j.supersede('a','b','2/3');check(j.view()=={'b':'2/3'},'supersede')
        check(p.read_bytes().startswith(before),'prefix')
        check(len(j.read())==2,'single event')
        check(reject(lambda:j.supersede('a','c','3'),ValidationError),'stale old')
        check(reject(lambda:j.append_active('a','3'),ValidationError),'duplicate historic')
        check(reject(lambda:j.append_active('b','3'),ValidationError),'duplicate supersession ID')
        check(reject(lambda:j.supersede('b','c',float('nan')),ValidationError),'preflight')
        check(len(j.read())==2,'failed transaction unchanged')
        bad=Path(td)/'bad.jsonl';bad.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
        check(reject(lambda:Ledger(bad).read(),IntegrityError),'ledger CRLF')
        bad.write_bytes(p.read_bytes()+b'{');check(reject(lambda:Ledger(bad).read(),IntegrityError),'torn tail')
        # 8 threads, locked transactions, no fork / loss.
        j2=Ledger(Path(td)/'concurrent.jsonl');errs=[]
        def worker(i):
            try:
                for n in range(25):j2.append_active(f'{i}-{n}',str(n))
            except Exception as e:errs.append(repr(e))
        threads=[threading.Thread(target=worker,args=(i,)) for i in range(8)]
        for t in threads:t.start()
        for t in threads:t.join()
        check(not errs and len(j2.read())==200,'concurrent chain '+repr(errs))
        check(len(j2.view())==200,'concurrent view')
    rng=random.Random(20261007)
    for i in range(10000):
        a=Fraction(rng.randrange(-10**8,10**8),rng.randrange(1,10000));m=Fraction(rng.randrange(0,10**8),rng.randrange(1,10000))
        plus=add_units(a,m,1,'m','m');minus=add_units(a,m,-1,'m','m')
        if plus-a!=a-minus:raise AssertionError('directional symmetry')
    check(True,'10k symmetry')
    print(f'PASS {tests}/{tests} deterministic groups; 10000 directional property cases; 200 concurrent append records')

if __name__=='__main__':selftest()
