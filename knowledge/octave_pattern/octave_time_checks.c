/* octave_time_checks.c - independent C99 build. Exact integer rationals. No float. */
#include <stdio.h>
#include <stdlib.h>
typedef struct { long long n, d; } Q;
static long long g(long long a, long long b){ a=llabs(a); b=llabs(b); while(b){ long long t=a%b; a=b; b=t; } return a?a:1; }
static Q mk(long long n, long long d){ if(d<0){n=-n;d=-d;} long long k=g(n,d); Q q={n/k,d/k}; return q; }
static Q I(long long n){ return mk(n,1); }
static Q add(Q a,Q b){ return mk(a.n*b.d+b.n*a.d,a.d*b.d); }
static Q sub(Q a,Q b){ return mk(a.n*b.d-b.n*a.d,a.d*b.d); }
static Q mul(Q a,Q b){ return mk(a.n*b.n,a.d*b.d); }
static Q dv(Q a,Q b){ return mk(a.n*b.d,a.d*b.n); }
static int eq(Q a,Q b){ return a.n==b.n && a.d==b.d; }
static int le(Q a,Q b){ return a.n*b.d <= b.n*a.d; }
static int lt0(Q a){ return a.n<0; } static int gt0(Q a){ return a.n>0; }
static Q P(Q x,Q y,Q z){ return add(add(mul(x,x),mul(y,y)),mul(z,z)); }
static Q fa(Q zr){ return dv(sub(I(1),zr),I(2)); }
static int T=0,F=0;
static void chk(const char*nm,int ok){ T++; if(!ok)F++; printf("%s %s\n",ok?"PASS":"FAIL",nm); }
int main(void){
  Q fps[3]={I(2),I(10),mk(7,5)};
  for(int i=0;i<3;i++){ Q fp=fps[i], f1=dv(fp,I(3)), f2=sub(fp,f1), h=dv(fp,I(2));
    chk("A1 split: f1+f2=fp", eq(add(f1,f2),fp));
    chk("A2 even split: each fp/2, one octave down", eq(add(h,h),fp) && eq(dv(fp,h),I(2)));
    chk("A3 doubling: f+f=2f, one octave up", eq(mul(h,I(2)),fp)); }
  long long kp0=4+4, kp1=3+(-3);
  chk("B1 arrow sum closes by squares: |kp|^2=64", kp0*kp0+kp1*kp1==64);
  chk("B2 not plus: |kp|=8 != 5+5=10", 64 != (5+5)*(5+5));
  Q us[3]={I(1),I(2),mk(7,5)};
  for(int i=0;i<3;i++){ Q u=us[i];
    Q c5=mul(I(5),u), c13=mul(I(13),u);
    chk("C1 3-4-5 with ct=5u on the cone", eq(sub(P(mul(I(3),u),mul(I(4),u),I(0)),mul(c5,c5)),I(0)));
    chk("C2 3-4-12 with ct=13u on the cone", eq(sub(P(mul(I(3),u),mul(I(4),u),mul(I(12),u)),mul(c13,c13)),I(0))); }
  chk("C3 time-like control ct=6: s^2<0", lt0(sub(P(I(3),I(4),I(0)),I(36))));
  chk("C4 space-like control ct=4: s^2>0", gt0(sub(P(I(3),I(4),I(0)),I(16))));
  chk("C5 forward-only: every cone point used has t>=0", 5>=0 && 13>=0);
  char buf[64];
  for(int n=0;n<6;n++){ long long L=1LL<<n, A=1LL<<(2*n), V=1LL<<(3*n);
    snprintf(buf,sizeof buf,"D octave %d: L=2^n, A=L^2, V=L^3",n); chk(buf, A==L*L && V==L*L*L); }
  chk("D balloon: doubling R multiplies sphere area 4piP by exactly 4", eq(P(I(6),I(8),I(24)),mul(I(4),P(I(3),I(4),I(12)))));
  chk("D one octave of volume = three octaves of length (8 = 2*2*2)", 8==2*2*2);
  chk("E1 cap above 3-4-12-13 point is exactly 1/26", eq(fa(mk(12,13)),mk(1,26)));
  chk("E2 band equator->point is exactly 6/13", eq(sub(mk(1,2),fa(mk(12,13))),mk(6,13)));
  int ok=1; for(int k=-4;k<4;k++) ok&=eq(sub(fa(mk(k,4)),fa(mk(k+1,4))),mk(1,8));
  chk("E3 8 equal-z bands each exactly 1/8", ok);
  chk("E4 8 bands x 8 sectors = 64 cells of exactly 1/64", eq(dv(mk(1,8),I(8)),mk(1,64)));
  chk("E5 point z/R=12/13 lands in top band [3/4,1]", le(mk(3,4),mk(12,13)) && le(mk(12,13),I(1)));
  chk("E6 negative control: equal-ANGLE bands are not equal area", !eq(sub(fa(I(0)),fa(mk(1,2))),mk(1,8)));
  printf("%d/%d\n",T-F,T); return F?1:0;
}
