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
vector<int> decode(const State&st){vector<int> full(N),coord(N),pt(N/2);int at=0,g=0;
 for(int i=0;i<N;i++)full[i]=(g<M&&st.loss[g]==i)?st.fill[g++]:source[at++];
 if(at!=(int)source.size()||g!=M)throw runtime_error("loss state");
 for(int i=0;i<N;i++)coord[layout[i]]=full[i];
 for(int i=0;i<N/2;i++)pt[i]=st.square[6*coord[2*i]+coord[2*i+1]];return pt;
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
double fitness(const State&st,double weight,double *qout=nullptr,double *lout=nullptr){auto pt=decode(st);double q=0;for(int i=0;i+3<(int)pt.size();i++)q+=quad[((pt[i]*36+pt[i+1])*36+pt[i+2])*36+pt[i+3]];double l=lexscore(pt);if(qout)*qout=q;if(lout)*lout=l;return q+weight*l;}
void sort_loss(State&st){vector<pair<int,int>> z;for(int i=0;i<M;i++)z.push_back({st.loss[i],st.fill[i]});sort(z.begin(),z.end());for(int i=0;i<M;i++){st.loss[i]=z[i].first;st.fill[i]=z[i].second;}}
void mutate(State&st){int type=ri(10);if(type<2&&unknown.size()>1){int a=unknown[ri(unknown.size())],b=unknown[ri(unknown.size())];swap(st.square[a],st.square[b]);}
 else if(type<5){st.fill[ri(M)]=ri(6);}
 else{int a=ri(M),p=ri(3)?st.loss[a]+(ri(2)?1:-1)*(1+ri(5)):ri(N);if(p<0||p>=N||find(st.loss.begin(),st.loss.end(),p)!=st.loss.end())return;st.loss[a]=p;if(ri(4)==0)st.fill[a]=ri(6);sort_loss(st);}}
string plain(const State&st){string s;for(int c:decode(st))s+=AL[c];return s;}
void emit(const State&st,double value,double weight,long long proposal,int restart,double seconds){double q,l;fitness(st,weight,&q,&l);
 cout<<setprecision(12)<<"{\"score\":"<<value<<",\"quad_sum\":"<<q<<",\"word_sum\":"<<l<<",\"word_weight\":"<<weight<<",\"proposal\":"<<proposal<<",\"restart\":"<<restart<<",\"seconds\":"<<seconds<<",\"square\":\"";for(int c:st.square)cout<<AL[c];cout<<"\",\"loss\":[";for(int i=0;i<M;i++)cout<<(i?",":"")<<st.loss[i];cout<<"],\"fill\":\"";for(int c:st.fill)cout<<CO[c];cout<<"\",\"plaintext\":\""<<plain(st)<<"\"}"<<endl;}
int main(int argc,char**argv){if(argc!=8){cerr<<"usage: word_loss QUAD LEX INPUT SECONDS WEIGHT SEED INITIAL\n";return 2;}try{
 ifstream f(argv[1],ios::binary);quad.resize(36*36*36*36);f.read((char*)quad.data(),quad.size()*4);if(!f)throw runtime_error("quad model");load_lexicon(argv[2]);
 ifstream in(argv[3]);string sq,ct;in>>K>>M>>sq;State base;base.square.resize(36);vector<int> unused;array<int,36>seen{};for(int i=0;i<36;i++){int z=AL.find(sq[i]);if(z<0){unknown.push_back(i);base.square[i]=-1;}else{base.square[i]=z;seen[z]++;}}for(int i=0;i<36;i++)if(!seen[i])unused.push_back(i);ranks.resize(K);for(int&i:ranks)in>>i;in>>ct;for(char c:ct){auto x=CO.find(c);if(x==string::npos)throw runtime_error("source must have no erasures");source.push_back(x);}N=source.size()+M;if(N%2||M<1||M>10)throw runtime_error("frame size");
 vector<int> cols(K);iota(cols.begin(),cols.end(),0);sort(cols.begin(),cols.end(),[](int a,int b){return ranks[a]<ranks[b];});for(int c:cols)for(int i=c;i<N;i+=K)layout.push_back(i);
 double budget=stod(argv[4]),weight=stod(argv[5]);rng.seed(stoull(argv[6]));State global;double gs=-1e100;auto start=chrono::steady_clock::now();long long proposals=0;int restart=0;
 auto seconds=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
 // Optional prior feasible state, never control truth; "-" means blind start.
 if(string(argv[7])!="-"){ifstream seed(argv[7]);string q,fill;seed>>q;global.square.clear();for(char c:q)global.square.push_back(AL.find(c));global.loss.resize(M);global.fill.resize(M);for(int&i:global.loss)seed>>i;seed>>fill;for(int i=0;i<M;i++)global.fill[i]=CO.find(fill[i]);if(!seed)throw runtime_error("initial state");for(int i=0;i<36;i++)if(base.square[i]>=0&&base.square[i]!=global.square[i])throw runtime_error("anchor conflict");gs=fitness(global,weight);emit(global,gs,weight,proposals,-1,seconds());}
 while(seconds()<budget){State st=base;shuffle(unused.begin(),unused.end(),rng);for(size_t i=0;i<unknown.size();i++)st.square[unknown[i]]=unused[i];st.loss.resize(M);st.fill.resize(M);vector<int> pos(N);iota(pos.begin(),pos.end(),0);shuffle(pos.begin(),pos.end(),rng);copy(pos.begin(),pos.begin()+M,st.loss.begin());sort(st.loss.begin(),st.loss.end());for(int&i:st.fill)i=ri(6);
  if(restart&&restart%4!=0&&gs>-1e90){st=global;for(int j=0;j<5+ri(30);j++)mutate(st);}double score=fitness(st,weight);State best=st;double bestscore=score;
  const int iterations=30000;for(int it=0;it<iterations;it++){State old=st;mutate(st);double candidate=fitness(st,weight);double temp=(restart%6==0?15.0:5.0)*pow(.015,double(it)/iterations);if(candidate>=score||uniform()<exp((candidate-score)/temp))score=candidate;else st=old;if(score>bestscore){bestscore=score;best=st;}proposals++;if(proposals%5000==0&&seconds()>=budget)break;}
  if(bestscore>gs){gs=bestscore;global=best;emit(global,gs,weight,proposals,restart,seconds());}restart++;
 }
 emit(global,gs,weight,proposals,restart,seconds());return 0;
 }catch(const exception&e){cerr<<e.what()<<endl;return 2;}}
