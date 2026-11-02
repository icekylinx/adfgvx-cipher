/* Sparse independent German six-gram model. See models/german36_sixgram.json.
 * Header-only reader: call g6_load(path), then g6_lookup(base36_code).
 * A six-character code is (((((a*36+b)*36+c)*36+d)*36+e)*36+f), a..f=0..35.
 * Returns base-10 log probability; this is a heuristic language model.
 */
#ifndef ADFGVX_SIXGRAM_MODEL_H
#define ADFGVX_SIXGRAM_MODEL_H
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static uint32_t *g6_keys, g6_size, g6_mask;
static float *g6_values, g6_floor;
static int g6_load(const char *path) {
    FILE *stream = fopen(path, "rb");
    char magic[8]; uint32_t count;
    if (!stream) return 0;
    if (fread(magic, 1, 8, stream) != 8 || memcmp(magic, "G6HASH2\0", 8) ||
        fread(&g6_size, 4, 1, stream) != 1 || fread(&count, 4, 1, stream) != 1 ||
        fread(&g6_floor, 4, 1, stream) != 1 || !g6_size ||
        (g6_size & (g6_size - 1))) { fclose(stream); return 0; }
    g6_mask = g6_size - 1;
    g6_keys = malloc((size_t)g6_size * 4);
    g6_values = malloc((size_t)g6_size * 4);
    if (!g6_keys || !g6_values ||
        fread(g6_keys, 4, g6_size, stream) != g6_size ||
        fread(g6_values, 4, g6_size, stream) != g6_size) {
        fclose(stream); free(g6_keys); free(g6_values); return 0;
    }
    fclose(stream); return 1;
}
static inline float g6_lookup(uint32_t code) {
    uint32_t key = code + 1, h = key;
    h = (h ^ (h >> 16)) * 0x7feb352dU;
    h = (h ^ (h >> 15)) * 0x846ca68bU;
    h ^= h >> 16;
    uint32_t slot = h & g6_mask;
    while (g6_keys[slot]) {
        if (g6_keys[slot] == key) return g6_values[slot];
        slot = (slot + 1) & g6_mask;
    }
    return g6_floor;
}
#endif
