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
int main(int argc,char**argv){if(argc!=3)return 2;ifstream f(argv[1],ios::binary);quad.resize(36*36*36*36);f.read((char*)quad.data(),quad.size()*4);load_lexicon(argv[2]);string s;while(cin>>s){vector<int>p;for(char c:s)p.push_back(AL.find(c));double q=0;for(int i=0;i+3<(int)p.size();i++)q+=quad[((p[i]*36+p[i+1])*36+p[i+2])*36+p[i+3]];cout<<setprecision(12)<<q<<" "<<lexscore(p)<<"\n";}return 0;}