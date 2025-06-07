"""Algorithms for matching two sequences of frame features."""

from typing import List, Tuple


def dynamic_time_warping(seq_a: List[float], seq_b: List[float]) -> Tuple[float, List[Tuple[int, int]]]:
    """Compute DTW distance between two sequences.

    Parameters
    ----------
    seq_a, seq_b:
        Feature sequences.

    Returns
    -------
    Tuple containing the DTW cost and the alignment path.
    """
    n = len(seq_a)
    m = len(seq_b)
    # Initialize cost matrix
    cost = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0.0
    # Compute dynamic programming table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diff = seq_a[i - 1] - seq_b[j - 1]
            val = diff * diff
            cost[i][j] = val + min(
                cost[i - 1][j],    # insertion
                cost[i][j - 1],    # deletion
                cost[i - 1][j - 1] # match
            )
    # Backtrack to find path
    i, j = n, m
    path = []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        diag = cost[i - 1][j - 1]
        left = cost[i][j - 1]
        up = cost[i - 1][j]
        if diag <= left and diag <= up:
            i -= 1
            j -= 1
        elif left < up:
            j -= 1
        else:
            i -= 1
    path.reverse()
    return cost[n][m], path


def find_best_match(long_seq: List[float], short_seq: List[float], window: int = 10) -> Tuple[int, float]:
    """Find the index in ``long_seq`` that best matches ``short_seq``.

    Parameters
    ----------
    long_seq:
        Feature sequence from the longer video.
    short_seq:
        Feature sequence from the shorter video.
    window:
        Search window size.

    Returns
    -------
    Tuple[int, float]
        Start index of the best match and the matching cost.
    """
    best_index = -1
    best_cost = float('inf')
    for start in range(0, max(1, len(long_seq) - len(short_seq) + 1), window):
        segment = long_seq[start : start + len(short_seq)]
        if len(segment) < len(short_seq):
            break
        cost, _ = dynamic_time_warping(segment, short_seq)
        if cost < best_cost:
            best_cost = cost
            best_index = start
    return best_index, best_cost
