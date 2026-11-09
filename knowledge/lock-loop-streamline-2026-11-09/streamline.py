# Streamline lock-loop-bundle/v1 -> exact ratios, direction for negatives, offset frame. Read-only on inputs.
import numpy as np, json, hashlib, struct
from fractions import Fraction as F
SRC='/workspace/lock-loop-xfer-2026-11-09/extracted/'
OUT='/workspace/lock-loop-xfer-2026-11-09/streamlined/'
a=np.load(SRC+'arrays.npz'); m=json.load(open(SRC+'manifest.json'))
OFFSET=F(1,4)                       # unit-ratio ladder: d=floor(1/0.20067...)=4 -> 1/4 > most negative magnitude
C=F(299792458); TP=F(539,10**46); LP=C*TP   # Planck-floor marker L_p = c*t_p (exact ratio)
SIG=15
def trunc(fr,sig=SIG):
    # truncated (toward zero) decimal rendering of a positive ratio, sig significant digits, integer math only
    assert fr>0
    n,d=fr.numerator,fr.denominator
    e=len(str(n//d))-1 if n>=d else -(len(str(d//n)) if d%n else len(str(d//n))-1)
    # find e with 10^e <= fr < 10^(e+1)
    while F(10)**e>fr: e-=1
    while F(10)**(e+1)<=fr: e+=1
    k=SIG-1-e
    q=(n*10**k)//d if k>=0 else n//(d*10**(-k))
    s=str(q); 
    return f'{s[0]}.{s[1:]}e{e:+d}'
def rs(fr): return f'{fr.numerator}/{fr.denominator}'
zeros=[]; nonfinite=0
def ex(x,tag):
    global nonfinite
    if not np.isfinite(x): nonfinite+=1; raise SystemExit('nonfinite '+tag)
    f=F(float(x))
    if f==0: zeros.append(tag); return None
    return f
def dirform(f,tag):
    if f is None: return {'mag':rs(LP),'mag_trunc15':trunc(LP),'dir':1,'note':'exact zero -> L_p floor marker'}
    return {'mag':rs(abs(f)),'mag_trunc15':trunc(abs(f)),'dir':(-1 if f<0 else 1)}
TH=F(m['knobs']['lock_rms_thresh']); TH_DEC=F('0.08')
frames=[]; rt={'pass':0,'fail':0}; lockmm=[]; subs_exact=0; subs_inexact=0; rms_rows=[]
for fr in m['frames']:
    i=fr['frame']; t=f'{i:02d}'
    y,yh,r=a['y_'+t],a['yhat_'+t],a['resid_'+t]
    for nm,arr in (('y',y),('yhat',yh),('resid',r)):
        assert hashlib.sha256(arr.astype('<f8').tobytes()).hexdigest()==fr[nm]['sha256'], (t,nm)
    S=[]; sumsq=F(0)  # accumulator start is the empty sum (count position), not a stored value
    for j in range(len(y)):
        fy,fh,fres=ex(y[j],f'y_{t}[{j}]'),ex(yh[j],f'yhat_{t}[{j}]'),ex(r[j],f'resid_{t}[{j}]')
        ys,hs=fy+OFFSET,fh+OFFSET
        assert ys>0 and hs>0
        rd=dirform(fres,'r')
        S.append({'j':j,'y_shift':rs(ys),'y_shift_trunc15':trunc(ys),'yhat_shift':rs(hs),'yhat_shift_trunc15':trunc(hs),'resid':rd})
        sumsq+=fres*fres
        if fy-fh==fres: subs_exact+=1
        else: subs_inexact+=1
        # round-trip: rebuild float64 from stored outputs only
        Ry=F(S[-1]['y_shift'])+(OFFSET*-1); Rh=F(S[-1]['yhat_shift'])+(OFFSET*-1)
        Rr=F(rd['mag'])*rd['dir']
        for R,orig in ((Ry,y[j]),(Rh,yh[j]),(Rr,r[j])):
            back=float(R)
            if F(back)==R and struct.pack('<d',back)==struct.pack('<d',orig): rt['pass']+=1
            else: rt['fail']+=1
    ms=sumsq/len(y)
    lk_bin=ms<TH*TH; lk_dec=ms<TH_DEC*TH_DEC
    if lk_bin!=fr['locked'] or lk_dec!=fr['locked']: lockmm.append(i)
    rmsF=F(fr['rms']); drift=rmsF*rmsF+(ms*-1)
    rms_rows.append((i,ms,rmsF,drift))
    coef=[dirform(ex(c,f'coef_{t}[{k}]'),'c') for k,c in enumerate(fr['coef'])]
    sc={}
    for k in ('rms','margin','peak_hz','peak_amp'):
        f=ex(fr[k],f'{k}_{t}'); sc[k]=dirform(f,k)
    frames.append({'schema':'lock-loop-streamlined/v1','source_schema':m['schema'],'frame':i,'offset':rs(OFFSET),
      'recover':'y = y_shift + (offset x -1); yhat = yhat_shift + (offset x -1); resid = mag x dir',
      'locked_manifest':fr['locked'],'locked_exact':lk_bin,'mean_sq_resid':rs(ms),'mean_sq_resid_trunc15':trunc(ms),
      'thresh_sq':rs(TH*TH),'order':fr['order'],'coef':coef,'scalars':sc,
      'n':len(S),'min_y_shift_trunc15':trunc(min(F(s['y_shift']) for s in S)),
      'neg_resid':sum(1 for s in S if s['resid']['dir']==-1),'samples':S})
with open(OUT+'lock_loop_streamlined.jsonl','w') as fo:
    for f in frames: fo.write(json.dumps(f,separators=(',',':'))+'\n')
json.dump({'rt':rt,'lockmm':lockmm,'zeros':zeros,'nonfinite':nonfinite,'subs_exact':subs_exact,'subs_inexact':subs_inexact,
  'rms':[(i,trunc(ms),trunc(rf),('+' if d>0 else '-' if d<0 else '='), trunc(abs(d)) if d else 'equal') for i,ms,rf,d in rms_rows],
  'minshift':min(f['min_y_shift_trunc15'] for f in frames),'TH_sq':rs(TH*TH),'TH_bin':rs(TH)},open('/tmp/ll_stats.json','w'),indent=1)
# summary + ODS
import pandas as pd
rows=[]
for f in frames:
    rows.append({'frame':f['frame'],'locked_manifest':str(f['locked_manifest']),'locked_exact':str(f['locked_exact']),
      'mean_sq_resid_trunc15':f['mean_sq_resid_trunc15'],'rms_trunc15':f['scalars']['rms']['mag_trunc15'],
      'peak_hz_trunc15':f['scalars']['peak_hz']['mag_trunc15'],'neg_resid_count':f['neg_resid'],'min_y_shift_trunc15':f['min_y_shift_trunc15'],
      'coef_dirs':' '.join(str(c['dir']) for c in f['coef'])})
smp=[]
for f in frames:
    for s in f['samples']:
        smp.append({'frame':f['frame'],'j':s['j'],'y_shift':s['y_shift'],'y_shift_trunc15':s['y_shift_trunc15'],'yhat_shift':s['yhat_shift'],
          'yhat_shift_trunc15':s['yhat_shift_trunc15'],'resid_mag':s['resid']['mag'],'resid_mag_trunc15':s['resid']['mag_trunc15'],'resid_dir':str(s['resid']['dir'])})
with pd.ExcelWriter(OUT+'lock_loop_streamlined.ods',engine='odf') as w:
    pd.DataFrame(rows).astype(str).to_excel(w,sheet_name='frames',index=False)
    pd.DataFrame(smp).astype(str).to_excel(w,sheet_name='samples',index=False)
    pd.DataFrame([{'key':'offset','value':rs(OFFSET)},{'key':'L_p_floor_marker','value':rs(LP)},{'key':'thresh_sq_binary','value':rs(TH*TH)},
      {'key':'recover','value':frames[0]['recover']}]).to_excel(w,sheet_name='keys',index=False)
with open(OUT+'lock_loop_summary.txt','w') as fo:
    fo.write('LOCK LOOP STREAMLINED SUMMARY  (lock-loop-bundle/v1 synthetic, seed 7)\n')
    fo.write(f'Offset (exact): {rs(OFFSET)}   y = y_shift + ({rs(OFFSET)} x -1)\n')
    fo.write(f'Decimals: truncated toward zero, {SIG} significant digits (renderings only; ratios are the values)\n\n')
    fo.write('frame locked(manifest) locked(exact) mean_sq_resid_trunc15 rms_trunc15 peak_hz neg_resid min_y_shift_trunc15\n')
    for r_ in rows:
        fo.write(f"{r_['frame']:>5} {r_['locked_manifest']:>16} {r_['locked_exact']:>13} {r_['mean_sq_resid_trunc15']:>22} {r_['rms_trunc15']:>21} {r_['peak_hz_trunc15']:>21} {r_['neg_resid_count']:>9} {r_['min_y_shift_trunc15']}\n")
    fo.write(f"\nRound-trip float64 bit-exact: pass {rt['pass']} fail {rt['fail']}\n")
    fo.write(f"Lock recheck mismatches: {lockmm if lockmm else 'none found'}\n")
    fo.write(f"Exact zeros: {zeros if zeros else 'none found'}; non-finite: {'none found' if not nonfinite else nonfinite}\n")
print(rt,lockmm,zeros,subs_exact,subs_inexact)
