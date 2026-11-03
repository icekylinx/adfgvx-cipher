// ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;const string A="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",C="ADFGVX";
struct Matcher{
 string src;vector<string>cols;int W,B,N;long long nodes=0;vector<vector<int>>cost;vector<int>path,answer;int firstOffset=-1,answerCost=-1;unordered_map<unsigned,int>failed;
 int diff(const string&s,int start,int pos,int count){int z=0;for(int i=0;i<count;i++){z+=s[start+i]!=src[pos+i];if(z>B)return z;}return z;}
 bool dfs(int pos,unsigned used,int spent){nodes++;if(pos==N){answer=path;answerCost=spent;return true;}auto it=failed.find(used);if(it!=failed.end()&&it->second<=spent)return false;unordered_set<string>same;
  for(int c=0;c<W;c++)if(!(used&(1u<<c))&&same.insert(cols[c]).second){int n=min((int)cols[c].size(),N-pos),next=spent+cost[pos][c];if(next>B)continue;path.push_back(c);if(dfs(pos+n,used|(1u<<c),next))return true;path.pop_back();}
  auto q=failed.find(used);if(q==failed.end()||spent<q->second)failed[used]=spent;return false;
 }
 bool solve(){cost.assign(N,vector<int>(W));for(int p=0;p<N;p++)for(int c=0;c<W;c++)cost[p][c]=diff(cols[c],0,p,min((int)cols[c].size(),N-p));unordered_set<string>same;
  for(int c=0;c<W;c++)if(same.insert(cols[c]).second)for(int offset=0;offset<(int)cols[c].size();offset++){int n=min((int)cols[c].size()-offset,N),spent=diff(cols[c],offset,0,n);if(spent>B)continue;path={c};failed.clear();if(dfs(n,1u<<c,spent)){firstOffset=offset;return true;}}return false;
 }
};
int main(int argc,char**argv){if(argc<7)return 2;ifstream kf(argv[1]),pf(argv[2]),sf(argv[3]);if(!kf||!pf||!sf)return 3;string source;sf>>source;int minw=stoi(argv[4]),maxw=stoi(argv[5]),budget=stoi(argv[6]);if(maxw>30||budget<0||budget>2)return 4;vector<pair<string,string>>keys,pool;string id,text;while(kf>>id>>text)keys.push_back({id,text});while(pf>>id>>text)pool.push_back({id,text});array<int,6>needed{};for(char c:source){auto z=C.find(c);if(z==string::npos)return 5;needed[z]++;}long long projects=0,histpass=0,nodes=0,hits=0;
 for(auto [kid,square]:keys){if(square.size()!=36||unordered_set<char>(square.begin(),square.end()).size()!=36)return 6;for(auto [pid,plain]:pool){if(plain.size()*2<source.size())continue;string mid;array<int,6>available{};for(char ch:plain){auto z=square.find(ch);if(z==string::npos)return 7;char a=C[z/6],b=C[z%6];mid+=a;mid+=b;available[z/6]++;available[z%6]++;}int excess=0;for(int j=0;j<6;j++)excess+=max(0,needed[j]-available[j]);
  for(int width=minw;width<=maxw;width++){projects++;if(excess>budget)continue;histpass++;Matcher m;m.src=source;m.N=source.size();m.W=width;m.B=budget;for(int col=0;col<width;col++){string s;for(int p=col;p<(int)mid.size();p+=width)s+=mid[p];m.cols.push_back(s);}if(!m.solve()){nodes+=m.nodes;continue;}nodes+=m.nodes;hits++;vector<int>order=m.answer;for(int c=0;c<width;c++)if(find(order.begin(),order.end(),c)==order.end())order.push_back(c);string cipher;for(int c:order)cipher+=m.cols[c];vector<int>bad;for(int i=0;i<(int)source.size();i++)if(source[i]!=cipher[m.firstOffset+i])bad.push_back(i);if((int)bad.size()!=m.answerCost)return 8;vector<int>ranks(width);for(int i=0;i<width;i++)ranks[order[i]]=i+1;
   cout<<"{\"donor\":\""<<pid<<"\",\"key\":\""<<kid<<"\",\"width\":"<<width<<",\"full_length\":"<<mid.size()<<",\"observed_offset\":"<<m.firstOffset<<",\"cost\":"<<bad.size()<<",\"used_columns\":[";for(int i=0;i<(int)m.answer.size();i++){if(i)cout<<',';cout<<m.answer[i];}cout<<"],\"full_column_order\":[";for(int i=0;i<width;i++){if(i)cout<<',';cout<<order[i];}cout<<"],\"ranks\":[";for(int i=0;i<width;i++){if(i)cout<<',';cout<<ranks[i];}cout<<"],\"mismatch_source_indices\":[";for(int i=0;i<(int)bad.size();i++){if(i)cout<<',';cout<<bad[i];}cout<<"]}\n";
  }
 }}cerr<<"projects "<<projects<<" histogram_pass "<<histpass<<" dfs_nodes "<<nodes<<" hits "<<hits<<'\n';}
