// Source-preserving p73 column-pair profile search, 3 November 2026.
// ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
// Finite stochastic profile optimization; no plaintext or key is accepted.
#include <bits/stdc++.h>
using namespace std;
string C="ADFGVX";
struct Hit{double score;vector<int>co;};
int main(int argc,char**argv){ifstream pf(argv[1]),cf(argv[2]);string src;cf>>src;int n=src.size(),k=atoi(argv[3]),reps=atoi(argv[4]),steps=atoi(argv[5]),topn=atoi(argv[7]),h=n/k,r=n%k;mt19937 gen(atoi(argv[6]));assert(n%2==0&&k%2==0);double mu[36],var[36],cost[100][36];for(int i=0;i<36;i++)pf>>mu[i]>>var[i];for(int a=0;a<=n/2;a++)for(int b=0;b<36;b++){double d=double(a)/(n/2)-mu[b];cost[a][b]=-d*d/(var[b]+.25/((n/2)*(n/2)));}
 vector<int>mask(k);fill(mask.begin(),mask.begin()+r,1);sort(mask.begin(),mask.end());int seg=0;vector<tuple<double,vector<int>,vector<int>>>global;
 do{
  vector<vector<int>>col(k);int off=0;for(int j=0;j<k;j++){for(int z=0;z<h+mask[j];z++){int v=C.find(src[off++]);col[j].push_back(v<6?v:-1);}}assert(off==n);
  vector<int>co(k);int at=0;for(int j=0;j<k;j++)if(mask[j])co[at++]=j;for(int j=0;j<k;j++)if(!mask[j])co[at++]=j;vector<pair<int,int>>moves;for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)if((a<r)==(b<r))moves.push_back({a,b});
  array<array<array<int,36>,40>,40>pc{};for(int a=0;a<k;a++)for(int b=0;b<k;b++)if(a!=b&&mask[a]==mask[b])for(int z=0;z<col[a].size();z++)if(col[a][z]>=0&&col[b][z]>=0)pc[a][b][6*col[a][z]+col[b][z]]++;
  array<int,36>cnt{};auto add=[&](int a,int b,int sign){for(int i=0;i<36;i++)cnt[i]+=sign*pc[a][b][i];};
  auto score=[&](){array<int,36>s=cnt;sort(s.begin(),s.end(),greater<int>());double v=0;for(int z=0;z<36;z++)v+=cost[s[z]][z];return v;};
  vector<Hit>hits;
  for(int rep=0;rep<reps;rep++){
   for(int z=0;z<10*k;z++){auto[a,b]=moves[gen()%moves.size()];swap(co[a],co[b]);}cnt.fill(0);for(int z=0;z<k;z+=2)add(co[z],co[z+1],1);double cur=score(),best=cur;vector<int>bestco=co;
   for(int st=0;st<steps;st++){auto[a,b]=moves[gen()%moves.size()];int pa=a&~1,pb=b&~1;add(co[pa],co[pa+1],-1);if(pb!=pa)add(co[pb],co[pb+1],-1);swap(co[a],co[b]);add(co[pa],co[pa+1],1);if(pb!=pa)add(co[pb],co[pb+1],1);double ne=score(),temp=4*pow(.005,double(st)/steps);if(ne>=cur||generate_canonical<double,53>(gen)<exp((ne-cur)/temp)){cur=ne;if(cur>best){best=cur;bestco=co;}}else{add(co[pa],co[pa+1],-1);if(pb!=pa)add(co[pb],co[pb+1],-1);swap(co[a],co[b]);add(co[pa],co[pa+1],1);if(pb!=pa)add(co[pb],co[pb+1],1);}}
   hits.push_back({best,bestco});
  }
  sort(hits.begin(),hits.end(),[](auto&a,auto&b){return a.score>b.score;});for(int z=0;z<min(topn,(int)hits.size());z++)global.push_back({hits[z].score,mask,hits[z].co});seg++;
 }while(next_permutation(mask.begin(),mask.end()));
 sort(global.begin(),global.end(),[](auto&a,auto&b){return get<0>(a)>get<0>(b);});cout<<"# segmentations "<<seg<<" candidates "<<global.size()<<'\n';
 for(auto const&[score,mask,co]:global){vector<int>ranks(k);for(int j=0;j<k;j++)ranks[j]=co[j]+1;cout<<setprecision(12)<<score<<'\t';for(int j=0;j<k;j++)cout<<mask[j];cout<<'\t';for(int j=0;j<k;j++)cout<<(j?",":"")<<ranks[j];cout<<'\n';}
}
