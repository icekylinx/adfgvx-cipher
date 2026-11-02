// Read-only word-objective harness; icekylinx and GPT-6 Astra Pro.
// Include the archived engine without invoking its stochastic search.
#define main archived_search_main
#include "../../p198_word_search/word_loss.cpp"
#undef main
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    load_lexicon(argv[1]);
    string text;
    while (getline(cin, text)) {
        vector<int> plaintext;
        for (char c : text) {
            auto position = AL.find(c);
            if (position == string::npos) return 3;
            plaintext.push_back(position);
        }
        cout << setprecision(17) << lexscore(plaintext) << "\n";
    }
}
