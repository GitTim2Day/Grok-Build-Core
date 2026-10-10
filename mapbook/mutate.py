import subprocess, filecmp, sys
FILES=('addresses.txt','roads.txt','road_nodes.txt')
FAULTS=['faults/%s.pbf'%n for n in ('empty','noheader','rawsize','truncated','lzma','feature','hdr_zero','hdr_huge')]
def check(cmd_base):
    r=subprocess.run(cmd_base+['osm_fixture.pbf','mut/out'],capture_output=True,text=True)
    if r.returncode!=0: return True
    for f in FILES:
        if not filecmp.cmp('mut/out/'+f,'osm_fixture_expected/'+f,shallow=False): return True
    cnt='\n'.join(l for l in r.stdout.splitlines() if l.startswith(('blocks=','kept_','missing_')))+'\n'
    if cnt!=open('osm_fixture_expected/summary_counts.txt').read(): return True
    for fp in FAULTS:
        if subprocess.run(cmd_base+[fp,'mut/o2'],capture_output=True).returncode==0: return True
    return False
def run(lang, src_path, muts):
    src=open(src_path).read(); k=0
    for a,b,name in muts:
        assert a in src,(lang,name)
        m=src.replace(a,b,1)
        if lang=='py':
            open('mut/m.py','w').write(m); cmd=['python3','-I','mut/m.py']
        else:
            open('mut/m.cpp','w').write(m)
            if subprocess.run(['g++','-std=c++17','-O1','mut/m.cpp','-lz','-o','mut/m'],capture_output=True).returncode: print('NOCOMPILE',name); continue
            cmd=['mut/m']
        d=check(cmd); k+=d; print(lang,'KILLED ' if d else 'SURVIVED ',name)
    print('%s mutants killed %d/%d'%(lang,k,len(muts)))
PY=[('frac[:7]','frac[:8]','chop width'),('letter = pos_letter               # no negative zero','pass','negative zero'),
('"motorway trunk primary','"motorway trunk','roadset'),('a[9] = "MISSINGREF"','a[9] = "FIRSTREF"','missingref'),
('lato + gran * lat,','gran * lat,','lat offset'),('lono + gran * lon,','gran * lon,','lon offset'),
('if k == 0:\n                            break','if k == 0 and False:\n                            break','dense terminator'),
('acc += unzz(v)','acc = unzz(v)','delta decode'),('for nid in sorted(road_ids):','for nid in road_ids:','sort road nodes'),
('if "addr:housenumber" in tags:\n                    a = addr_fields','if "addr:street" in tags:\n                    a = addr_fields','addr trigger'),
('if stats["blocks"] == 1 and kind != "OSMHeader":','if False:','header first'),('if len(data) != rsize:','if False:','rawsize'),
('mag // 1000000000','mag // 100000000','whole degrees'),('raise Refuse("empty input file")','pass','empty file'),
('stats["relations"] += count_relations(g)','pass','relation count'),('first = refs[0] if refs else 0','first = refs[-1] if refs else 0','first ref')]
CPP=[('frac[7] = 0;','frac[8] = 0;','chop width'),('letter = pos;  // no negative zero','(void)0;','negative zero'),
('"motorway","trunk","primary",','"motorway","trunk",','roadset'),('else a.pos = "MISSINGREF";','else a.pos = "FIRSTREF";','missingref'),
('fn(id, B.lato + B.gran * la,','fn(id, B.gran * la,','lat offset'),('B.lono + B.gran * lo, t);','B.gran * lo, t);','lon offset'),
('if (k == 0) break;','if (k == 0 && false) break;','dense terminator'),('acc += unzz(v);','acc = unzz(v);','delta decode'),
('std::sort(rid.begin(), rid.end());','','sort road nodes'),
('if (blocks == 1 && R.kind != "OSMHeader")','if (false)','header first'),
('if ((int64_t)data.size() != rsize) { refuse("raw_size mismatch"); return -1; }','','rawsize'),
('mag / 1000000000ULL','mag / 100000000ULL','whole degrees'),('if (blocks == 0) { g_err = "empty input file"; return fail(); }','','empty file'),
('if (x.no == 4 && x.wt == 2) ++rels;','','relation count'),('a.first = refs.empty() ? 0 : refs[0];','a.first = refs.empty() ? 0 : refs.back();','first ref')]
run('py','osm_streamline.py',PY); run('cpp','osm_streamline.cpp',CPP)
