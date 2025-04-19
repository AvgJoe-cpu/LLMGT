import random
from typing import Callable, Tuple

def sample_payoffs() -> list[int]:
    """
    Samples a list of four random payoff values between 1 and 10.

    Returns:
        list[int]: A list of four integers representing 2x2 game payoffs.
    """
    return [random.randint(1, 10) for _ in range(4)]

def sample_fn(condition: Callable[[int, int, int, int], bool]):
    """
    Samples payoff tuples until a given condition is satisfied.

    Args:
        condition (Callable): A function that takes four integers (payoffs)
            and returns True if the sampled tuple meets the criteria.

    Returns:
        tuple[int, int, int, int]: A payoff tuple that satisfies the condition.
    """
    while True:
        a = sample_payoffs()
        if condition(*a):
            return tuple(a)

def sample_game_fn(p1_cond: Callable[[int, int, int, int], bool],
                   p2_cond: Callable[[int, int, int, int], bool]):
    """
    Samples a payoff tuple for each player, satisfying their respective conditions.

    Args:
        p1_cond: Condition applied to Player 1's payoff tuple.
        p2_cond: Condition applied to Player 2's payoff tuple.

    Returns:
        A pair of payoff tuples: (p1, p2).
    """
    p1 = sample_fn(p1_cond)
    p2 = sample_fn(p2_cond)
    return p1, p2


def cond_p1_dominant_top(x1, x2, x3, x4):
    """
    Returns True if Player 1 strictly prefers the top row.

    Requires: x1 > x3 and x2 > x4
    """
    return x1 > x3 and x2 > x4


def cond_p1_dominant_bot(x1, x2, x3, x4):
    """
    Returns True if Player 1 strictly prefers the bottom row.

    Requires: x3 > x1 and x4 > x2
    """
    return x3 > x1 and x4 > x2


def cond_p2_dominant_left(y1, y2, y3, y4):
    """
    Returns True if Player 2 strictly prefers the left column.

    Requires: y1 > y2 and y3 > y4
    """
    return y1 > y2 and y3 > y4


def cond_p2_dominant_right(y1, y2, y3, y4):
    """
    Returns True if Player 2 strictly prefers the right column.

    Requires: y2 > y1 and y4 > y3
    """
    return y2 > y1 and y4 > y3


CONFIG_GAMES = {
    "1NE": [
        {
            "p1_cond": cond_p1_dominant_top,
            "p2_cond": cond_p2_dominant_left,
            "structure": {
                "dominance": {
                    "p1": "top",
                    "p2": "left"
                }
            },
            "nash_locations": ["TL"]
        },
        {
            "p1_cond": cond_p1_dominant_top,
            "p2_cond": cond_p2_dominant_right,
            "structure": {
                "dominance": {
                    "p1": "top",
                    "p2": "right"
                }
            },
            "nash_locations": ["TR"]
        },
        {
            "p1_cond": cond_p1_dominant_bot,
            "p2_cond": cond_p2_dominant_left,
            "structure": {
                "dominance": {
                    "p1": "bot",
                    "p2": "left"
                }
            },
            "nash_locations": ["BL"]
        },
        {
            "p1_cond": cond_p1_dominant_bot,
            "p2_cond": cond_p2_dominant_right,
            "structure": {
                "dominance": {
                    "p1": "bot",
                    "p2": "right"
                }
            },
            "nash_locations": ["BR"]
        },
    ]
}