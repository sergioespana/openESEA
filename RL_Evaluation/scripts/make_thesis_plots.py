"""
Thesis figures for the RL evaluation, drawn from the CSVs in ../results:
- RL_Training_Convergence.png      (Goal 1: R_Final per episode, small and large dashboard)
- Goal5_Reward_Comparison.png      (Goal 5: R_Final per episode for four hyperparameter settings)
- Goal5_ValidActions_Comparison.png (Goal 5: valid actions sampled per episode)

The original plotting script (27-09-2026) was not kept; this re-creates the
same three figures from the same logs (checked against the thesis figures:
same data and layout; only the drawing order of overlapping lines differs).
Output goes to ../results/plots.
Usage: python make_thesis_plots.py
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RESULTS = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'results'))
OUT = os.path.join(RESULTS, 'plots')
DPI = 150
STABLE_TOL = 1e-3  # reward counts as stable once it stays within this of its final value


def load(name):
    return pd.read_csv(os.path.join(RESULTS, name))


def stabilisation_episode(df):
    """First episode from which R_Final stays within STABLE_TOL of the final value."""
    final = df['reward_final'].iloc[-1]
    off = (df['reward_final'] - final).abs() >= STABLE_TOL
    return int(df['episode'][off].max() + 1) if off.any() else int(df['episode'].iloc[0])


def convergence_plot():
    small = load('goal1_training_log_100ep.csv')
    large = load('goal1_training_log_100ep_large_dashboard.csv')
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for df, label, colour in ((small, 'Small dashboard (6 visualisations)', 'tab:blue'),
                              (large, 'Large dashboard (15 visualisations)', 'tab:red')):
        ax.plot(df['episode'], df['reward_final'], color=colour, label=label)
        ep = stabilisation_episode(df)
        ax.axvline(ep, color=colour, linestyle='--', alpha=0.7)
        print(f'{label}: stable from episode {ep}')
    ax.set_xlabel('Episode')
    ax.set_ylabel(r'$R_{\mathrm{Final}}$ (episode reward)')
    ax.grid(alpha=0.3)
    ax.legend(loc='lower right')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'RL_Training_Convergence.png'), dpi=DPI)
    plt.close(fig)


GOAL5_RUNS = (
    ('goal1_training_log_100ep.csv', 'Baseline (lr=1e-2, γ=1.0, current default)', 'black'),
    ('goal5_training_log_lr1e-3.csv', 'Lower LR (lr=1e-3, γ=1.0)', 'tab:blue'),
    ('goal5_training_log_gamma0.95.csv', 'Lower γ (lr=1e-2, γ=0.95)', 'tab:orange'),
    ('goal5_training_log_entropy_default_c0.01.csv', 'Entropy bonus (lr=1e-2, γ=1.0, coef=0.01)', 'tab:green'),
)


def goal5_plot(column, ylabel, filename, floor=None, legend_loc='lower left'):
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for name, label, colour in GOAL5_RUNS:
        df = load(name)
        ax.plot(df['episode'], df[column], color=colour, label=label)
    if floor is not None:
        ax.axhline(floor, color='grey', linestyle='--', label='10% validity floor (20/200 steps)')
    ax.set_xlabel('Training episode')
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.legend(loc=legend_loc, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, filename), dpi=DPI)
    plt.close(fig)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    convergence_plot()
    goal5_plot('reward_final', r'$R_{\mathrm{Final}}$ (mean per-step reward, per episode)',
               'Goal5_Reward_Comparison.png')
    goal5_plot('valid_actions', 'Valid actions sampled per episode',
               'Goal5_ValidActions_Comparison.png', floor=20, legend_loc='upper right')
    print('plots written to', OUT)
