// Exact maximum word/bigram segmentation of position-wise letter domains.
// Exploratory only: a fluent compatible filling is not source evidence.
// icekylinx and GPT-6 Astra Pro; Apache-2.0.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;
const string AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
constexpr double NEG=-1e100;
struct Trie {array<int,26> next;int id=-1;Trie(){next.fill(-1);}};
struct Cell {double score=NEG;int pos=-1,prev=-1;char fallback='?';double bonus=0;};
vector<Trie> trie(1);
vector<string> words;
vector<double> scores;
vector<vector<pair<int,double>>> incoming;
double fallback_score=-3,bigram_weight=.65,x_score=-.25;

void load(const string &path){
 ifstream f(path);int n,b;f>>n>>b;
 if(!f||n<1||b<0)throw runtime_error("lexicon header");
 incoming.resize(n);
 for(int id=0;id<n;id++){
  string w;double s;f>>w>>s;
  if(!f||w.empty()||w.size()>64)throw runtime_error("lexicon word");
  words.push_back(w);scores.push_back(s);int node=0;
  for(char c:w){if(c<'A'||c>'Z')throw runtime_error("nonalphabetic lexicon word");
   int q=c-'A';if(trie[node].next[q]<0){trie[node].next[q]=trie.size();trie.emplace_back();}
   node=trie[node].next[q];}
  if(trie[node].id>=0)throw runtime_error("duplicate lexicon word");
  trie[node].id=id;
 }
 for(int j=0;j<b;j++){int a,z;double s;f>>a>>z>>s;
  if(!f||a<0||z<0||a>=n||z>=n||s<0)throw runtime_error("invalid or negative bigram bonus");
  incoming[z].push_back({a,s});}
 // Negative bonuses require a different baseline optimization.
 if(bigram_weight<0)throw runtime_error("negative bigram weight");
}

string esc(const string&s){string o="\"";for(char c:s){if(c=='\\'||c=='\"')o+='\\';o+=c;}return o+'\"';}

void decode(const string&id,const vector<uint64_t>&domain){
 auto start=chrono::steady_clock::now();int n=domain.size();
 vector<unordered_map<int,Cell>> dp(n+1);
 vector<pair<double,int>> best(n+1,{NEG,-1});
 dp[0][-1]={0,-1,-1,'?',0};best[0]={0,-1};
 uint64_t visits=0,matches=0,states=1;
 auto update=[&](int end,int word,double value,int prevpos,int prevword,char fallback,double bonus){
  auto found=dp[end].find(word);
  if(found==dp[end].end()){
   dp[end].emplace(word,Cell{value,prevpos,prevword,fallback,bonus});states++;
  } else if(value>found->second.score){found->second={value,prevpos,prevword,fallback,bonus};}
  else return;
  if(value>best[end].first||(value==best[end].first&&word<best[end].second))best[end]={value,word};
 };
 vector<char> digits(n,'?');
 for(int i=0;i<n;i++)for(int q=26;q<36;q++)if((domain[i]>>q)&1){digits[i]=AL[q];break;}
 for(int i=0;i<n;i++){
  if(best[i].first<=NEG/2)continue;
  char fallback='?';double penalty=NEG;
  if(domain[i]&(uint64_t(1)<<23)){fallback='X';penalty=x_score;}
  if(fallback_score>NEG/2&&fallback_score>penalty){
   for(int q=0;q<36;q++)if(q!=23&&((domain[i]>>q)&1)){fallback=AL[q];penalty=fallback_score;break;}}
  if(penalty>NEG/2)update(i+1,-1,best[i].first+penalty,i,best[i].second,fallback,0);
  for(int j=i;j<n&&j<i+10&&digits[j]!='?';j++)
   update(j+1,-2,best[i].first-1.0-(j-i+1),i,best[i].second,'?',0);
  function<void(int,int)> walk=[&](int node,int at){
   visits++;
   int w=trie[node].id;
   if(w>=0){
    matches++;
    double value=best[i].first+scores[w],bonus=0;int previous=best[i].second;
    for(auto [p,b]:incoming[w]){auto it=dp[i].find(p);if(it==dp[i].end())continue;
     double candidate=it->second.score+scores[w]+bigram_weight*b;
     if(candidate>value){value=candidate;previous=p;bonus=bigram_weight*b;}}
    update(at,w,value,i,previous,'?',bonus);
   }
   if(at==n)return;
   for(int q=0;q<26;q++)if(((domain[at]>>q)&1)&&trie[node].next[q]>=0)
    walk(trie[node].next[q],at+1);
  };
  walk(0,i);
 }
 double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<setprecision(13)<<"{\"id\":"<<esc(id)<<",\"length\":"<<n<<",\"score\":";
 if(best[n].first<=NEG/2){cout<<"null,\"feasible\":false";}
 else{
  struct Token{int begin,end,word;string text;double score,bonus;};vector<Token>tokens;
  int at=n,w=best[n].second;double sum=0;
  while(at){const Cell &c=dp[at].at(w);string text;double local;
   if(w>=0){text=words[w];local=scores[w];}
   else if(w==-2){for(int j=c.pos;j<at;j++)text+=digits[j];local=-1.0-(at-c.pos);}
   else{text=string(1,c.fallback);local=c.fallback=='X'?x_score:fallback_score;}
   tokens.push_back({c.pos,at,w,text,local,c.bonus});sum+=local+c.bonus;at=c.pos;w=c.prev;
  }
  reverse(tokens.begin(),tokens.end());
  if(abs(sum-best[n].first)>1e-7)throw runtime_error("reconstruction score differs");
  string text,seg;int fallback_count=0,x_count=0,numeric=0;
  for(auto &t:tokens){text+=t.text;if(!seg.empty())seg+=' ';seg+=t.text;
   if(t.word==-1){if(t.text=="X")x_count++;else fallback_count++;}
   if(t.word==-2)numeric+=t.end-t.begin;}
  if((int)text.size()!=n)throw runtime_error("reconstruction length");
  for(int j=0;j<n;j++)if(!(domain[j]&(uint64_t(1)<<AL.find(text[j]))))throw runtime_error("domain violation");
  cout<<best[n].first<<",\"feasible\":true,\"plaintext\":"<<esc(text)
      <<",\"segmented\":"<<esc(seg)<<",\"fallback_letters\":"<<fallback_count
      <<",\"separator_tokens\":"<<x_count<<",\"numeric_characters\":"<<numeric<<",\"tokens\":[";
  for(size_t j=0;j<tokens.size();j++){auto&t=tokens[j];if(j)cout<<',';
   cout<<"{\"start\":"<<t.begin<<",\"stop\":"<<t.end<<",\"text\":"<<esc(t.text)
       <<",\"word_id\":"<<t.word<<",\"local_score\":"<<t.score<<",\"bigram_bonus\":"<<t.bonus<<'}';}
  cout<<']';
 }
 cout<<",\"trie_visits\":"<<visits<<",\"word_edges\":"<<matches<<",\"dp_states\":"<<states
     <<",\"seconds\":"<<seconds<<"}"<<endl;
}

int main(int argc,char**argv){
 try{
  if(argc<3||argc>6){cerr<<"usage: domain_words LEXICON FRAMES [FALLBACK_SCORE=-3] [BIGRAM_WEIGHT=.65] [X_SCORE=-.25]\n";
   cerr<<"FRAMES: one line per frame, ID LENGTH followed by LENGTH decimal uint64 letter-domain masks (A-Z0-9). Use -1e100 to forbid non-X fallback.\n";return 2;}
  if(argc>3)fallback_score=stod(argv[3]);
  if(argc>4)bigram_weight=stod(argv[4]);
  if(argc>5)x_score=stod(argv[5]);
  load(argv[1]);ifstream f(argv[2]);string line;
  if(!f)throw runtime_error("cannot read frames file: "+string(argv[2]));
  while(getline(f,line)){if(line.empty()||line[0]=='#')continue;istringstream in(line);string id;int n;in>>id>>n;
   if(!in||n<1||n>2000)throw runtime_error("frame header");
   vector<uint64_t>d(n);
   for(auto &v:d){in>>v;if(!in||v==0||v>>36)throw runtime_error("domain mask");}
   string extra;if(in>>extra)throw runtime_error("extra frame input");decode(id,d);
  }
  return 0;
 }catch(const exception&e){cerr<<e.what()<<endl;return 2;}
}
