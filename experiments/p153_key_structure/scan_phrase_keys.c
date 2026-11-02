/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
 * Exact stable-rank matching against every contiguous normalized text window.
 * Input argv[1]: target count, then ID, width, and one-based ranks per target.
 * Other arguments: files containing only uppercase A-Z, without a newline.
 * No plaintext model or candidate score is used.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define MAX_TARGETS 64
#define MAX_WIDTH 64

typedef struct {
    char id[128];
    int width;
    int order[MAX_WIDTH];
    unsigned long long windows, matches;
} Target;

int main(int argc, char **argv) {
    if (argc < 3) return 2;
    FILE *input = fopen(argv[1], "r");
    int count;
    Target targets[MAX_TARGETS] = {0};
    if (!input || fscanf(input, "%d", &count) != 1 || count < 1 || count > MAX_TARGETS) return 2;
    for (int t = 0; t < count; ++t) {
        Target *target = &targets[t];
        int seen[MAX_WIDTH] = {0};
        if (fscanf(input, "%127s%d", target->id, &target->width) != 2 || target->width < 2 || target->width > MAX_WIDTH) return 2;
        for (int i = 0; i < target->width; ++i) {
            int rank;
            if (fscanf(input, "%d", &rank) != 1 || rank < 1 || rank > target->width || seen[rank-1]++) return 2;
            target->order[rank-1] = i;
        }
    }
    fclose(input);
    for (int f = 2; f < argc; ++f) {
        FILE *text = fopen(argv[f], "rb");
        if (!text || fseek(text, 0, SEEK_END) != 0) return 3;
        long length = ftell(text);
        if (length < 0 || fseek(text, 0, SEEK_SET) != 0) return 3;
        char *data = malloc((size_t)length + 1);
        if (!data || fread(data, 1, (size_t)length, text) != (size_t)length) return 3;
        fclose(text);
        for (long i = 0; i < length; ++i) if (data[i] < 'A' || data[i] > 'Z') return 4;
        for (int t = 0; t < count; ++t) {
            Target *target = &targets[t];
            if (length < target->width) continue;
            target->windows += (unsigned long long)(length - target->width + 1);
            for (long pos = 0; pos <= length - target->width; ++pos) {
                int good = 1;
                for (int j = 1; j < target->width; ++j) {
                    int a = target->order[j-1], b = target->order[j];
                    char ca = data[pos+a], cb = data[pos+b];
                    if (ca > cb || (ca == cb && a > b)) { good = 0; break; }
                }
                if (good) {
                    char word[MAX_WIDTH+1];
                    memcpy(word, data+pos, (size_t)target->width);
                    word[target->width] = '\0';
                    ++target->matches;
                    const char *name = strrchr(argv[f], '/');
                    name = name ? name+1 : argv[f];
                    printf("{\"type\":\"match\",\"target\":\"%s\",\"file\":\"%s\",\"offset\":%ld,\"word\":\"%s\"}\n", target->id, name, pos, word);
                }
            }
        }
        free(data);
    }
    for (int t = 0; t < count; ++t)
        printf("{\"type\":\"summary\",\"target\":\"%s\",\"width\":%d,\"windows\":%llu,\"matches\":%llu}\n", targets[t].id, targets[t].width, targets[t].windows, targets[t].matches);
    return 0;
}
