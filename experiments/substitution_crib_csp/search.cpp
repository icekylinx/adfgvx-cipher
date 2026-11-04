// SPDX-License-Identifier: Apache-2.0
// Exact known-plaintext / unknown-square / unknown-column-order search with
// at most E substitutions of observed coordinates; declared masks retain their slots.
// ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
#include <bits/stdc++.h>
using namespace std;
// A source has a fixed, even number of slots. '?' is an erasure in an
// existing slot; valid coordinates may be ignored only against the error budget.
// The solver never inserts, deletes, reorders, or silently corrects source slots.
constexpr int MAXK=30,MAXN=512,MAXR=64,MAXERRORS=7;
const string CO="ADFGVX",ABC="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
struct Candidate{uint64_t ignored_mask;unsigned char n,letter[36];signed char row[36],col[36];};
struct Crib{string id,text;};
vector<Crib>donors;
int n,m,k,q,e,maximum_errors,encoded[MAXN],height[MAXK],spec[MAXK][MAXR],component[MAXK][MAXR],rmap[36],cmap[36],owner[36],chosen[MAXK];
uint64_t chosen_ignored_mask[MAXK];
vector<Candidate>cache[MAXK][MAXN][MAXERRORS+1];uint32_t epoch[MAXK][MAXN][MAXERRORS+1],current_epoch;
int row_count[6], col_count[6], symbol_count[36], weight[6], observed_count[6], source_masks;
string source,reason="completed";Crib*cur;
uint64_t projects=0,completed_projects=0,nodes=0,solutions=0,generations=0,localvariants=0,local_recursion_nodes=0,maxnodes=0,maxsolutions=0;
double maxseconds=0;bool stopped=false;
chrono::steady_clock::time_point began;
double seconds(){return chrono::duration<double>(chrono::steady_clock::now()-began).count();}
bool limited(){if(stopped)return true;if(maxseconds>0&&seconds()>=maxseconds){stopped=true;reason="wall_time_limit";}if(maxnodes&&nodes>=maxnodes){stopped=true;reason="node_limit";}if(maxsolutions&&solutions>=maxsolutions){stopped=true;reason="solution_limit";}return stopped;}
// Necessary bounds: at most six distinct letters share a square row/column.
// Assigned components consume known-plaintext symbol frequencies. Any excess
// above the received coordinate histogram costs an error or an erased slot.
bool local_possible(const Candidate&a){
 int rc[6]={},cc[6]={},w[6]={},excess=0;
 for(int t=0;t<a.n;t++){int l=a.letter[t],r=a.row[t],c=a.col[t];if(r>=0){rc[r]++;w[r]+=symbol_count[l];}if(c>=0){cc[c]++;w[c]+=symbol_count[l];}}
 for(int c=0;c<6;c++){if(rc[c]>6||cc[c]>6)return false;excess+=max(0,w[c]-observed_count[c]);}
 return excess<=maximum_errors+source_masks;
}
bool compatible(const Candidate&a){
 int fresh[36],nf=0,dr[6]={},dc[6]={},dw[6]={};
 for(int t=0;t<a.n;t++){
  int l=a.letter[t],r=a.row[t],c=a.col[t];
  if(r>=0&&rmap[l]>=0&&r!=rmap[l])return false;
  if(c>=0&&cmap[l]>=0&&c!=cmap[l])return false;
  if(r>=0&&rmap[l]<0){dr[r]++;dw[r]+=symbol_count[l];}
  if(c>=0&&cmap[l]<0){dc[c]++;dw[c]+=symbol_count[l];}
  if(r<0)r=rmap[l];
  if(c<0)c=cmap[l];
  if(r>=0&&c>=0){int cell=6*r+c;if(owner[cell]>=0&&owner[cell]!=l)return false;for(int z=0;z<nf;z++)if(fresh[z]==cell)return false;fresh[nf++]=cell;}
 }
 int excess=0;for(int c=0;c<6;c++){if(row_count[c]+dr[c]>6||col_count[c]+dc[c]>6)return false;excess+=max(0,weight[c]+dw[c]-observed_count[c]);}
 return excess<=maximum_errors+source_masks;
}
// Generate bindings for the next transmitted chunk if it belongs to physical
// column phys and exactly d valid coordinates in that chunk are ignored.
// Equal bindings with different ignored masks are equivalent for existence;
// keep one mask as a concrete witness, not an exhaustive error-mask listing.
void generate(int phys,int pos,int d){
 generations++;
 auto&out=cache[phys][pos][d];out.clear();epoch[phys][pos][d]=current_epoch;
 if(pos+height[phys]>m)return;
 int rows[36],cols[36],owned[36];fill(rows,rows+36,-1);fill(cols,cols+36,-1);fill(owned,owned+36,-1);
 unordered_set<string>seen;
 auto rec=[&](auto&&self,int row,int used,int ignored_count,uint64_t ignored_mask)->void{
  if(stopped)return;
  local_recursion_nodes++;
  if((local_recursion_nodes&4095)==0&&limited())return;
  if(row==height[phys]){
   if(ignored_count!=d)return;
   string sig;sig.reserve(72);for(int l=0;l<36;l++){sig.push_back(char(rows[l]+1));sig.push_back(char(cols[l]+1));}
   if(!seen.insert(sig).second)return;
   Candidate a;a.ignored_mask=ignored_mask;a.n=0;for(int l=0;l<36;l++)if(rows[l]>=0||cols[l]>=0){int t=a.n++;a.letter[t]=l;a.row[t]=rows[l];a.col[t]=cols[l];}if(!local_possible(a))return;out.push_back(a);localvariants++;return;
  }
  if(ignored_count<d&&encoded[pos+used]>=0)self(self,row+1,used+1,ignored_count+1,ignored_mask|(1ULL<<row));
  if(height[phys]-row<=d-ignored_count)return;
  int l=spec[phys][row],value=encoded[pos+used];
  if(l<0||value<0){self(self,row+1,used+1,ignored_count,ignored_mask);return;}
  int&var=component[phys][row]?cols[l]:rows[l],old=var;
  if(old>=0&&old!=value)return;
  var=value;int cell=rows[l]>=0&&cols[l]>=0?6*rows[l]+cols[l]:-1;
  if(cell>=0&&owned[cell]>=0&&owned[cell]!=l){var=old;return;}
  int prior=cell>=0?owned[cell]:-1;if(cell>=0)owned[cell]=l;
  self(self,row+1,used+1,ignored_count,ignored_mask);
  if(cell>=0)owned[cell]=prior;
  var=old;
 };
 rec(rec,0,0,0,0);
}
// A full bipartite matching supplies one bijective square completion. Free
// cells are arithmetic witnesses and carry no recovered-text interpretation.
bool augment(int l,int*own,bool*seen){
 for(int cell=0;cell<36;cell++)if((rmap[l]<0||rmap[l]==cell/6)&&(cmap[l]<0||cmap[l]==cell%6)&&!seen[cell]){seen[cell]=true;if(own[cell]<0||augment(own[cell],own,seen)){own[cell]=l;return true;}}
 return false;
}
void record(){
 int own[36];fill(own,own+36,-1);for(int l=0;l<36;l++){bool seen[36]={};if(!augment(l,own,seen))return;}
 string square(36,'?');for(int c=0;c<36;c++)square[c]=ABC[own[c]];
 int offsets[MAXK],pos=0;vector<int>ignored;bool ignored_at[MAXN]={};
 for(int rank=0;rank<k;rank++)for(int phys=0;phys<k;phys++)if(chosen[phys]==rank){offsets[phys]=pos;for(int row=0;row<height[phys];row++,pos++)if(chosen_ignored_mask[phys]>>row&1ULL){ignored.push_back(pos);ignored_at[pos]=true;}}
 if(pos!=n||(int)ignored.size()>maximum_errors)abort();
 string text=cur->text,filled=source,partial(36,'?');for(int l=0;l<36;l++)if(rmap[l]>=0&&cmap[l]>=0)partial[6*rmap[l]+cmap[l]]=ABC[l];
 for(int i=0;i<n/2;i++){
  int a=offsets[(2*i)%k]+(2*i)/k,b=offsets[(2*i+1)%k]+(2*i+1)/k,cell;
  if(text[i]!='?')cell=square.find(text[i]);else{int r=encoded[a],c=encoded[b];cell=6*(r<0||ignored_at[a]?0:r)+(c<0||ignored_at[b]?0:c);text[i]=square[cell];}
  if(encoded[a]>=0&&!ignored_at[a]&&encoded[a]!=cell/6)abort();
  if(encoded[b]>=0&&!ignored_at[b]&&encoded[b]!=cell%6)abort();
  filled[a]=CO[cell/6];filled[b]=CO[cell%6];
 }
 vector<int>edits;for(int i=0;i<n;i++)if(encoded[i]>=0&&source[i]!=filled[i])edits.push_back(i);if((int)edits.size()>maximum_errors)abort();
 solutions++;
 cout<<"{\"kind\":\"solution\",\"crib_id\":\""<<cur->id<<"\",\"width\":"<<k<<",\"ranks\":[";
 for(int c=0;c<k;c++)cout<<(c?",":"")<<chosen[c]+1;
 cout<<"],\"square\":\""<<square<<"\",\"partial_square\":\""<<partial<<"\",\"plaintext\":\""<<text<<"\",\"filled_source\":\""<<filled<<"\",\"ignored_source_indices\":[";
 for(int i=0;i<(int)ignored.size();i++)cout<<(i?",":"")<<ignored[i];
 cout<<"],\"actual_observed_substitutions\":"<<edits.size()<<",\"edits\":[";
 for(int i=0;i<(int)edits.size();i++){int j=edits[i];cout<<(i?",":"")<<"["<<j<<",\""<<source[j]<<"\",\""<<filled[j]<<"\"]";}
 cout<<"]}"<<endl;limited();
}
// The next transmitted chunk can be any unused physical column. Its known
// height fixes the next source offset. This enumerates all length layouts and
// all column permutations without requiring a separately seeded rank order.
void walk(int rank,int pos,int used_errors,uint32_t used){
 if(stopped)return;
 nodes++;
 if((nodes&4095)==0&&limited())return;
 if(rank==k){if(pos!=m||used_errors>maximum_errors)abort();record();return;}
 for(int phys=0;phys<k;phys++)if(!(used>>phys&1U))for(int d=0;d<=maximum_errors-used_errors&&d<=height[phys];d++){
  if(pos+height[phys]>m)continue;
  if(epoch[phys][pos][d]!=current_epoch)generate(phys,pos,d);
  if(stopped)return;
  for(const Candidate&a:cache[phys][pos][d]){
   if(!compatible(a))continue;
   signed char oldr[36],oldc[36];for(int t=0;t<a.n;t++){int l=a.letter[t];oldr[t]=rmap[l];oldc[t]=cmap[l];if(a.row[t]>=0)rmap[l]=a.row[t];if(a.col[t]>=0)cmap[l]=a.col[t];if(oldr[t]<0&&rmap[l]>=0){row_count[rmap[l]]++;weight[rmap[l]]+=symbol_count[l];}if(oldc[t]<0&&cmap[l]>=0){col_count[cmap[l]]++;weight[cmap[l]]+=symbol_count[l];}if(rmap[l]>=0&&cmap[l]>=0)owner[6*rmap[l]+cmap[l]]=l;}
   chosen[phys]=rank;chosen_ignored_mask[phys]=a.ignored_mask;
   walk(rank+1,pos+height[phys],used_errors+d,used|(1U<<phys));
   for(int t=0;t<a.n;t++){int l=a.letter[t];if((oldr[t]<0||oldc[t]<0)&&rmap[l]>=0&&cmap[l]>=0)owner[6*rmap[l]+cmap[l]]=-1;if(oldr[t]<0&&rmap[l]>=0){row_count[rmap[l]]--;weight[rmap[l]]-=symbol_count[l];}if(oldc[t]<0&&cmap[l]>=0){col_count[cmap[l]]--;weight[cmap[l]]-=symbol_count[l];}rmap[l]=oldr[t];cmap[l]=oldc[t];}
   if(stopped)return;
  }
 }
}
void project(Crib&d){
 cur=&d;projects++;fill(row_count,row_count+6,0);fill(col_count,col_count+6,0);fill(weight,weight+6,0);fill(symbol_count,symbol_count+36,0);for(char c:d.text){auto x=ABC.find(c);if(x!=string::npos)symbol_count[x]++;}current_epoch++;
 fill(rmap,rmap+36,-1);fill(cmap,cmap+36,-1);fill(owner,owner+36,-1);
 for(int phys=0;phys<k;phys++)for(int row=0;row<height[phys];row++){int at=row*k+phys;auto l=ABC.find(d.text[at/2]);spec[phys][row]=l==string::npos?-1:l;component[phys][row]=at%2;}
 walk(0,0,0,0);
 if(!stopped)completed_projects++;
 if(projects%1000==0)cerr<<"progress "<<projects<<" seconds "<<seconds()<<" nodes "<<nodes<<endl;
}
int main(int argc, char** argv) {
    if (argc < 5 || argc > 8) {
        cerr << "Usage: substitution_crib SOURCE POOL WIDTH MAX_ERRORS [SECONDS [NODES [SOLUTIONS]]]\n";
        return 2;
    }
    auto unsigned_argument = [](const char* argument) -> uint64_t {
        string value(argument);
        if (value.empty() || value.find_first_not_of("0123456789") != string::npos)
            throw invalid_argument("Expected an unsigned integer");
        return stoull(value);
    };
    try {
        uint64_t width = unsigned_argument(argv[3]);
        uint64_t budget = unsigned_argument(argv[4]);
        if (width < 2 || width > MAXK || budget > MAXERRORS)
            throw invalid_argument("Width or error budget outside supported limits");
        k = int(width);
        maximum_errors = int(budget);
        if (argc > 5) {
            size_t consumed = 0;
            string argument(argv[5]);
            maxseconds = stod(argument, &consumed);
            if (consumed != argument.size() || !isfinite(maxseconds) || maxseconds < 0)
                throw invalid_argument("Invalid wall-time budget");
        }
        if (argc > 6) maxnodes = unsigned_argument(argv[6]);
        if (argc > 7) maxsolutions = unsigned_argument(argv[7]);
    } catch (const exception& error) {
        cerr << "Invalid numeric argument: " << error.what() << '\n';
        return 2;
    }

    ifstream source_file(argv[1]);
    string extra;
    if (!(source_file >> source) || (source_file >> extra)
        || source.find_first_not_of(CO + "?") != string::npos) {
        cerr << "Source must be one unbroken string containing only ADFGVX or ?\n";
        return 2;
    }
    n = m = source.size();
    if (n == 0 || n % 2 || n > MAXN || n / k + (n % k > 0) > MAXR) {
        cerr << "Source length outside supported limits\n";
        return 2;
    }
    q = n / k;
    e = n % k;
    for (int j = 0; j < k; j++) height[j] = q + (j < e);
    for (int i = 0; i < m; i++) {
        auto coordinate = CO.find(source[i]);
        encoded[i] = coordinate == string::npos ? -1 : coordinate;
        if (encoded[i] < 0) source_masks++;
        else observed_count[encoded[i]]++;
    }

    ifstream pool_file(argv[2]);
    string line;
    while (getline(pool_file, line)) {
        if (line.find_first_not_of(" \t\r") == string::npos) continue;
        istringstream row(line);
        string id, plaintext;
        if (!(row >> id >> plaintext) || (row >> extra)
            || int(plaintext.size()) != n / 2
            || plaintext.find_first_not_of(ABC + "?") != string::npos
            || id.find_first_not_of("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-") != string::npos) {
            cerr << "Invalid crib row\n";
            return 2;
        }
        donors.push_back({id, plaintext});
    }
    if (donors.empty()) {
        cerr << "No crib rows supplied\n";
        return 2;
    }

    began = chrono::steady_clock::now();
    for (Crib& crib : donors) {
        project(crib);
        if (limited()) break;
    }
    cout << "{\"kind\":\"summary\",\"width\":" << k
         << ",\"received_length\":" << m << ",\"full_length\":" << n
         << ",\"maximum_observed_substitutions\":" << maximum_errors
         << ",\"donors\":" << donors.size()
         << ",\"complete\":" << (stopped ? "false" : "true")
         << ",\"stop_reason\":\"" << reason
         << "\",\"projects\":" << projects
         << ",\"completed_projects\":" << completed_projects
         << ",\"local_generations\":" << generations
         << ",\"local_variants\":" << localvariants
         << ",\"search_nodes\":" << nodes
         << ",\"solutions\":" << solutions
         << ",\"seconds\":" << seconds() << "}" << endl;
}
