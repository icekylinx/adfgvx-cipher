/* ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
 * Exact joint scattered-coordinate-loss placement and missing-value decoding.
 * Objective: sum of the original float32 quadgram log values, scaled exactly.
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
static constexpr std::uint32_t domain_count = 36;
static constexpr std::uint32_t suffix_modulus = 36U * 36U * 36U;
static constexpr std::uint32_t table_size = suffix_modulus * 36U;
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
    std::unique_ptr<std::uint32_t[]> stamps;
    std::vector<std::uint32_t> active;
    std::uint32_t epoch = 0;
    explicit Layer(std::size_t size) : score(new std::int64_t[size]), masks(new LossMask[size]),
                                       stamps(new std::uint32_t[size]{}) {}
    void reset() { ++epoch; active.clear(); }
    void offer(std::uint32_t key, std::int64_t value, const LossMask& mask) {
        if (stamps[key] != epoch) {
            stamps[key] = epoch; score[key] = value; masks[key] = mask; active.push_back(key);
        } else if (value > score[key] || (value == score[key] && earlier_mask(mask, masks[key]))) {
            score[key] = value; masks[key] = mask;
        }
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
    std::vector<std::int64_t> scores;
    std::array<int, 36> cell_letters{};
    Layer layer_a, layer_b;
    bool has_best = false;
    std::int64_t best_score = std::numeric_limits<std::int64_t>::min();
    LossMask best_mask;
    std::vector<int> best_allocation;

    Search(int k, int loss_count, std::uint64_t first, std::uint64_t limit, std::size_t cap,
           std::vector<int> key, std::string sq, const std::string& ciphertext, const std::string& table_path)
        : width(k), missing(loss_count), total_length(static_cast<int>(ciphertext.size()) + loss_count),
          first_allocation(first), allocation_limit(limit), state_cap(cap), ranks(std::move(key)), square(std::move(sq)),
          layer_a((1U << missing) * suffix_modulus), layer_b((1U << missing) * suffix_modulus) {
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
        std::ifstream input(table_path, std::ios::binary);
        scores.reserve(table_size);
        for (std::uint32_t i = 0; i < table_size; ++i) {
            const double value = static_cast<double>(read_value<float>(input)) * static_cast<double>(score_scale);
            if (!std::isfinite(value) || std::trunc(value) != value) throw std::runtime_error("Invalid integer quad score");
            scores.push_back(static_cast<std::int64_t>(value));
        }
        if (input.peek() != EOF) throw std::runtime_error("Unexpected quad table suffix");
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
            for (std::uint32_t state : current->active) {
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
                                LossMask mask = current->masks[state];
                                if (left_loss) mask.set(full_starts[left_column] + row, first);
                                if (right_loss) mask.set(full_starts[right_column] + row, second);
                                const auto value = current->score[state] + (position >= 3 ? scores[combined] : 0);
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
        for (std::uint32_t state : current->active) {
            if (state / suffix_modulus != static_cast<std::uint32_t>(combinations - 1))
                throw std::runtime_error("Final state did not consume every allocated loss");
            const auto value = current->score[state];
            if (!has_best || value > best_score || (value == best_score && earlier_mask(current->masks[state], best_mask))) {
                has_best = true; best_score = value; best_mask = current->masks[state]; best_allocation = allocation;
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
        if (argc != 5 || std::string(argv[1]) != "solve")
            throw std::runtime_error("Usage: exact_joint solve config quad_model output");
        std::ifstream input(argv[2]);
        int width, missing;
        std::uint64_t start, count;
        std::size_t cap;
        if (!(input >> width >> missing >> start >> count >> cap) || width < 2 || width > 32 || missing < 0 || missing > 6)
            throw std::runtime_error("Invalid search header");
        std::string square, ciphertext;
        input >> square;
        std::vector<int> ranks(width);
        for (auto& rank : ranks) input >> rank;
        if (!(input >> ciphertext)) throw std::runtime_error("Missing ciphertext");
        Search search(width, missing, start, count, cap, ranks, square, ciphertext, argv[3]);
        search.enumerate(0, missing);
        search.output(argv[4]);
    } catch (const std::exception& error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
    return 0;
}
