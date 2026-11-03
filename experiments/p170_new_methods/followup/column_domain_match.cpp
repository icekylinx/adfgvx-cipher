// ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;const string A="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",C="ADFGVX";using Mask=uint64_t;
struct Donor{string id;vector<Mask>domains;};
struct Matcher{
 vector<Mask>original,current,answer;vector<vector<int>>cols;array<array<Mask,6>,2>allow{};string src;int W,N,maxUnfixed;long long nodes=0;vector<pair<int,Mask>>trail;vector<int>path,answerPath;int firstOffset=-1,answerUnfixed=-1;
 bool apply(int c,int offset,int pos,int&unfixed){int count=min((int)cols[c].size()-offset,N-pos),extra=0;for(int j=0;j<count;j++)extra+=__builtin_popcountll(original[cols[c][offset+j]/2])!=1;if(unfixed+extra>maxUnfixed)return false;for(int j=0;j<count;j++){int mid=cols[c][offset+j],p=mid/2,half=mid%2,z=C.find(src[pos+j]);Mask next=current[p]&allow[half][z];if(!next)return false;trail.push_back({p,current[p]});current[p]=next;}unfixed+=extra;return true;}
 void undo(size_t mark){while(trail.size()>mark){auto[p,v]=trail.back();trail.pop_back();current[p]=v;}}
 bool dfs(int pos,unsigned used,int unfixed){nodes++;if(pos==N){answer=current;answerPath=path;answerUnfixed=unfixed;return true;}int available=0,known=0;for(int c=0;c<W;c++)if(!(used&(1u<<c)))for(int mid:cols[c]){available++;known+=__builtin_popcountll(original[mid/2])==1;}if(available<N-pos||unfixed+max(0,N-pos-known)>maxUnfixed)return false;
  for(int c=0;c<W;c++)if(!(used&(1u<<c))){size_t mark=trail.size();int next=unfixed,n=min((int)cols[c].size(),N-pos);if(apply(c,0,pos,next)){path.push_back(c);if(dfs(pos+n,used|(1u<<c),next))return true;path.pop_back();}undo(mark);}return false;
 }
 bool solve(){for(int c=0;c<W;c++)for(int offset=0;offset<(int)cols[c].size();offset++){size_t mark=trail.size();int unfixed=0,n=min((int)cols[c].size()-offset,N);if(apply(c,offset,0,unfixed)){path={c};if(dfs(n,1u<<c,unfixed)){firstOffset=offset;return true;}}undo(mark);}return false;}
};
int main(int argc,char**argv){if(argc<7)return 2;ifstream kf(argv[1]),df(argv[2]),sf(argv[3]);if(!kf||!df||!sf)return 3;vector<pair<string,string>>keys;string id,square,source;while(kf>>id>>square)keys.push_back({id,square});sf>>source;for(char c:source)if(C.find(c)==string::npos)return 4;vector<Donor>donors;string line;while(getline(df,line)){istringstream in(line);Donor d;int n;if(!(in>>d.id>>n))continue;d.domains.resize(n);for(Mask&x:d.domains)if(!(in>>x)||!x||x>>36)return 5;donors.push_back(d);}int lo=stoi(argv[4]),hi=stoi(argv[5]),support=stoi(argv[6]);if(hi>30||support<0||support>(int)source.size())return 6;array<int,6>needed{};for(char c:source)needed[C.find(c)]++;long long projects=0,histpass=0,nodes=0,hits=0;
 for(auto[kid,sq]:keys){if(sq.size()!=36)return 7;array<array<Mask,6>,2>allow{};array<array<int,2>,36>coord{};Mask seen=0;for(int cell=0;cell<36;cell++){int letter=A.find(sq[cell]);if(letter<0||letter>35||(seen&(Mask(1)<<letter)))return 8;seen|=Mask(1)<<letter;allow[0][cell/6]|=Mask(1)<<letter;allow[1][cell%6]|=Mask(1)<<letter;coord[letter]={cell/6,cell%6};}
 for(auto d:donors){int L=d.domains.size()*2;if(L<(int)source.size())continue;array<int,6>maximum{},fixedCount{};for(Mask mask:d.domains){array<int,6>best{};for(int letter=0;letter<36;letter++)if(mask&(Mask(1)<<letter)){array<int,6>count{};count[coord[letter][0]]++;count[coord[letter][1]]++;for(int z=0;z<6;z++)best[z]=max(best[z],count[z]);}for(int z=0;z<6;z++)maximum[z]+=best[z];if(__builtin_popcountll(mask)==1){int letter=__builtin_ctzll(mask);fixedCount[coord[letter][0]]++;fixedCount[coord[letter][1]]++;}}
 int excess=0;bool possible=true;for(int z=0;z<6;z++){if(needed[z]>maximum[z])possible=false;excess+=max(0,needed[z]-fixedCount[z]);}if(excess>(int)source.size()-support)possible=false;
 for(int width=lo;width<=hi;width++){projects++;if(!possible)continue;histpass++;Matcher m;m.original=d.domains;m.current=d.domains;m.allow=allow;m.src=source;m.W=width;m.N=source.size();m.maxUnfixed=source.size()-support;m.cols.resize(width);for(int c=0;c<width;c++)for(int p=c;p<L;p+=width)m.cols[c].push_back(p);if(!m.solve()){nodes+=m.nodes;continue;}nodes+=m.nodes;hits++;vector<int>order=m.answerPath;for(int c=0;c<width;c++)if(find(order.begin(),order.end(),c)==order.end())order.push_back(c);vector<int>ranks(width);for(int i=0;i<width;i++)ranks[order[i]]=i+1;string plain;for(Mask v:m.answer)plain+=A[__builtin_ctzll(v)];cout<<"{\"donor\":\""<<d.id<<"\",\"key\":\""<<kid<<"\",\"width\":"<<width<<",\"full_length\":"<<L<<",\"observed_offset\":"<<m.firstOffset<<",\"directly_fixed_coordinate_support\":"<<m.N-m.answerUnfixed<<",\"coordinates_relying_on_partial_donor_domains\":"<<m.answerUnfixed<<",\"used_columns\":[";for(int i=0;i<(int)m.answerPath.size();i++){if(i)cout<<',';cout<<m.answerPath[i];}cout<<"],\"full_column_order\":[";for(int i=0;i<width;i++){if(i)cout<<',';cout<<order[i];}cout<<"],\"ranks\":[";for(int i=0;i<width;i++){if(i)cout<<',';cout<<ranks[i];}cout<<"],\"remaining_plaintext_domains\":[";for(int i=0;i<(int)m.answer.size();i++){if(i)cout<<',';cout<<m.answer[i];}cout<<"],\"joint_witness_plaintext\":\""<<plain<<"\"}\n";
 }}}
 cerr<<"projects "<<projects<<" histogram_pass "<<histpass<<" dfs_nodes "<<nodes<<" hits "<<hits<<'\n';}
