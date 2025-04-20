from llmgt.utils.paths import *
from llmgt.utils.config import load_dataset
from llmgt.evaluation.metrics import summarize_quality, compute_binary_accuracy
from llmgt.evaluation.parse import build_parser_fn, classify_errors

from collections import Counter
import json


def run_parser(input_path: Path, msg_key: str):
    ds = load_dataset(input_path)

    parser = build_parser_fn(msg_key)
    ds = ds.map(parser)
    ds = ds.map(classify_errors)

    status_labels = [ex["status"] for ex in ds]
    counts = Counter(status_labels)
    summary = summarize_quality(counts, total=ds.num_rows)

    if not summary["passed"]:
        print(json.dumps(summary, indent=2))
        return

    ds = ds.map(compute_binary_accuracy)
    df = ds.to_pandas()
    return df


def run_parser_for_key(exp_id: str, msg_key: str):
    path = get_stage_path("predictions", f"{exp_id}/{msg_key}.json")
    return run_parser(path, msg_key)


def run_parsing_multiple(exp_id: str, message_keys: list[str]):
    for key in message_keys:
        run_parser_for_key(exp_id, key)



def main():
    exp_id = "task_one_trial"
    message_keys = ["b_v1_0_shot"]
    path = get_stage_path("predictions", f"{exp_id}/{message_keys}.json")
    run_parsing_multiple(exp_id, message_keys)
if __name__ == "__main__":
    main()









