// Exact insertion DP in the fractionated stream, before column transposition.
// Prepared by icekylinx and GPT-6 Astra Pro. Historical keys retain prior credit.
// Build: c++ -O3 -std=c++17 interim_dp.cpp -o interim_dp
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

constexpr int A = 37;
constexpr int K = A * A * A;
constexpr int LAST2 = A * A;
constexpr double NEG = -std::numeric_limits<double>::infinity();
const std::string CO = "ADFGVX";
const std::string ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?";

int main(int argc, char** argv) {
  try {
    if (argc != 5) throw std::runtime_error("usage: interim_dp model37.bin square losses observed_interim");
    const auto started = std::chrono::steady_clock::now();
    const std::string square = argv[2], observed = argv[4];
    const int losses = std::stoi(argv[3]);
    if (square.size() != 36 || losses < 0 || losses > 15 || (observed.size() + losses) % 2)
      throw std::runtime_error("invalid square, loss count, or parity");
    const int chars = static_cast<int>((observed.size() + losses) / 2);
    if (chars < 1) throw std::runtime_error("empty plaintext");
    std::vector<int> labels(36), coordinates(observed.size());
    for (int i = 0; i < 36; ++i) {
      auto p = ABC.find(square[i]);
      if (p == std::string::npos) throw std::runtime_error("invalid square label");
      labels[i] = static_cast<int>(p);
    }
    for (size_t i = 0; i < observed.size(); ++i) {
      auto p = CO.find(observed[i]);
      if (p == std::string::npos && observed[i] != '?') throw std::runtime_error("invalid coordinate");
      coordinates[i] = observed[i] == '?' ? -1 : static_cast<int>(p);
    }
    std::vector<float> model(static_cast<size_t>(K) * A);
    std::ifstream file(argv[1], std::ios::binary);
    if (!file.read(reinterpret_cast<char*>(model.data()), model.size() * sizeof(float)))
      throw std::runtime_error("could not read complete model");
    char extra;
    if (file.read(&extra, 1)) throw std::runtime_error("unexpected model bytes");
    const int states = (losses + 1) * K;
    std::vector<double> current(states, NEG), next(states, NEG);
    std::vector<int> active{0}, next_active;
    std::vector<uint32_t> back(static_cast<size_t>(chars + 1) * states, UINT32_MAX);
    current[0] = 0;
    uint64_t expanded = 0, transitions = 0, improved = 0;
    size_t maximum_active = 1;
    for (int t = 0; t < chars; ++t) {
      next_active.clear();
      for (int state : active) {
        ++expanded;
        const int used = state / K, context = state % K;
        const int index = 2 * t - used;
        if (index < 0 || index > static_cast<int>(observed.size())) continue;
        auto transition = [&](int mode, int cell, int added) {
          const int new_used = used + added;
          if (new_used > losses) return;
          const int label = labels[cell];
          const int new_context = (context % LAST2) * A + label;
          const int target = new_used * K + new_context;
          const double value = current[state] + (t >= 3 ? model[context * A + label] : 0.0);
          ++transitions;
          if (value > next[target]) {
            if (!std::isfinite(next[target])) next_active.push_back(target);
            next[target] = value;
            // 16 bits previous context, 4 previous losses, 6 cell, 2 mode.
            back[static_cast<size_t>(t + 1) * states + target] =
                static_cast<uint32_t>(context) |
                (static_cast<uint32_t>(used) << 16) |
                (static_cast<uint32_t>(cell) << 20) |
                (static_cast<uint32_t>(mode) << 26);
            ++improved;
          }
        };
        // mode 0: both coordinates observed; 1: first observed, second lost;
        // mode 2: first lost, second observed; 3: both coordinates lost.
        if (index + 2 <= static_cast<int>(observed.size())) {
          for (int r = 0; r < 6; ++r) if (coordinates[index] < 0 || coordinates[index] == r)
            for (int c = 0; c < 6; ++c) if (coordinates[index + 1] < 0 || coordinates[index + 1] == c)
              transition(0, 6 * r + c, 0);
        }
        if (used < losses && index < static_cast<int>(observed.size())) {
          for (int r = 0; r < 6; ++r)
            for (int c = 0; c < 6; ++c) {
              if (coordinates[index] < 0 || coordinates[index] == r) transition(1, 6 * r + c, 1);
              if (coordinates[index] < 0 || coordinates[index] == c) transition(2, 6 * r + c, 1);
            }
        }
        if (used + 2 <= losses)
          for (int cell = 0; cell < 36; ++cell) transition(3, cell, 2);
      }
      for (int state : active) current[state] = NEG;
      current.swap(next);
      active.swap(next_active);
      maximum_active = std::max(maximum_active, active.size());
    }
    int winner = -1;
    double score = NEG;
    for (int state : active) {
      if (state / K == losses && current[state] > score) {
        score = current[state]; winner = state;
      }
    }
    if (winner < 0) throw std::runtime_error("no feasible alignment");
    std::string text(chars, '?'), complete(chars * 2, '?');
    std::vector<int> lost;
    int state = winner;
    for (int t = chars; t > 0; --t) {
      uint32_t code = back[static_cast<size_t>(t) * states + state];
      if (code == UINT32_MAX) throw std::runtime_error("missing traceback");
      const int context = code & 65535u;
      const int used = (code >> 16) & 15u;
      const int cell = (code >> 20) & 63u;
      const int mode = (code >> 26) & 3u;
      const int first = 2 * (t - 1);
      complete[first] = CO[cell / 6]; complete[first + 1] = CO[cell % 6];
      text[t - 1] = square[cell];
      if (mode == 2 || mode == 3) lost.push_back(first);
      if (mode == 1 || mode == 3) lost.push_back(first + 1);
      state = used * K + context;
    }
    std::sort(lost.begin(), lost.end());
    if (static_cast<int>(lost.size()) != losses || state != 0)
      throw std::runtime_error("invalid traceback endpoint");
    std::string shortened;
    for (int i = 0; i < chars * 2; ++i)
      if (!std::binary_search(lost.begin(), lost.end(), i)) shortened += complete[i];
    if (shortened.size() != observed.size()) throw std::runtime_error("wrong witness length");
    for (size_t i = 0; i < observed.size(); ++i)
      if (observed[i] != '?' && observed[i] != shortened[i]) throw std::runtime_error("witness changed observation");
    const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    std::cout << std::setprecision(17)
      << "{\"completed\":true,\"plaintext\":\"" << text
      << "\",\"full_interim\":\"" << complete << "\",\"missing_interim_indices\":[";
    for (size_t i = 0; i < lost.size(); ++i) std::cout << (i ? "," : "") << lost[i];
    std::cout << "],\"score_sum\":" << score
      << ",\"score_mean\":" << (chars >= 4 ? score / (chars - 3) : 0)
      << ",\"states_expanded\":" << expanded << ",\"transitions_evaluated\":" << transitions
      << ",\"improving_updates\":" << improved << ",\"maximum_active_states\":" << maximum_active
      << ",\"elapsed_seconds\":" << elapsed << "}\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n'; return 2;
  }
}
