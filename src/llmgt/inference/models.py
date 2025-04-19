from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM,
)

VALID_MODELS = {
    "qwen-0.5_inst": "Qwen/Qwen2.5-0.5B-Instruct",
    "qwen-3_inst": "Qwen/Qwen2.5-3B-Instruct",
    "qwen-3": "Qwen/Qwen2.5-3B",
    "qwen-7_inst": "Qwen/Qwen2.5-7B-Instruct",
    "qwen-7": "Qwen/Qwen2.5-7B",
}

_MODEL_PATH = VALID_MODELS["qwen-0.5_inst"]
_PIPE = None

def get_pipe_fn():
    global _PIPE
    if _PIPE is None:
        tokenizer = AutoTokenizer.from_pretrained(_MODEL_PATH)
        model = AutoModelForCausalLM.from_pretrained(_MODEL_PATH, device_map="auto")
        _PIPE = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            return_full_text=False,
        )
    return _PIPE


def set_model(model_key: str):
    global _MODEL_PATH, _PIPE
    new_path = VALID_MODELS[model_key]
    if new_path != _MODEL_PATH:
        _MODEL_PATH = new_path
        _PIPE = None  # Lazy reload on next call

def clear_model_cache():
    global _PIPE
    _PIPE = None
