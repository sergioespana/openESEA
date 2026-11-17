"""
Goal 3 - Training Budget Adequacy.

Reads the Goal 1 convergence log and computes the four numbers/observations
requested by the brief: mean R_Final over the first 10% of episodes, mean
R_Final over the last 10% of episodes, the percentage change between those
two windows, and a plateaued-yes/no judgment (based on comparing the slope
of the first half vs. the second half of the run, and the variance of the
final window relative to the overall range).
"""
import csv
import os
import sys


def load_rewards(csv_path):
    rewards = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rewards.append(float(row['reward_final']))
    return rewards


def summarize(rewards, window_fraction=0.10):
    n = len(rewards)
    window = max(1, round(n * window_fraction))

    first_window = rewards[:window]
    last_window = rewards[-window:]

    mean_first = sum(first_window) / len(first_window)
    mean_last = sum(last_window) / len(last_window)

    pct_change = ((mean_last - mean_first) / abs(mean_first)) * 100 if mean_first != 0 else float('inf')

    # Simple plateau heuristic: compare the mean of the second half to the
    # mean of the first half of the run, and check how much the last window
    # still moves within itself (slope of a linear fit over the last window).
    half = n // 2
    mean_first_half = sum(rewards[:half]) / half
    mean_second_half = sum(rewards[half:]) / (n - half)
    half_over_half_change_pct = ((mean_second_half - mean_first_half) / abs(mean_first_half)) * 100 if mean_first_half != 0 else float('inf')

    # Linear slope over the last window (least squares), normalised by the
    # window's own mean so it's comparable in magnitude to pct_change.
    xs = list(range(len(last_window)))
    x_mean = sum(xs) / len(xs)
    y_mean = mean_last
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, last_window))
    den = sum((x - x_mean) ** 2 for x in xs)
    slope = num / den if den != 0 else 0.0

    plateaued = abs(half_over_half_change_pct) < 5 and abs(slope) < 0.01 * abs(mean_last if mean_last != 0 else 1)

    return {
        'n_episodes': n,
        'window_size': window,
        'mean_first_window': mean_first,
        'mean_last_window': mean_last,
        'pct_change': pct_change,
        'mean_first_half': mean_first_half,
        'mean_second_half': mean_second_half,
        'half_over_half_change_pct': half_over_half_change_pct,
        'last_window_slope': slope,
        'plateaued': plateaued,
    }


def format_summary(stats, label):
    plateau_word = 'plateaued' if stats['plateaued'] else 'still trending (not clearly plateaued)'
    text = (
        "[{label}] Over {n} episodes: mean R_Final for the first {w} episodes = {mf:.4f}; "
        "mean R_Final for the last {w} episodes = {ml:.4f}; change = {pct:+.1f}%. "
        "First-half mean = {mfh:.4f}, second-half mean = {msh:.4f} ({hpct:+.1f}% half-over-half), "
        "last-window slope = {slope:+.5f}/episode -> the reward curve appears {plateau}."
    ).format(
        label=label,
        n=stats['n_episodes'], w=stats['window_size'],
        mf=stats['mean_first_window'], ml=stats['mean_last_window'], pct=stats['pct_change'],
        mfh=stats['mean_first_half'], msh=stats['mean_second_half'], hpct=stats['half_over_half_change_pct'],
        slope=stats['last_window_slope'], plateau=plateau_word,
    )
    return text


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', 'results', 'goal1_training_log_100ep.csv'))
    label = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(csv_path)

    rewards = load_rewards(csv_path)
    stats = summarize(rewards)
    text = format_summary(stats, label)
    print(text)

    out_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'results',
                                               'goal3_training_budget_summary.txt'))
    mode = 'a' if os.path.exists(out_path) and len(sys.argv) > 1 else 'w'
    with open(out_path, mode) as f:
        f.write(text + '\n')
    print('Appended summary to {}'.format(out_path))
