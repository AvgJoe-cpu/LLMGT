from llmgt.utils.paths import get_sampled_games_dir

from .build_games import *
import os
import uuid
from pprint import pprint
import argparse
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

####
def build_labelled_payoffs(p1: tuple[int, int, int, int],
                           p2: tuple[int, int, int, int]) -> Tuple[dict, dict]:
    labels = ["TL", "TR", "BL", "BR"]
    return dict(zip(labels, p1)), dict(zip(labels, p2))

def build_matrix_fn(data: dict) -> list[list]:
    return [[data["TL"], data["TR"]],[data["BL"], data["BR"]]]

def build_combined_matrix_fn(mx1: list[list], mx2: list[list]):
    return [[[mx1[r][c], mx2[r][c]] for c in range(2)]for r in range(2)]

def build_action_fn(mx1: list[list], mx2: list[list]):
    p1_actions = {
        "top": mx1[0],
        "bot": mx1[1]
    }
    p2_actions = {
        "left": [mx2[0][0], mx2[1][0]],
        "right": [mx2[0][1], mx2[1][1]]
    }
    return p1_actions, p2_actions


def extract_gold_labels_fn(payoffs_p1: dict, payoffs_p2: dict) -> tuple[list[dict], list[dict]]:
    combined_entries = [
        {"label": label, "x": payoffs_p1[label], "y": payoffs_p2[label]}
        for label in payoffs_p1
    ]

    sorted_p1 = sorted(combined_entries, key=lambda d: d["x"], reverse=True)
    sorted_p2 = sorted(combined_entries, key=lambda d: d["y"], reverse=True)

    return sorted_p1, sorted_p2


def wrap_game_data_v2(config_block: dict, batch_id: str = None) -> list[dict]:
    results = []
    batch_id = batch_id or uuid.uuid4().hex[:8]

    for idx, cfg in enumerate(config_block["1NE"], start=1):
        p1, p2 = sample_game_fn(cfg["p1_cond"], cfg["p2_cond"])
        payoffs_p1, payoffs_p2 = build_labelled_payoffs(p1, p2)

        x_matrix = build_matrix_fn(payoffs_p1)
        y_matrix = build_matrix_fn(payoffs_p2)
        combined_matrix = build_combined_matrix_fn(x_matrix, y_matrix)
        p1_labels, p2_labels = extract_gold_labels_fn(payoffs_p1, payoffs_p2)
        p1_actions, p2_actions = build_action_fn(x_matrix, y_matrix)

        game_id = f"{batch_id}-cfg{idx:02d}"

        full_game = {
            "id": game_id,
            "payoffs": {
                "p1": payoffs_p1,
                "p2": payoffs_p2
            },
            "source": {
                "matrix": combined_matrix
            },
            "golds": {
                "p1_matrix": x_matrix,
                "p2_matrix": y_matrix,
                "labels": {
                    "p1": p1_labels,
                    "p2": p2_labels,
                },
                "actions": {
                    "p1": p1_actions,
                    "p2": p2_actions
                },
                "dominance": cfg["structure"]["dominance"],
                "nash": cfg["nash_locations"]
            }
        }

        variant_game = {
            "id": game_id,
            "matrix": combined_matrix,
            "gold_ne": cfg["nash_locations"]
        }

        results.append({
            "full": full_game,
            "variant": variant_game
        })

    return results


def sample_games(config_block: dict, n_batches: int = 1) -> list[dict]:
    """
    Samples a list of 2x2 games according to the provided configuration.

    Args:
        config_block (dict): A configuration block defining payoff structure,
            Nash location, and symbolic labeling.
        n_batches (int, optional): Number of batches to sample. Defaults to 1.

    Returns:
        list[dict]: A list of dictionaries, each representing a sampled game.
            Includes matrix data, action labels, and NE labels.
    """
    all_games = []

    for batch_num in range(1, n_batches + 1):
        batch_id = f"IDx-{batch_num:03d}"
        batch_games = wrap_game_data_v2(config_block, batch_id=batch_id)
        all_games.extend(batch_games)

    return all_games

def main():
    parser = argparse.ArgumentParser(description="Sample deterministic game data and optionally dump to JSON.")
    parser.add_argument('-n', '--n_batches', type=int, default=None,
                        help="Number of batches to sample and dump to JSON")

    args = parser.parse_args()

    SEED = 42
    random.seed(SEED)
    sample1 = sample_games(CONFIG_GAMES, n_batches=args.n_batches or 1)
    random.seed(SEED)
    sample2 = sample_games(CONFIG_GAMES, n_batches=args.n_batches or 1)

    identical_samples = sample1 == sample2
    print("Samples identical?", identical_samples)
    if not identical_samples:
        print("Differences detected!")
        exit(1)
    else:
        print("Verified: Sampling is deterministic.\n")

    if args.n_batches is not None:
        full_games = [g["full"] for g in sample1]
        variant_games = [g["variant"] for g in sample1]

        output_dir = get_sampled_games_dir()
        os.makedirs(output_dir, exist_ok=True)

        full_filename = os.path.join(output_dir, f"sampled_games_{args.n_batches}_batches_full.json")
        with open(full_filename, "w") as f:
            json.dump(full_games, f, indent=2)

        variant_filename = os.path.join(output_dir, f"sampled_games_{args.n_batches}_batches_variant.json")
        with open(variant_filename, "w") as f:
            json.dump(variant_games, f, indent=2)

        print(f"Full games dumped to: {full_filename}")
        print(f"Variant games dumped to: {variant_filename}")
    else:
        pprint(sample1)

if __name__ == "__main__":
    main()
