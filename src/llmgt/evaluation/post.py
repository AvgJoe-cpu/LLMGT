from llmgt.evaluation.pre import *
from llmgt.evaluation.checks import *
from collections import Counter


def check_eval_gate(counter: Counter, total: int, ok_label: str = "ne_ok") -> tuple[bool, int, float]:
    """
    Eval gate: Check if sample meets threshold for evaluation.

    Input:
        counter: label counts
        total: number of examples

    Output:
        (fit, count_ok, rate)
    """
    n_ok = counter.get(ok_label, 0)
    rate = n_ok / total if total else 0.0

    fit = (
        n_ok >= 60 or
        (n_ok >= 40 and rate >= 0.80)
    )
    return fit, n_ok, rate

def build_error_summary(counter: Counter, ok_label: str = "ne_ok") -> dict:
    total = sum(counter.values())
    n_ok = counter.get(ok_label, 0)
    n_err = total - n_ok
    return {
        "total": total,
        "ne_ok": n_ok,
        "errors": {
            k: v for k, v in counter.items() if k != ok_label
        },
        "num_errors": n_err
    }

def run_post(ds, input_key):
    # --- Step 0: Initial parse ---
    parse_fn = build_parse_fn(input_key)
    ds = ds.map(parse_fn)

    # --- Step 1: Flag parse results ---
    success_key = f"success_{input_key}"
    error_key = f"error_{input_key}"
    total_before = len(ds)

    # --- Step 2: Filter well-formed entries ---
    ds_filtered = ds.filter(lambda ex: ex.get(success_key) is True)
    ds_filtered = ds_filtered.remove_columns([success_key, error_key])

    # Filter by NE structure
    type_fn = build_ne_type_fn(input_key)
    ds_filtered = ds_filtered.map(type_fn)

    if "ne_type" in ds_filtered.column_names:
        error_stats = Counter(ds_filtered["ne_type"])
        error_summary = build_error_summary(error_stats)
        fit_for_eval, _, _ = check_eval_gate(error_stats, total_before)

        ds_filtered = ds_filtered.filter(lambda ex: ex["ne_type"] == "ne_ok").remove_columns(["ne_type"])
    else:
        fit_for_eval = False
        error_summary = None

    return ds_filtered, {
        "fit_for_eval": fit_for_eval,
        "error_summary": error_summary
    }