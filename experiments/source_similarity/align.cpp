// ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
// Direct sequence retrieval only: no key or plaintext language model.
#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <utility>
#include <vector>

struct Metrics { int local, longest, fitting; };

Metrics compare(const std::string& a, const std::string& b) {
    const int n = a.size(), m = b.size(), neg = -1000000000;
    std::vector<int> h(m+1), next(m+1), e(m+1,neg);
    std::vector<int> run(m+1), run_next(m+1);
    std::vector<int> fit(m+1), fit_next(m+1);
    int best = 0, longest = 0;
    for (int i=1; i<=n; ++i) {
        next[0] = run_next[0] = 0;
        fit_next[0] = i;
        int f = neg;
        for (int j=1; j<=m; ++j) {
            const bool erased = a[i-1]=='?' || b[j-1]=='?';
            const bool equal = a[i-1]==b[j-1] && !erased;
            const int score = erased ? 0 : (equal ? 2 : -3);
            e[j] = std::max(h[j]-3, e[j]-1);
            f = std::max(next[j-1]-3, f-1);
            next[j] = std::max({0, h[j-1]+score, e[j], f});
            best = std::max(best, next[j]);
            run_next[j] = equal ? run[j-1]+1 : 0;
            longest = std::max(longest, run_next[j]);
            fit_next[j] = std::min({fit[j-1]+(erased||equal ? 0 : 1),
                                    fit[j]+1, fit_next[j-1]+1});
        }
        h.swap(next); run.swap(run_next); fit.swap(fit_next);
    }
    return {best,longest,*std::min_element(fit.begin(),fit.end())};
}

int main() {
    std::ios::sync_with_stdio(false);
    int nq,nb;
    if (!(std::cin >> nq)) return 1;
    std::vector<std::pair<std::string,std::string>> queries(nq);
    for(auto& q:queries) std::cin >> q.first >> q.second;
    std::cin >> nb;
    std::vector<std::pair<std::string,std::string>> blocks(nb);
    for(auto& b:blocks) std::cin >> b.first >> b.second;
    for(const auto& q:queries) for(const auto& b:blocks) {
        auto s=compare(q.second,b.second);
        std::cout << q.first << '\t' << b.first << '\t' << s.local << '\t'
                  << s.longest << '\t' << s.fitting << '\n';
    }
}
