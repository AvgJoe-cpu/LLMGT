import json
import re

from llmgt.utils.paths import get_stage_path, ensure_parent_dir
from pathlib import Path

# --- Regex pattern for extracting inline or block JSON from model output ---
COMPOUND_PATTERN = re.compile(
    r"```json\s*\n(.*?)\n```"           # 1. strict fenced block
    r"|```json\s*(.*?)```"             # 2. inline fenced
    r"|```\s*\n(.*?)\n```"             # 3. untagged fenced
    r"|^\s*json\s*\n(.*?\{.*?\})",     # 4. 'json' header
    re.DOTALL | re.MULTILINE
)

COMPOUND_NE_TYPE_PATTERN = re.compile(
    r'"NE"\s*:\s*\[\s*("([A-Z]{2})")\s*\]'                             # Group 1: strict, one 2-letter item only
    r'|"NE"\s*:\s*\[\s*("([A-Z]{2}"(?:\s*,\s*"[A-Z]{2}")+)?)\s*\]'     # Group 2: list with commas (forbidden)
    r'|"NE"\s*:\s*\[\s*\]'                                            # Group 3: empty list
    r'|"NE"\s*:\s*".*?"'                                              # Group 4: not a list
    , re.DOTALL
)

VALID_NE_VALUES = {"TL", "BL", "TR", "BR"}

def extract_json_block(text: str) -> str | None:
    match = COMPOUND_PATTERN.search(text)
    return next((g.strip() for g in match.groups() if g), None) if match else None


def build_parser_fn(key: str):
    def parse(example):
        raw = example[key][0]["generated_text"]
        block = extract_json_block(raw)
        if block is None:
            return {
                "parsed": "",
                "success": False
            }

        try:
            parsed = json.dumps(json.loads(block), separators=(",", ":")) if block else ""
            return {
                "parsed": parsed,
                "success": bool(parsed)
            }
        except json.JSONDecodeError:
            return {
                "parsed": "",
                "success": False
            }
    return parse


def classify_errors(example):
    preds = example["parsed"]

    if not isinstance(preds, str):
        return {"status": "format", "pred": ""}

    match = COMPOUND_NE_TYPE_PATTERN.search(preds)
    if not match:
        return {"status": "missing", "pred": ""}

    groups = match.groups()
    if groups[0]:
        pred = groups[1]
        status = "valid" if pred in VALID_NE_VALUES else "invalid"
        return {"status": status, "pred": pred if status == "valid" else ""}

    if groups[2]:
        return {"status": "multiple", "pred": ""}

    if groups[4] is not None:
        return {"status": "empty", "pred": ""}

    if groups[5]:
        return {"status": "malformed", "pred": ""}

    return {"status": "format", "pred": ""}


def get_eval_output_path(exp_id: str, msg_key: str) -> Path:
    return get_stage_path("eval", f"{exp_id}/{msg_key}_parsed.json")

