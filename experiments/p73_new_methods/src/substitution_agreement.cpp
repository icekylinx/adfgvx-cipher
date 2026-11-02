// Maximum bijective substitution agreement over every sufficiently long overlap.
// ADFGVX Cipher; icekylinx and GPT-6 Astra Pro.
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
int ix(char c){if(c>='A'&&c<='Z')return c-'A';if(c>='0'&&c<='9')return c-'0'+26;return -1;}
int maximum(const int count[36][36]){
 vector<int> rows,cols;for(int i=0;i<36;i++){bool a=false,b=false;for(int j=0;j<36;j++){a|=count[i][j]>0;b|=count[j][i]>0;}if(a)rows.push_back(i);if(b)cols.push_back(i);}
 int n=max(rows.size(),cols.size());if(!n)return 0;
 int u[37]={},v[37]={},p[37]={},way[37]={};
 for(int i=1;i<=n;i++){
  p[0]=i;int j0=0,minv[37];bool used[37]={};fill(minv,minv+37,1000000);
  do{used[j0]=true;int i0=p[j0],delta=1000000,j1=0;
   for(int j=1;j<=n;j++)if(!used[j]){
    int w=i0<=int(rows.size())&&j<=int(cols.size())?count[rows[i0-1]][cols[j-1]]:0;
    int cur=-w-u[i0]-v[j];if(cur<minv[j]){minv[j]=cur;way[j]=j0;}
    if(minv[j]<delta){delta=minv[j];j1=j;}
   }
   for(int j=0;j<=n;j++)if(used[j]){u[p[j]]+=delta;v[j]-=delta;}else minv[j]-=delta;
   j0=j1;
  }while(p[j0]);
  do{int j1=way[j0];p[j0]=p[j1];j0=j1;}while(j0);
 }
 return v[0];
}
struct Result {int matched=0,known=1,len=0,qs=0,ps=0;};
bool better(int matched,int known,int len,const Result&b){int l=matched*b.known,r=b.matched*known;return l>r||(l==r&&(known>b.known||(known==b.known&&len>b.len)));}
int main(){int nq,np,minknown;if(!(cin>>nq>>np>>minknown))return 2;vector<string>q(nq),p(np);for(auto&s:q)cin>>s;for(auto&s:p)cin>>s;
 for(int qi=0;qi<nq;qi++)for(int pi=0;pi<np;pi++){
  const string&a=q[qi],&b=p[pi];Result best;
  for(int d=-int(a.size())+minknown;d<=int(b.size())-minknown;d++){
   int as=max(0,-d),bs=max(0,d),n=min(int(a.size())-as,int(b.size())-bs),known=0;
   int count[36][36]={};for(int k=0;k<n;k++){int x=ix(a[as+k]),y=ix(b[bs+k]);if(x>=0&&y>=0){count[x][y]++;known++;}}
   if(known<minknown)continue;
   int rbound=0,cbound=0;for(int i=0;i<36;i++){int rmax=0,cmax=0;for(int j=0;j<36;j++){rmax=max(rmax,count[i][j]);cmax=max(cmax,count[j][i]);}rbound+=rmax;cbound+=cmax;}
   if(!better(min(rbound,cbound),known,n,best))continue;
   int matched=maximum(count);if(better(matched,known,n,best))best={matched,known,n,as,bs};
  }
  if(best.len)cout<<qi<<' '<<pi<<' '<<best.matched<<' '<<best.known<<' '<<best.len<<' '<<best.qs<<' '<<best.ps<<'\n';
 }
}
