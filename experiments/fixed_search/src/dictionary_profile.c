/* Score dictionary-derived column orders without assuming any square.
 * Usage: dictionary_profile PROFILE WORDS INPUT
 * INPUT is nmsg followed by one ADFGVX/? string per message.
 * Output TSV: width, profile score, combined IC score, keyword.
 * Repeated keyword letters are ranked from left to right.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXK 40
#define MAXM 8
#define MAXN 4096
static int nmsg, ns[MAXM], ct[MAXM][MAXN];
static double mu[37], variance[37];

static void score(const int *perm, int k, double *profile, double *combined_ic) {
    int count[36]={0}, pairs[1296]={0}, nt=0, nd=0;
    for(int m=0;m<nmsg;m++) {
        int n=ns[m], q=n/k, e=n%k, offset[MAXK], pos=0, text[MAXN];
        for(int i=0;i<k;i++){int col=perm[i];offset[col]=pos;pos+=q+(col<e);}
        for(int i=0;i<n/2;i++) {
            int x=2*i, y=x+1;
            int a=ct[m][offset[x%k]+x/k], b=ct[m][offset[y%k]+y/k];
            int z=(a<0||b<0)?-1:6*a+b;text[i]=z;
            if(z>=0){count[z]++;nt++;}
        }
        for(int i=0;i+1<n/2;i++)if(text[i]>=0&&text[i+1]>=0){pairs[36*text[i]+text[i+1]]++;nd++;}
    }
    double ic1=0,ic2=0;
    for(int i=0;i<36;i++)ic1+=count[i]*(count[i]-1.0);
    for(int i=0;i<1296;i++)ic2+=pairs[i]*(pairs[i]-1.0);
    ic1/=nt*(nt-1.0);ic2/=nd*(nd-1.0);
    *combined_ic=10000*(ic1+2*ic2);
    for(int i=1;i<36;i++){int v=count[i],j=i;while(j&&count[j-1]<v){count[j]=count[j-1];j--;}count[j]=v;}
    double value=0,reg=.25/(nt*nt);
    for(int i=0;i<36;i++){double d=(double)count[i]/nt-mu[i];value-=d*d/(variance[i]+reg);}
    double d=ic2-mu[36];value-=d*d/variance[36];*profile=value;
}

int main(int argc,char**argv) {
    if(argc!=4)return 2;
    FILE *p=fopen(argv[1],"r"),*words=fopen(argv[2],"r"),*input=fopen(argv[3],"r");
    if(!p||!words||!input)return 2;
    for(int i=0;i<37;i++)if(fscanf(p,"%lf%lf",mu+i,variance+i)!=2)return 2;
    fclose(p);
    if(fscanf(input,"%d",&nmsg)!=1||nmsg<1||nmsg>MAXM)return 2;
    char buf[MAXN];
    for(int m=0;m<nmsg;m++) {
        if(fscanf(input,"%4095s",buf)!=1)return 2;
        ns[m]=strlen(buf);if(ns[m]%2||ns[m]<8)return 2;
        for(int i=0;i<ns[m];i++){char*z=strchr("ADFGVX",buf[i]);ct[m][i]=z?(int)(z-"ADFGVX"):-1;}
    }
    fclose(input);setvbuf(stdout,NULL,_IOFBF,1<<20);
    char word[1024];unsigned long scanned=0;
    while(fscanf(words,"%1023s",word)==1) {
        int k=strlen(word);if(k<8||k>32)continue;
        int perm[MAXK],n=0;
        for(char c='A';c<='Z';c++)for(int j=0;j<k;j++)if(word[j]==c)perm[n++]=j;
        if(n!=k)continue;
        double profile,ic;score(perm,k,&profile,&ic);
        printf("%d\t%.9f\t%.9f\t%s\n",k,profile,ic,word);scanned++;
    }
    fclose(words);fprintf(stderr,"Scored %lu keyword occurrences.\n",scanned);return 0;
}
