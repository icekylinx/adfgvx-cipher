#!/usr/bin/env python3
"""Render the verified p198 digit/QY count frontier as a discrete staircase.
ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Only published exact counts are plotted; no probabilities are inferred.
"""
from pathlib import Path
import argparse
import json
import os
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'adfgvx-matplotlib-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=HERE/'results.json')
    parser.add_argument('--output', type=Path, default=HERE/'count_frontier.svg')
    parser.add_argument('--png', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    assert data['all_memberships_and_allocations_completed']
    assert data['membership_classes_completed'] == 28
    points = data['global_frontier_counts']
    budgets = list(range(16))
    exact = [min(d for d, q in points if q <= budget) for budget in budgets]
    assert exact == [row['minimum_attainable_digits'] for row in data['bounds_with_at_most_QY']]
    earlier = [max(3, 10-budget) for budget in budgets]

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none',
                         'svg.hashsalt': 'adfgvx-p198-count-frontier-v1',
                         'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(10.4, 6.6))
    fig.subplots_adjust(left=.095, right=.97, bottom=.28, top=.76)
    ax.step(budgets, earlier, where='post', color='#9ca8b0', linewidth=2.0,
            linestyle=(0, (4, 3)), label='Earlier necessary lower bound', zorder=2)
    ax.step(budgets, exact, where='post', color='#244b68', linewidth=2.4,
            label='Exact minimum for each allowed budget', zorder=3)
    ax.scatter(budgets, exact, s=28, color='#244b68', zorder=4)
    ax.annotate('Three digits first become possible\nwhen 13 Q/Y positions are allowed.',
                xy=(13, 3), xytext=(8.1, 6.55), color='#244b68', fontsize=10.5,
                arrowprops={'arrowstyle': '->', 'color': '#6a879b', 'lw': 1.2},
                ha='left', va='top')
    ax.set_xlim(-.25, 15.25)
    ax.set_ylim(2.5, 10.6)
    ax.set_xticks(budgets)
    ax.set_yticks(list(range(3, 11)))
    ax.set_xlabel('Allowed maximum number of Q or Y positions', labelpad=10)
    ax.set_ylabel('Minimum attainable digit positions', labelpad=10)
    ax.grid(axis='y', color='#d9e0e6', linewidth=.7)
    ax.set_axisbelow(True)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.015), frameon=False,
              fontsize=9.5, ncol=2, columnspacing=1.6, handlelength=2.6)
    fig.text(.095, .945, 'p198: the exact digit and Q/Y trade-off', fontsize=20,
             fontweight='bold', color='#18354a')
    fig.text(.095, .887, 'Fixed Nov13–15b partial square and 16-column rank order; exactly five deleted coordinates.',
             fontsize=10.5, color='#52626f')
    fig.text(.095, .848, 'All 40,320 square completions and all source-preserving loss/fill witnesses are covered.',
             fontsize=10.5, color='#52626f')
    fig.text(.095, .16, 'Dots show integer budgets; the staircase does not assign fractional character counts.',
             fontsize=9, color='#40505d')
    fig.text(.095, .12, 'Different budgets may use different square completions and loss masks. The historical counts are unknown.',
             fontsize=9, color='#40505d')
    fig.text(.095, .08, 'These are count constraints, not a historical plaintext or a decision that this key is correct.',
             fontsize=9, color='#40505d')
    fig.text(.095, .035, 'ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · Source: verified p198_category_frontier/results.json.',
             fontsize=8, color='#647481')
    fig.savefig(args.output, metadata={'Title': 'p198 exact digit and Q/Y count frontier',
                                      'Creator': 'icekylinx and GPT-6 Astra Pro', 'Date': None})
    if args.output.suffix.lower() == '.svg':
        args.output.write_text('\n'.join(line.rstrip() for line in args.output.read_text().splitlines())+'\n')
    if args.png:
        fig.savefig(args.png, dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()
