// C++ port of frac_trunc_sig (integer-only, cut toward zero, plain positional text) + redshift ratio.
#include <iostream>
#include <string>
typedef __int128 i128;
static std::string s128(i128 v){ if(v==0) return "0"; std::string r; while(v>0){ r.insert(r.begin(), char('0'+(int)(v%10))); v/=10;} return r; }
static i128 p10(int e){ i128 r=1; while(e-->0) r*=10; return r; }
static i128 gcd128(i128 a,i128 b){ while(b){ i128 t=a%b; a=b; b=t;} return a; }
std::string trunc_sig(i128 num, i128 den, int n){
  if(num==0) return "0";
  bool neg=false;
  if(num<0){neg=true; num=-num;}
  i128 g=gcd128(num,den); num/=g; den/=g;
  int e=(int)s128(num).size()-(int)s128(den).size();
  auto ge=[&](int p){ return p>=0 ? (num>=den*p10(p)) : (num*p10(-p)>=den); };
  while(!ge(e)) e--;
  while(ge(e+1)) e++;
  int s=n-1-e; i128 k = s>=0 ? (num*p10(s))/den : num/(den*p10(-s));
  std::string d=s128(k), t;
  if(s<=0) t=d+std::string(-s,'0');
  else if(s>=(int)d.size()) t="0."+std::string(s-d.size(),'0')+d;
  else t=d.substr(0,d.size()-s)+"."+d.substr(d.size()-s);
  return (neg?"-":"")+t;
}
int main(){
  // redshift: g=980665/100000, c=299792458
  i128 c=299792458;
  for(int dh: {1,10,100,1000}) std::cout<<"REDSHIFT "<<dh<<" "<<trunc_sig((i128)980665*dh, (i128)100000*c*c, 12)<<"\n";
  std::cout<<"CUT 1999999/1000000 3 "<<trunc_sig(1999999,1000000,3)<<"\n";
  std::cout<<"CUT -1999999/1000000 3 "<<trunc_sig(-1999999,1000000,3)<<"\n";
  std::cout<<"CUT 1/3 12 "<<trunc_sig(1,3,12)<<"\n";
  std::cout<<"CUT 2/3 4 "<<trunc_sig(2,3,4)<<"\n";
  std::cout<<"CUT 0 5 "<<trunc_sig(0,1,5)<<"\n";
  std::cout<<"CUT 1/1e20 4 "<<trunc_sig(1,(i128)10000000000LL*10000000000LL,4)<<"\n";
  std::cout<<"LAMBDA 156525121/1210320000 12 "<<trunc_sig(156525121,1210320000,12)<<"\n";
}
