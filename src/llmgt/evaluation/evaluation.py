from llmgt.evaluation.post import *
from llmgt.utils.paths import *
from datasets import Dataset
import re
import pathlib
import pandas as pd
import glob
import json

OUTPUT_KEY_RE = re.compile(r"^output_(?P<variant>.+)$")
FILENAME_RE = re.compile(r"t(?P<temp>\d+).*?_b_v(?P<prompt>\d)_0_shot\.json$")

def get_key_fn(columns):
    """Return first column matching OUTPUT_KEY_RE or None."""
    return next((col for col in columns if OUTPUT_KEY_RE.match(col)), None)


def extract_meta_fn(path):
    """Extract metadata and prompt version from filename."""
    m = FILENAME_RE.search(path.name)
    return {
        "temperature": int(m.group("temp")) / 10,   # 07 → 0.7
        "prompt": f"v{m.group('prompt')}"           # 3 → v3
    }


def build_eval_fn(key: str):
    """Return eval fn that compares predicted vs. gold NE for a given key."""
    parsed_key = f"parsed_{key}"

    def fn(example):
        parsed = json.loads(example[parsed_key])
        pred_nash = parsed["NE"][0]
        gold_nash = example["gold_ne"][0]
        return {
            "binary_acc": int(pred_nash == gold_nash),
            "pred_nash": pred_nash
        }

    return fn

def evaluate(path):
    """
    Evaluate a prediction file.

    Input:
        path (Path): JSON file with model predictions.

    Output:
        pd.DataFrame or None: Structured eval table with NE accuracy,
        or None if evaluation is skipped.
    """
    ds = Dataset.from_json(str(path))
    input_key = get_key_fn(ds.column_names)
    post_ds, stats = run_post(ds, input_key)

    if not stats["fit_for_eval"]:
        return None

    eval_fn = build_eval_fn(input_key)
    post_ds = post_ds.map(eval_fn)

    # Convert to pandas
    df = post_ds.to_pandas()
    required_cols = {"id", "gold_ne", "pred_nash", "binary_acc"}
    if not required_cols.issubset(df.columns):
        return None

    # Retain + structure columns
    df = df[["id", "gold_ne", "pred_nash", "binary_acc"]].copy()

    # Append file-level metadata
    meta = extract_meta_fn(path)
    df["source_file"] = path.name
    df["temperature"] = meta["temperature"]
    df["prompt"] = meta["prompt"]

    df = df[[
        "source_file",
        "temperature",
        "prompt",
        "id",
        "gold_ne",
        "pred_nash",
        "binary_acc"
    ]]

    return df

def build_big_df_from_dir(pred_dir: Path) -> pd.DataFrame:
    return pd.concat(
        [evaluate(p) for p in pred_dir.glob("*.json") if evaluate(p) is not None],
        ignore_index=True
    )

def build_big_df(pred_dirs: list[Path]) -> pd.DataFrame:
    results = []
    for pred_dir in pred_dirs:
        for p in pred_dir.glob("*.json"):
            res = evaluate(p)
            if res is not None:
                results.append(res)
    return pd.concat(results, ignore_index=True) if results else pd.DataFrame()



