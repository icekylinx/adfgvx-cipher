/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
 * Exact joint scattered-coordinate-loss placement and missing-value decoding.
 * Objective: exact integer combinations of the original four- and six-gram logs.
 * Missing coordinate values are explicit model hypotheses, not source readings.
 */
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

static constexpr const char* alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
static constexpr const char* coordinates = "ADFGVX";
static constexpr std::uint32_t suffix_modulus = 36U * 36U * 36U * 36U * 36U;
static constexpr std::uint32_t quad_modulus = 36U * 36U * 36U * 36U;
static constexpr std::int64_t score_scale = 1LL << 24;

template <typename T> static T read_value(std::istream& in) {
    T value;
    if (!in.read(reinterpret_cast<char*>(&value), sizeof(T))) throw std::runtime_error("Truncated input");
    return value;
}

template <typename T> static void write_value(std::ostream& out, T value) {
    out.write(reinterpret_cast<const char*>(&value), sizeof(T));
}

static void check_square(const std::string& square) {
    std::string sorted = square, expected = alphabet;
    std::sort(sorted.begin(), sorted.end()); std::sort(expected.begin(), expected.end());
    if (sorted != expected) throw std::runtime_error("A complete bijective square is required");
}

struct LossMask {
    std::array<std::uint64_t, 4> words{};
    std::uint32_t fills = 0;
    void set(int position, int coordinate) {
        int rank = 0;
        for (int word = 0; word < position / 64; ++word) rank += __builtin_popcountll(words[word]);
        const auto before = (position % 64) ? ((1ULL << (position % 64)) - 1) : 0ULL;
        rank += __builtin_popcountll(words[position / 64] & before);
        const auto lower = rank ? ((1U << (3 * rank)) - 1) : 0U;
        fills = (fills & lower) | ((fills & ~lower) << 3) | (static_cast<std::uint32_t>(coordinate) << (3 * rank));
        words[position / 64] |= 1ULL << (position % 64);
    }
};

// For masks of equal cardinality, the lower first differing loss position wins.
// Then compare inserted coordinates in increasing loss-position order.
// Adding the same future positions and values preserves this ordering.
static bool earlier_mask(const LossMask& a, const LossMask& b) {
    for (std::size_t i = 0; i < a.words.size(); ++i) {
        const auto difference = a.words[i] ^ b.words[i];
        if (difference) {
            const auto lowest = difference & (~difference + 1);
            return (a.words[i] & lowest) != 0;
        }
    }
    for (int i = 0; i < 6; ++i) {
        const auto av = (a.fills >> (3 * i)) & 7U, bv = (b.fills >> (3 * i)) & 7U;
        if (av != bv) return av < bv;
    }
    return false;
}

struct Layer {
    std::unique_ptr<std::int64_t[]> score;
    std::unique_ptr<LossMask[]> masks;
    std::unique_ptr<std::uint32_t[]> stamps, keys;
    std::vector<std::uint32_t> active;
    std::uint32_t epoch = 0, hash_mask;
    std::size_t maximum_states;
    explicit Layer(std::size_t cap) : maximum_states(cap) {
        std::size_t size = 1;
        while (size < 2 * maximum_states) size <<= 1;
        if (size < 2 || size > (1U << 24)) throw std::runtime_error("Unsupported state hash capacity");
        hash_mask = static_cast<std::uint32_t>(size - 1);
        score.reset(new std::int64_t[size]); masks.reset(new LossMask[size]);
        stamps.reset(new std::uint32_t[size]{}); keys.reset(new std::uint32_t[size]);
        active.reserve(maximum_states);
    }
    void reset() { ++epoch; active.clear(); }
    void offer(std::uint32_t key, std::int64_t value, const LossMask& mask) {
        std::uint32_t h = (key ^ (key >> 16)) * 0x7FEB352DU;
        h = (h ^ (h >> 15)) * 0x846CA68BU;
        h ^= h >> 16;
        std::uint32_t slot = h & hash_mask;
        while (stamps[slot] == epoch && keys[slot] != key) slot = (slot + 1) & hash_mask;
        if (stamps[slot] != epoch) {
            if (active.size() >= maximum_states) throw std::runtime_error("Exact state cap exceeded; no pruning performed");
            stamps[slot] = epoch; keys[slot] = key; score[slot] = value; masks[slot] = mask; active.push_back(slot);
        } else if (value > score[slot] || (value == score[slot] && earlier_mask(mask, masks[slot]))) {
            score[slot] = value; masks[slot] = mask;
        }
    }
};

static std::int64_t integer_log(float value) {
    const double exact = static_cast<double>(value) * static_cast<double>(score_scale);
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

struct Search {
    int width, missing, total_length;
    std::uint64_t first_allocation, allocation_limit, ordinal = 0, completed = 0;
    std::size_t state_cap, maximum_states = 0;
    std::uint64_t state_visits = 0, transitions = 0;
    std::vector<int> ranks, readout, full_lengths, full_starts, allocation, weights, retained_starts, retained_lengths;
    std::vector<int> observed;
    std::string square;
    Tables tables;
    std::int64_t coefficient4, coefficient6;
    std::array<int, 36> cell_letters{};
    Layer layer_a, layer_b;
    bool has_best = false;
    std::int64_t best_score = std::numeric_limits<std::int64_t>::min();
    LossMask best_mask;
    std::vector<int> best_allocation;

    Search(int k, int loss_count, std::uint64_t first, std::uint64_t limit, std::size_t cap,
           std::vector<int> key, std::string sq, const std::string& ciphertext, const std::string& quad_path, const std::string& six_path,
           std::int64_t c4, std::int64_t c6)
        : width(k), missing(loss_count), total_length(static_cast<int>(ciphertext.size()) + loss_count),
          first_allocation(first), allocation_limit(limit), state_cap(cap), ranks(std::move(key)), square(std::move(sq)),
          tables(quad_path, six_path), coefficient4(c4), coefficient6(c6), layer_a(cap), layer_b(cap) {
        check_square(square);
        if (width % 2 || total_length % 2 || width < 2 || width > 32 || missing < 0 || missing > 6
            || total_length > 256 || total_length < width || ciphertext.empty())
            throw std::runtime_error("Unsupported exact-loss geometry");
        std::vector<int> sorted = ranks; std::sort(sorted.begin(), sorted.end());
        for (int i = 0; i < width; ++i) if (sorted[i] != i + 1) throw std::runtime_error("Invalid ranks");
        readout.resize(width); std::iota(readout.begin(), readout.end(), 0);
        std::sort(readout.begin(), readout.end(), [&](int a, int b) { return ranks[a] < ranks[b]; });
        full_lengths.resize(width); full_starts.resize(width); allocation.resize(width); weights.resize(width);
        retained_starts.resize(width); retained_lengths.resize(width);
        for (int c = 0; c < width; ++c) full_lengths[c] = total_length / width + (c < total_length % width);
        int start = 0;
        for (int column : readout) { full_starts[column] = start; start += full_lengths[column]; }
        for (char c : ciphertext) {
            const char* found = std::strchr(coordinates, c);
            if (!found) throw std::runtime_error("Unexpected source coordinate");
            observed.push_back(static_cast<int>(found - coordinates));
        }
        for (int cell = 0; cell < 36; ++cell)
            cell_letters[cell] = static_cast<int>(std::strchr(alphabet, square[cell]) - alphabet);
        if (coefficient4 < 0 || coefficient6 < 0 || (!coefficient4 && !coefficient6))
            throw std::runtime_error("Invalid score coefficients");
    }

    void one_allocation() {
        const auto current_ordinal = ordinal++;
        if (current_ordinal < first_allocation || (allocation_limit && completed >= allocation_limit)) return;
        int received_start = 0, combinations = 1;
        for (int c = 0; c < width; ++c) {
            weights[c] = combinations;
            combinations *= allocation[c] + 1;
        }
        for (int c : readout) {
            retained_starts[c] = received_start;
            retained_lengths[c] = full_lengths[c] - allocation[c];
            received_start += retained_lengths[c];
        }
        if (received_start != static_cast<int>(observed.size())) throw std::runtime_error("Wrong column partition");
        Layer* current = &layer_a; Layer* next = &layer_b;
        current->reset(); current->offer(0, 0, LossMask{});
        for (int position = 0; position < total_length / 2; ++position) {
            next->reset();
            const int left_column = (2 * position) % width, right_column = left_column + 1;
            const int row = (2 * position) / width;
            for (std::uint32_t slot : current->active) {
                const auto state = current->keys[slot];
                ++state_visits;
                const int used_code = static_cast<int>(state / suffix_modulus);
                const auto suffix = state % suffix_modulus;
                const int left_used = (used_code / weights[left_column]) % (allocation[left_column] + 1);
                const int right_used = (used_code / weights[right_column]) % (allocation[right_column] + 1);
                for (int left_loss = 0; left_loss < 2; ++left_loss) {
                    if (left_loss ? left_used == allocation[left_column]
                                  : row - left_used >= retained_lengths[left_column]) continue;
                    const int left = left_loss ? 6 : observed[retained_starts[left_column] + row - left_used];
                    for (int right_loss = 0; right_loss < 2; ++right_loss) {
                        if (right_loss ? right_used == allocation[right_column]
                                       : row - right_used >= retained_lengths[right_column]) continue;
                        const int right = right_loss ? 6 : observed[retained_starts[right_column] + row - right_used];
                        const int new_used = used_code + left_loss * weights[left_column] + right_loss * weights[right_column];
                        for (int first = (left_loss ? 0 : left); first <= (left_loss ? 5 : left); ++first) {
                            for (int second = (right_loss ? 0 : right); second <= (right_loss ? 5 : right); ++second) {
                                const int symbol = cell_letters[6 * first + second];
                                const auto combined = suffix * 36U + symbol;
                                const auto target = new_used * suffix_modulus + combined % suffix_modulus;
                                LossMask mask = current->masks[slot];
                                if (left_loss) mask.set(full_starts[left_column] + row, first);
                                if (right_loss) mask.set(full_starts[right_column] + row, second);
                                std::int64_t delta = 0;
                                if (position >= 3 && coefficient4) delta += coefficient4 * tables.quad[combined % quad_modulus];
                                if (position >= 5 && coefficient6) delta += coefficient6 * tables.six(combined);
                                const auto value = current->score[slot] + delta;
                                next->offer(target, value, mask);
                                ++transitions;
                            }
                        }
                    }
                }
            }
            if (next->active.size() > state_cap) throw std::runtime_error("Exact state cap exceeded; no pruning performed");
            maximum_states = std::max(maximum_states, next->active.size());
            std::swap(current, next);
        }
        for (std::uint32_t slot : current->active) {
                const auto state = current->keys[slot];
            if (state / suffix_modulus != static_cast<std::uint32_t>(combinations - 1))
                throw std::runtime_error("Final state did not consume every allocated loss");
            const auto value = current->score[slot];
            if (!has_best || value > best_score || (value == best_score && earlier_mask(current->masks[slot], best_mask))) {
                has_best = true; best_score = value; best_mask = current->masks[slot]; best_allocation = allocation;
            }
        }
        ++completed;
        if (completed % 1000 == 0)
            std::cerr << "allocations " << completed << ", best integer score " << best_score
                      << ", peak states " << maximum_states << "\n";
    }

    void enumerate(int readout_index, int remaining) {
        if (readout_index == width) {
            if (remaining == 0) one_allocation();
            return;
        }
        const int column = readout[readout_index];
        for (int count = 0; count <= std::min(remaining, full_lengths[column]); ++count) {
            allocation[column] = count;
            enumerate(readout_index + 1, remaining - count);
        }
    }

    void output(const std::string& path) const {
        if (!has_best) throw std::runtime_error("No allocation was searched");
        std::ofstream out(path);
        out << "{\n  \"nominal_coordinates\":" << total_length << ",\"observed_coordinates\":" << observed.size()
            << ",\"missing_coordinates\":" << missing << ",\"width\":" << width
            << ",\n  \"integer_log_scale\":" << score_scale << ",\"quad_windows\":" << total_length / 2 - 3
            << ",\"six_windows\":" << total_length / 2 - 5
            << ",\"coefficient4\":" << coefficient4 << ",\"coefficient6\":" << coefficient6
            << ",\"best_integer_score\":" << best_score
            << ",\n  \"allocation_count_total\":" << ordinal << ",\"allocation_start\":" << first_allocation
            << ",\"allocations_completed\":" << completed
            << ",\"all_allocations_completed\":" << (first_allocation == 0 && completed == ordinal ? "true" : "false")
            << ",\n  \"maximum_active_states\":" << maximum_states << ",\"state_visits\":" << state_visits
            << ",\"transitions_considered\":" << transitions
            << ",\n  \"missing_full_ciphertext_positions\":[";
        bool first = true;
        for (int i = 0; i < total_length; ++i) if (best_mask.words[i / 64] & (1ULL << (i % 64))) {
            out << (first ? "" : ",") << i; first = false;
        }
        out << "],\n  \"filled_missing_coordinates\":\"";
        for (int i = 0; i < missing; ++i) out << coordinates[(best_mask.fills >> (3 * i)) & 7U];
        out << "\",\n  \"losses_per_physical_column\":[";
        for (int c = 0; c < width; ++c) out << (c ? "," : "") << best_allocation[c];
        out << "]\n}\n";
    }
};

int main(int argc, char** argv) {
    try {
        const std::uint32_t endian_test = 1;
        if (*reinterpret_cast<const char*>(&endian_test) != 1) throw std::runtime_error("Little-endian host required");
        if (argc != 6 || std::string(argv[1]) != "solve")
            throw std::runtime_error("Usage: exact_joint_six solve config quad_model six_model output");
        std::ifstream input(argv[2]);
        int width, missing;
        std::uint64_t start, count;
        std::size_t cap;
        std::int64_t coefficient4, coefficient6;
        if (!(input >> width >> missing >> start >> count >> cap >> coefficient4 >> coefficient6) || width < 2 || width > 32 || missing < 0 || missing > 6)
            throw std::runtime_error("Invalid search header");
        std::string square, ciphertext;
        input >> square;
        std::vector<int> ranks(width);
        for (auto& rank : ranks) input >> rank;
        if (!(input >> ciphertext)) throw std::runtime_error("Missing ciphertext");
        Search search(width, missing, start, count, cap, ranks, square, ciphertext, argv[3], argv[4], coefficient4, coefficient6);
        search.enumerate(0, missing);
        search.output(argv[5]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
    return 0;
}
