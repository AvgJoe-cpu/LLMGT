from transformers import set_seed
import json

from llmgt.inference.models import get_pipe_fn
from llmgt.utils.paths import get_stage_path, ensure_parent_dir, get_data_path
from llmgt.utils.config import load_dataset, load_generation_config, save_dataset_json


def load_and_prepare_experiments(name="experiments.json") -> dict:
    path = get_data_path("experimental_config", name)
    configs = json.load(open(path, encoding="utf-8"))

    for exp_key, config in configs.items():
        set_seed(config["seed"])
        config["id"] = config.get("id", exp_key)
        config["gen_config"] = load_generation_config(config)

    return configs


def run_inference_for_key(ds, pipe, config, msg_key):
    """
    Run inference for a single message key and save the output to a JSON file.
    Output is stored under: pipeline_data/stages/predictions/<exp_id>_<msg_key>.json
    """
    output_key = msg_key
    output_path = get_stage_path("predictions", f"{config['id']}/{msg_key}.json")
    batch_size = config["batch_size"]
    gen_config = config["gen_config"]

    def run_fn(batch):
        outputs = pipe(batch[msg_key], generation_config=gen_config)
        return {output_key: outputs}

    ds_out = ds.map(run_fn, batched=True, batch_size=batch_size)

    ensure_parent_dir(output_path)
    fields_to_keep = ["id", "matrix", "gold_ne", output_key]
    ds_out = ds_out.select_columns([k for k in fields_to_keep if k in ds_out.column_names])

    save_dataset_json(ds_out, output_path)
    return ds_out


def run_experiment(base_ds, config, pipe):
    """
    Run inference across all message keys, writing output files per key.
    """
    for msg_key in config["message_keys"]:
        run_inference_for_key(base_ds, pipe, config, msg_key)


def main():
    configs = load_and_prepare_experiments()
    config = configs["exp_task_one"]
    pipe = get_pipe_fn()

    ds = load_dataset(get_stage_path("prompts", "test_prompt.json"))

    run_experiment(ds, config, pipe)


if __name__ == "__main__":
    main()