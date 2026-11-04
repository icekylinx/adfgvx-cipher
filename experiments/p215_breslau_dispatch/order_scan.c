#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define N 392
#define G 79
#define QN 5764801
static float q[QN];
static int ranks[22],tx_to_iv[N];
static double best=-1e300;
static long long evals=0,ties=0;
static int tieops[1000][5],ntie=0;
static const char C[]="ADFGVX";
static int glyph(char c){const char *p=strchr(C,c);return p?(int)(p-C):6;}
static double score(const int *frame,const int *order){
 int iv[N],pat[196],out=0;
 for(int g=0;g<G;g++){int id=order[g],len=id==78?2:5;for(int j=0;j<len;j++)iv[tx_to_iv[out++]]=frame[id*5+j];}
 if(out!=N)exit(4);
 for(int i=0;i<196;i++)pat[i]=iv[2*i]*7+iv[2*i+1];
 double z=0;for(int i=0;i<193;i++)z+=q[((pat[i]*49+pat[i+1])*49+pat[i+2])*49+pat[i+3]];
 return z;
}
static void record(const int *f,const int *o,int fi,int kind,int a,int b){
 double z=score(f,o);evals++;
 if(z>best+1e-7){best=z;ties=0;ntie=0;}
 if(fabs(z-best)<1e-7){ties++;if(ntie<1000){int *t=tieops[ntie++];t[0]=fi;t[1]=kind;t[2]=a;t[3]=b;t[4]=0;}}
}
int main(int argc,char**argv){
 if(argc!=3){fprintf(stderr,"model frames\n");return 2;}
 FILE *fp=fopen(argv[1],"rb");if(!fp)return 2;if(fread(q,4,QN,fp)!=QN)return 2;fclose(fp);
 fp=fopen(argv[2],"r");if(!fp)return 2;int nf;if(fscanf(fp,"%d",&nf)!=1)return 2;
 for(int c=0;c<22;c++)if(fscanf(fp,"%d",&ranks[c])!=1)return 2;
 int cur=0;for(int k=1;k<=22;k++)for(int c=0;c<22;c++)if(ranks[c]==k)for(int p=c;p<N;p+=22)tx_to_iv[cur++]=p;
 if(cur!=N)return 3;
 for(int fi=0;fi<nf;fi++){
  int a,b;if(fscanf(fp,"%d %d",&a,&b)!=2)return 2;char s[400];if(fscanf(fp,"%399s",s)!=1||strlen(s)!=N)return 2;
  int f[N],o[G];for(int i=0;i<N;i++)f[i]=glyph(s[i]);for(int i=0;i<G;i++)o[i]=i;
  record(f,o,fi,0,-1,-1);
  for(int i=0;i<78;i++)for(int j=i+1;j<78;j++){
   for(int k=0;k<G;k++)o[k]=k;o[i]=j;o[j]=i;record(f,o,fi,1,i,j);
  }
  for(int i=0;i<78;i++)for(int j=0;j<78;j++)if(i!=j){
   int left[G],t=0;for(int k=0;k<G;k++)if(k!=i)left[t++]=k;
   t=0;for(int k=0;k<G;k++)o[k]=k==j?i:left[t++];record(f,o,fi,2,i,j);
  }
 }
 fclose(fp);
 printf("{\"evaluations\":%lld,\"best_score\":%.17g,\"tie_descriptions\":%lld,\"stored_ties\":%d,\"ops\":[",evals,best,ties,ntie);
 for(int i=0;i<ntie;i++){if(i)printf(",");printf("[%d,%d,%d,%d]",tieops[i][0],tieops[i][1],tieops[i][2],tieops[i][3]);}printf("]}\n");return 0;
}
