// rt345_check.cpp - independent C++17 build of the same checks.
// Exact integer rationals (num/den, den>0, reduced). No float.
#include <cstdio>
#include <numeric>
#include <cstdlib>
struct Q { long long n, d; };
static Q mk(long long n, long long d){ if(d<0){n=-n;d=-d;} long long g=std::gcd(std::llabs(n),d); if(!g)g=1; return {n/g,d/g}; }
static Q mul(Q a,Q b){ return mk(a.n*b.n,a.d*b.d); }
static Q add(Q a,Q b){ return mk(a.n*b.d+b.n*a.d,a.d*b.d); }
static Q sub(Q a,Q b){ return mk(a.n*b.d-b.n*a.d,a.d*b.d); }
static Q dv(Q a,Q b){ return mk(a.n*b.d,a.d*b.n); }
static bool eq(Q a,Q b){ return a.n==b.n && a.d==b.d; }
static Q I(long long n){ return {n,1}; }
static int R(char s){ return s=='h'?3:s=='b'?4:5; }
static bool root(Q h,Q b,Q H){ return eq(add(mul(h,h),mul(b,b)),mul(H,H)); }

static int fails=0, total=0;
static void report(const char* nm,bool ok){ total++; if(!ok)fails++; std::printf("%s %s\n",ok?"PASS":"FAIL",nm); }

int main(){
  struct C{char s; Q v; Q want;} cs[]={{'h',I(3),I(1)},{'h',I(15),I(5)},{'H',I(25),I(5)},{'b',I(8),I(2)},
    {'H',I(5),I(1)},{'H',I(10),I(2)},{'H',I(7),mk(7,5)},{'h',mk(21,5),mk(7,5)},{'b',mk(28,5),mk(7,5)}};
  bool ok=true;
  for(auto&c:cs){ Q u=dv(c.v,I(R(c.s))); ok&=eq(u,c.want)&&root(mul(u,I(3)),mul(u,I(4)),mul(u,I(5))); }
  report("unit from any side (9 cases)",ok);
  Q u1=dv(I(3),I(3)), u2=dv(I(5),I(4));
  report("units disagree -> not 3-4-5, root needed (sqrt 34)",!eq(u1,u2)&&eq(u2,mk(5,4))&&(9+25==34));
  ok=true; Q us[]={I(1),I(2),I(5),mk(7,5)};
  for(auto u:us) ok&=!eq(add(mul(I(3),u),mul(I(4),u)),mul(I(5),u));
  report("not plus: 3u+4u=7u != 5u",ok);
  ok=true; Q t[3][3]={{I(3),I(4),I(5)},{I(15),I(20),I(25)},{mk(21,5),mk(28,5),I(7)}};
  for(auto&r:t){ Q a=r[0],b=r[1],c=r[2];
    ok&=root(a,b,c)&&eq(sub(mul(c,c),mul(b,b)),mul(a,a))&&eq(sub(mul(c,c),mul(a,a)),mul(b,b)); }
  report("solve for any one factor",ok);
  int sg[4][2]={{1,1},{1,-1},{-1,-1},{-1,1}}, want[4][2]={{3,4},{3,-4},{-3,-4},{-3,4}}; ok=true;
  for(int q=0;q<4;q++){ int h=3*sg[q][0], b=4*sg[q][1]; ok&=h==want[q][0]&&b==want[q][1]&&h*h+b*b==25; }
  report("four quadrants, all roots 5",ok);
  auto fold=[](int d){ d%=360; return d<=90?d:d<=180?180-d:d<=270?d-180:360-d; };
  report("stored 60 associates 60/120/240/300; 0 and 360 one wrap",
         fold(60)==60&&fold(120)==60&&fold(240)==60&&fold(300)==60&&fold(360)==fold(0));
  Q s=mk(3,5), co=mk(4,5), tt=mk(1,3), one=I(1);
  report("3-4-5 = exact point (4/5, 3/5) on unit circle, t=1/3",
    eq(add(mul(s,s),mul(co,co)),one)&&eq(co,dv(sub(one,mul(tt,tt)),add(one,mul(tt,tt))))&&eq(s,dv(mul(I(2),tt),add(one,mul(tt,tt)))));
  report("negative control 3-4-6 rejected",!root(I(3),I(4),I(6)));
  std::printf("%d/%d\n",total-fails,total);
  return fails?1:0;
}
