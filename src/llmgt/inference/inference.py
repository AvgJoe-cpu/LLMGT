from transformers import set_seed, GenerationConfig
from datasets import Dataset, load_from_disk
import os

from llmgt.inference.models import get_pipe_fn
from llmgt.utils.config import load_experiment_config
from llmgt.utils.paths import *
from pprint import pprint


def preview():
    """Pretty-print loaded experiment configs."""
    configs = load_experiment_config()
    print("\nLoaded Experiment Configs:\n")
    pprint(configs, indent=2, width=100)


def build_config(config_dict: dict) -> dict:
    base_cache = get_cache_dir()
    base_results = get_predictions_dir()
    config = enrich_paths(config_dict, base_cache, base_results)
    config["gen_config"] = GenerationConfig(**config["generation_config"])
    return config

def build_experiment(config: dict) -> dict:
    """Loads the dataset and returns the full runtime context."""
    set_seed(config["seed"])
    resolved_path = resolve_prompt_file(config["json_path"])
    ds = Dataset.from_json(str(resolved_path))

    return {
        "ds": ds,
        **config
    }


def run_experiment(ds_, config, pipe, force=False):
    gen_config = config["gen_config"]

    for msg_key in config["message_keys"]:
        output_key = get_output_key(msg_key)
        path_info = config["paths"][msg_key]

        if not force and os.path.exists(path_info["cache"]):
            ds_ = load_from_disk(path_info["cache"])
            continue

        def run_fn(batch):
            return {output_key: pipe(batch[msg_key], generation_config=gen_config)}

        ds_ = ds_.map(
            run_fn,
            batched=True,
            batch_size=config["batch_size"],
            cache_file_name=str(path_info["arrow"])
        )

        ds_.save_to_disk(path_info["cache"])

        os.makedirs(os.path.dirname(path_info["json"]), exist_ok=True)

        fields_to_keep = ["id", "matrix", "gold_ne", output_key]
        ds_out = ds_.remove_columns([col for col in ds_.column_names if col not in fields_to_keep])
        ds_out.to_json(path_info["json"], orient="records", lines=True)

    return ds_


def main():
    all_configs = load_experiment_config()
    pipe = get_pipe_fn()

    for name, cfg in all_configs.items():
        enriched_cfg = build_config(cfg)
        experiment = build_experiment(enriched_cfg)
        run_experiment(experiment["ds"], experiment, pipe=pipe)


if __name__ == "__main__":
    main()