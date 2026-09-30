// p_equals_r2.cpp - independent build. Integers scaled by 5 (u in fifths). No float.
#include <cstdio>
static long long P(long long x,long long y,long long z){ return x*x+y*y+z*z; }
int main(){
  int t=0,f=0; auto rep=[&](const char*n,bool ok){t++; if(!ok)f++; std::printf("%s %s\n",ok?"PASS":"FAIL",n);};
  long long us[]={5,10,7};                     // u = 1, 2, 7/5 held as fifths
  for(long long u:us){
    long long rho=5*u, R=13*u;
    rep("plane z=0: P=25u^2=R^2, R=5u=rho", P(3*u,4*u,0)==25*u*u && 25*u*u==rho*rho);
    rep("lift: P=169u^2=R^2, R=13u", P(3*u,4*u,12*u)==169*u*u && 169*u*u==R*R);
    rep("lift = second right triangle rho^2+z^2=R^2 (5-12-13)", rho*rho+(12*u)*(12*u)==R*R);
    rep("not plus: 3u+4u+12u=19u != 13u", 3*u+4*u+12*u!=R);
  }
  rep("unit sphere point (3/13,4/13,12/13): P=1", P(3,4,12)==13*13);
  rep("latitude exact: cos=rho/R=5/13, sin=z/R=12/13", 5*5+12*12==13*13);
  rep("negative control 3-4-11 is not R=13", P(3,4,11)!=169);
  std::printf("%d/%d\n",t-f,t); return f?1:0;
}
