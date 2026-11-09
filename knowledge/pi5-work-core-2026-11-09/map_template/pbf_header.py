import struct,zlib,sys,json
def varint(b,i):
    r=0;s=0
    while True:
        c=b[i];i+=1;r|=(c&0x7f)<<s;s+=7
        if c<0x80: return r,i
def fields(b):
    i=0;out=[]
    while i<len(b):
        k,i=varint(b,i);f,w=k>>3,k&7
        if w==0: v,i=varint(b,i)
        elif w==2:
            n,i=varint(b,i);v=b[i:i+n];i+=n
        elif w==1: v=b[i:i+8];i+=8
        elif w==5: v=b[i:i+4];i+=4
        out.append((f,w,v))
    return out
zz=lambda n:(n>>1)^-(n&1)
def nd(n):  # nanodegrees exact decimal string, no floats
    s='-' if n<0 else '';n=abs(n);return '%s%d.%09d'%(s,n//10**9,n%10**9)
p=sys.argv[1];fh=open(p,'rb')
hl=struct.unpack('>I',fh.read(4))[0];bh=dict((f,v) for f,w,v in fields(fh.read(hl)))
blob=dict((f,v) for f,w,v in fields(fh.read(bh[3])))
data=zlib.decompress(blob[3]) if 3 in blob else blob[1]
h={'blob_type':bh[1].decode(),'blobheader_bytes':hl,'blob_datasize':bh[3]}
req=[];opt=[]
for f,w,v in fields(data):
    if f==1:
        bb=dict((g,zz(x)) for g,_,x in fields(v))
        h['bbox_nanodeg']={'left':bb[1],'right':bb[2],'top':bb[3],'bottom':bb[4]}
        h['bbox_deg']={k:nd(bb[j]) for k,j in (('left',1),('right',2),('top',3),('bottom',4))}
    elif f==4: req.append(v.decode())
    elif f==5: opt.append(v.decode())
    elif f==16: h['writingprogram']=v.decode()
    elif f==17: h['source']=v.decode()
    elif f==32: h['osmosis_replication_timestamp']=v
    elif f==33: h['osmosis_replication_sequence_number']=v
    elif f==34: h['osmosis_replication_base_url']=v.decode()
h['required_features']=req;h['optional_features']=opt
if 'osmosis_replication_timestamp' in h:
    import datetime;h['replication_timestamp_utc']=datetime.datetime.fromtimestamp(h['osmosis_replication_timestamp'],datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print(json.dumps(h,indent=1))
