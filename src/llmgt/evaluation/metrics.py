from collections import Counter


def summarize_quality(counter: Counter, total: int, ok_label: str = "valid") -> dict:
    n_ok = counter.get(ok_label, 0)
    n_err = total - n_ok
    rate = n_ok / total if total else 0.0

    gate_passed = (
        n_ok >= 60 or
        (n_ok >= 40 and rate >= 0.80)
    )

    return {
        "total": total,
        ok_label: n_ok,
        "num_errors": n_err,
        "errors": {
            k: v for k, v in counter.items() if k != ok_label
        },
        "success_rate": rate,
        "passed": gate_passed
    }


def compute_binary_accuracy(example):
    """
    Compares predicted NE ('pred') to gold NE ('gold_ne').
    Returns:
        - binary_acc: 1 if equal, 0 otherwise
        - pred_nash: prediction string
    """
    pred = example["pred"]
    gold = example["gold_ne"][0]
    return {
        "binary_acc": int(pred == gold),
        "pred": pred
    }
