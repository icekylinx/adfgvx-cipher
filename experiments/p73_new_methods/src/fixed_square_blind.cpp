// Source-preserving stochastic loss/fill and partial-square search.
// ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro; pilot, no optimum claim.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
const string AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", CO="ADFGVX";
struct Trie {array<int,26> next; int id=-1; Trie(){next.fill(-1);}};
vector<Trie> trie(1); vector<float> word_score,quad; vector<string> words;
unordered_map<uint64_t,float> pairs;
struct Match {int end,id;float score;};
struct State {vector<int> square,loss,fill;};
vector<int> ranks,source,layout,unknown;int N,K,M;
mt19937_64 rng;
int ri(int n){return rng()%n;}
double uniform(){return (rng()>>11)*0x1.0p-53;}
void load_lexicon(const string&path){ifstream f(path);int n,b;f>>n>>b;string w;float s;
 for(int id=0;id<n;id++){f>>w>>s;words.push_back(w);word_score.push_back(s);int node=0;
  for(char c:w){int q=c-'A';if(trie[node].next[q]<0){int z=trie.size();trie[node].next[q]=z;trie.emplace_back();}node=trie[node].next[q];}trie[node].id=id;}
 for(int i=0;i<b;i++){int a,b;float s;f>>a>>b>>s;pairs[(uint64_t(a)<<32)|uint32_t(b)]=s;}
 if(!f)throw runtime_error("invalid lexicon");
}
double lexscore(const vector<int>&pt){int n=pt.size();vector<vector<Match>> match(n);vector<vector<pair<int,double>>> dp(n+1);dp[0].push_back({-1,0});
 for(int i=0;i<n;i++){
  // Single-character fallback makes any authentic garble feasible.
  match[i].push_back({i+1,-1,pt[i]==23?-.25f:-3.0f});
  if(pt[i]>=26){for(int j=i;j<n&&j<i+10&&pt[j]>=26;j++)match[i].push_back({j+1,-2,float(-1.0-(j-i+1))});}
  int node=0;for(int j=i;j<n&&j<i+32&&pt[j]<26;j++){node=trie[node].next[pt[j]];if(node<0)break;if(trie[node].id>=0){int id=trie[node].id;match[i].push_back({j+1,id,word_score[id]});}}
  for(auto m:match[i]){double best=-1e100;for(auto prev:dp[i]){double s=prev.second+m.score;if(prev.first>=0&&m.id>=0){auto it=pairs.find((uint64_t(prev.first)<<32)|uint32_t(m.id));if(it!=pairs.end())s+=.65*it->second;}best=max(best,s);}
   auto &dest=dp[m.end];bool found=false;for(auto &x:dest)if(x.first==m.id){x.second=max(x.second,best);found=true;break;}if(!found)dest.push_back({m.id,best});}
 }
 double best=-1e100;for(auto x:dp[n])best=max(best,x.second);return best;
}

vector<array<int,2>> source_pairs;
vector<int> fixed_base;
vector<int> decode_frozen(const State&st){vector<int> pt(source_pairs.size());
 for(size_t i=0;i<source_pairs.size();i++){auto p=source_pairs[i];int a=p[0]<0?st.fill[-p[0]-1]:p[0],b=p[1]<0?st.fill[-p[1]-1]:p[1];pt[i]=st.square[6*a+b];}return pt;}
double score_frozen(const State&st,double weight,double *qout=nullptr,double *lout=nullptr){auto pt=decode_frozen(st);double q=0;
 for(int i=0;i+3<(int)pt.size();i++)q+=quad[((pt[i]*36+pt[i+1])*36+pt[i+2])*36+pt[i+3]];
 double l=weight==0?0:lexscore(pt);if(qout)*qout=q;if(lout)*lout=l;return q+weight*l;}
void mutate_frozen(State&st){
 if(M&&ri(10)==0){st.fill[ri(M)]=ri(6);return;}
 int a=unknown[ri(unknown.size())],b=unknown[ri(unknown.size())];swap(st.square[a],st.square[b]);
 if(ri(20)==0){int c=unknown[ri(unknown.size())];swap(st.square[b],st.square[c]);}
}
void emit_frozen(const State&st,double value,double weight,long long proposals,int restart,double seconds){double q,l;score_frozen(st,weight,&q,&l);
 cout<<setprecision(12)<<"{\"score\":"<<value<<",\"quad_sum\":"<<q<<",\"word_sum\":"<<l<<",\"word_weight\":"<<weight<<",\"proposals\":"<<proposals<<",\"restart\":"<<restart<<",\"seconds\":"<<seconds<<",\"square\":\"";
 for(int c:st.square)cout<<AL[c];cout<<"\",\"erasure_fill\":\"";for(int c:st.fill)cout<<CO[c];cout<<"\",\"plaintext\":\"";for(int c:decode_frozen(st))cout<<AL[c];cout<<"\"}"<<endl;}
int main(int argc,char**argv){if(argc!=7){cerr<<"usage: fixed_square QUAD LEX INPUT SECONDS WEIGHT SEED\n";return 2;}
 try{ifstream f(argv[1],ios::binary);quad.resize(36*36*36*36);f.read((char*)quad.data(),quad.size()*4);if(!f)throw runtime_error("quad model");load_lexicon(argv[2]);
 ifstream in(argv[3]);string sq,ct;in>>K>>sq;if(K<2||K>40||sq.size()!=36)throw runtime_error("input frame");
 State base;base.square.resize(36);vector<int> unused;array<int,36>seen{};
 for(int i=0;i<36;i++){auto z=AL.find(sq[i]);if(z==string::npos){if(sq[i]!='?')throw runtime_error("square symbol");unknown.push_back(i);base.square[i]=-1;}else{base.square[i]=z;if(seen[z]++)throw runtime_error("duplicate square");}}
 for(int i=0;i<36;i++)if(!seen[i])unused.push_back(i);if(unknown.size()<2)throw runtime_error("need at least two unknown cells");
 ranks.resize(K);for(int&i:ranks)in>>i;auto sr=ranks;sort(sr.begin(),sr.end());for(int i=0;i<K;i++)if(sr[i]!=i+1)throw runtime_error("rank permutation");
 in>>ct;if(!in||ct.size()%2)throw runtime_error("ciphertext");N=ct.size();vector<int> src(N),stream(N);M=0;
 for(int i=0;i<N;i++){auto c=CO.find(ct[i]);if(c==string::npos){if(ct[i]!='?')throw runtime_error("ciphertext symbol");src[i]=-(++M);}else src[i]=c;}
 vector<int> cols(K);iota(cols.begin(),cols.end(),0);sort(cols.begin(),cols.end(),[](int a,int b){return ranks[a]<ranks[b];});int at=0;
 for(int c:cols)for(int i=c;i<N;i+=K)stream[i]=src[at++];for(int i=0;i<N;i+=2)source_pairs.push_back({stream[i],stream[i+1]});
 double budget=stod(argv[4]),weight=stod(argv[5]);rng.seed(stoull(argv[6]));auto start=chrono::steady_clock::now();
 auto seconds=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
 State global;double gs=-1e100;long long proposals=0;int restart=0;
 while(seconds()<budget){State st=base;shuffle(unused.begin(),unused.end(),rng);for(size_t i=0;i<unknown.size();i++)st.square[unknown[i]]=unused[i];st.fill.resize(M);for(int&i:st.fill)i=ri(6);
  if(restart&&restart%3!=0){st=global;for(int j=0;j<3+ri(20);j++)mutate_frozen(st);}double score=score_frozen(st,weight),bs=score;State best=st;
  const int iterations=30000;for(int i=0;i<iterations;i++){State prev=st;mutate_frozen(st);double v=score_frozen(st,weight);
   double temp=(restart%6==0?15.0:5.0)*(1+.4*weight)*pow(.015,double(i)/iterations);
   if(v>=score||uniform()<exp((v-score)/temp))score=v;else st=prev;if(score>bs){bs=score;best=st;}proposals++;if(proposals%5000==0&&seconds()>=budget)break;}
  if(bs>gs){gs=bs;global=best;emit_frozen(global,gs,weight,proposals,restart,seconds());}restart++;
 }
 emit_frozen(global,gs,weight,proposals,restart,seconds());return 0;
 }catch(const exception&e){cerr<<e.what()<<endl;return 2;}}
