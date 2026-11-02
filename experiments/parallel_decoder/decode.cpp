/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
 * Exact top-K Markov decoding with an integer excess-observation-cost budget.
 * State: (last order symbols, exact cost used); keep K best prefixes per state.
 * The fixed alphabet is A..Z0..9. Ties use ordinary ASCII lexical order.
 */
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

static constexpr const char* alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static constexpr std::int64_t scale = 1LL << 24;

struct Entry { std::int64_t score; std::string text; };
using Bucket = std::vector<Entry>;

static bool better(const Entry& a, const Entry& b) {
    return a.score != b.score ? a.score > b.score : a.text < b.text;
}

static void retain(Bucket& bucket, std::int64_t score, const std::string& prefix,
                   char letter, int top_k) {
    if (static_cast<int>(bucket.size()) == top_k && score < bucket.back().score) return;
    Entry candidate{score, prefix + letter};
    if (static_cast<int>(bucket.size()) == top_k && !better(candidate, bucket.back())) return;
    auto where = std::lower_bound(bucket.begin(), bucket.end(), candidate, better);
    bucket.insert(where, std::move(candidate));
    if (static_cast<int>(bucket.size()) > top_k) bucket.pop_back();
}

static std::int64_t integer_log(float value) {
    const double exact = static_cast<double>(value) * static_cast<double>(scale);
    if (!std::isfinite(exact) || std::trunc(exact) != exact)
        throw std::runtime_error("A model float is not exact at the declared integer scale");
    return static_cast<std::int64_t>(exact);
}

static std::vector<char> read_file(const std::string& path) {
    std::ifstream in(path, std::ios::binary | std::ios::ate);
    if (!in) throw std::runtime_error("Cannot open model file");
    const auto size = in.tellg();
    if (size < 0) throw std::runtime_error("Cannot determine model file size");
    in.seekg(0);
    std::vector<char> data(static_cast<std::size_t>(size));
    if (!in.read(data.data(), size)) throw std::runtime_error("Cannot read model file");
    return data;
}

template <typename T>
static T at(const std::vector<char>& data, std::size_t offset) {
    T value;
    if (offset + sizeof(T) > data.size()) throw std::runtime_error("Truncated model file");
    std::memcpy(&value, data.data() + offset, sizeof(T));
    return value;
}

struct Tables {
    std::vector<std::int64_t> quad, six_values;
    std::vector<std::uint32_t> six_keys;
    std::uint32_t mask = 0;
    std::int64_t floor = 0;

    Tables(const std::string& quad_path, const std::string& six_path) {
        const std::uint32_t endian_test = 1;
        if (*reinterpret_cast<const char*>(&endian_test) != 1)
            throw std::runtime_error("This model loader requires little endian");
        auto bytes = read_file(quad_path);
        const std::size_t count4 = 36U * 36U * 36U * 36U;
        if (bytes.size() != count4 * sizeof(float)) throw std::runtime_error("Wrong quad table size");
        quad.reserve(count4);
        for (std::size_t i = 0; i < count4; ++i) quad.push_back(integer_log(at<float>(bytes, 4 * i)));
        bytes = read_file(six_path);
        if (bytes.size() < 20 || std::memcmp(bytes.data(), "G6HASH2\0", 8) != 0)
            throw std::runtime_error("Wrong sixgram magic");
        const auto size = at<std::uint32_t>(bytes, 8);
        if (!size || (size & (size - 1)) || bytes.size() != 20ULL + 8ULL * size)
            throw std::runtime_error("Wrong sixgram table size");
        mask = size - 1;
        floor = integer_log(at<float>(bytes, 16));
        six_keys.resize(size); six_values.resize(size);
        for (std::uint32_t i = 0; i < size; ++i) {
            six_keys[i] = at<std::uint32_t>(bytes, 20ULL + 4ULL * i);
            six_values[i] = integer_log(at<float>(bytes, 20ULL + 4ULL * size + 4ULL * i));
        }
    }

    std::int64_t six(std::uint32_t code) const {
        const std::uint32_t key = code + 1;
        std::uint32_t hash = (key ^ (key >> 16)) * 0x7FEB352DU;
        hash = (hash ^ (hash >> 15)) * 0x846CA68BU;
        hash ^= hash >> 16;
        std::uint32_t slot = hash & mask;
        while (six_keys[slot]) {
            if (six_keys[slot] == key) return six_values[slot];
            slot = (slot + 1) & mask;
        }
        return floor;
    }
};

int main(int argc, char** argv) {
    try {
        if (argc != 5) throw std::runtime_error("Usage: decode costs.txt quad.bin six.bin output.json");
        std::ifstream input(argv[1]);
        int length, max_budget, top_k, order;
        std::int64_t coefficient4, coefficient6;
        std::size_t max_states;
        if (!(input >> length >> max_budget >> top_k >> order >> coefficient4 >> coefficient6 >> max_states))
            throw std::runtime_error("Invalid cost header");
        if (length < 1 || length > 10000 || max_budget < 0 || max_budget > 100 || top_k < 1 || top_k > 100
            || (order != 3 && order != 5) || coefficient4 < 0 || coefficient6 < 0
            || (coefficient6 && order != 5) || !max_states)
            throw std::runtime_error("Unsupported decoding parameters");
        std::vector<std::array<int, 36>> costs(length);
        for (auto& row : costs) for (auto& value : row) {
            if (!(input >> value) || value < 0) throw std::runtime_error("Invalid symbol cost");
        }
        Tables tables(argv[2], argv[3]);
        std::uint32_t suffix_modulus = 1;
        for (int i = 0; i < order; ++i) suffix_modulus *= 36;
        const auto budget_width = static_cast<std::uint64_t>(max_budget + 1);
        std::unordered_map<std::uint64_t, Bucket> states;
        states.emplace(0, Bucket{{0, ""}});
        std::vector<std::size_t> layer_states;
        std::uint64_t extensions = 0;
        std::size_t peak = 1;

        for (int position = 0; position < length; ++position) {
            std::unordered_map<std::uint64_t, Bucket> next;
            next.reserve(std::min(max_states, states.size() * 3 + 64));
            for (const auto& state : states) {
                const auto suffix = static_cast<std::uint32_t>(state.first / budget_width);
                const auto used = static_cast<int>(state.first % budget_width);
                for (int symbol = 0; symbol < 36; ++symbol) {
                    const int cost = used + costs[position][symbol];
                    if (cost > max_budget) continue;
                    const auto combined = suffix * 36U + static_cast<std::uint32_t>(symbol);
                    const auto next_suffix = combined % suffix_modulus;
                    const auto state_key = static_cast<std::uint64_t>(next_suffix) * budget_width + cost;
                    std::int64_t delta = 0;
                    if (position >= 3 && coefficient4)
                        delta += coefficient4 * tables.quad[combined % (36U * 36U * 36U * 36U)];
                    if (position >= 5 && coefficient6) delta += coefficient6 * tables.six(combined);
                    auto& bucket = next[state_key];
                    extensions += state.second.size();
                    for (const auto& entry : state.second)
                        retain(bucket, entry.score + delta, entry.text, alphabet[symbol], top_k);
                }
            }
            if (next.size() > max_states)
                throw std::runtime_error("Exact state cap exceeded; no beam pruning or result was produced");
            states = std::move(next);
            layer_states.push_back(states.size());
            peak = std::max(peak, states.size());
            if ((position + 1) % 10 == 0 || position + 1 == length)
                std::cerr << "position " << position + 1 << "/" << length << ": " << states.size() << " exact states\n";
        }
        std::vector<Bucket> by_budget(max_budget + 1);
        for (const auto& state : states) {
            auto& bucket = by_budget[state.first % budget_width];
            bucket.insert(bucket.end(), state.second.begin(), state.second.end());
        }
        std::ofstream output(argv[4]);
        if (!output) throw std::runtime_error("Cannot open output");
        output << "{\n  \"length\": " << length << ", \"max_budget\": " << max_budget
               << ", \"top_k\": " << top_k << ", \"order\": " << order
               << ",\n  \"integer_log_scale\": " << scale << ", \"coefficient4\": " << coefficient4
               << ", \"coefficient6\": " << coefficient6 << ",\n  \"peak_suffix_budget_states\": " << peak
               << ", \"candidate_path_extensions\": " << extensions << ",\n  \"layer_states\": [";
        for (std::size_t i = 0; i < layer_states.size(); ++i) output << (i ? "," : "") << layer_states[i];
        output << "],\n  \"by_exact_excess_budget\": [\n";
        for (int budget = 0; budget <= max_budget; ++budget) {
            auto& bucket = by_budget[budget];
            std::sort(bucket.begin(), bucket.end(), better);
            if (static_cast<int>(bucket.size()) > top_k) bucket.resize(top_k);
            output << (budget ? ",\n" : "") << "    {\"budget\":" << budget << ",\"candidates\":[";
            for (std::size_t rank = 0; rank < bucket.size(); ++rank) {
                if (rank) output << ",";
                output << "{\"rank\":" << rank + 1 << ",\"score\":" << bucket[rank].score
                       << ",\"plaintext\":\"" << bucket[rank].text << "\"}";
            }
            output << "]}";
        }
        output << "\n  ]\n}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
    return 0;
}
