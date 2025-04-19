import json
from functools import partial

# --- Atomic helpers ---
def is_list(val): return isinstance(val, list)
def is_dict(val): return isinstance(val, dict)

# --- Check factories ---
# 1. Check if a dict is missing a key
def missing_key(key, d):
    return not (is_dict(d) and key in d)

# 2. Check if key exists but is not a list
def key_not_list(key, d):
    return not is_list(d.get(key))

# 3. Check if key points to a list of specific length
def list_len_eq(key, n, d):
    return is_list(d.get(key)) and len(d[key]) == n

# 4. Check if list at key is all strings
def list_of_str_len_eq(key, n, d):
    val = d.get(key)
    return is_list(val) and all(isinstance(x, str) for x in val) and len(val) == n

def list_of_str_len_gt(key, n, d):
    val = d.get(key)
    return is_list(val) and all(isinstance(x, str) for x in val) and len(val) > n

NE_TYPE = {
    "no_ne": {
        "check": partial(missing_key, "NE"),
        "code": "dict_no_ne",
    },
    "non_list": {
        "check": partial(key_not_list, "NE"),
        "code": "ne_type_error",
    },
    "empty": {
        "check": partial(list_len_eq, "NE", 0),
        "code": "ne_empty_list",
    },
    "one": {
        "check": partial(list_of_str_len_eq, "NE", 1),
        "code": "ne_ok",
    },
    "multi": {
        "check": partial(list_of_str_len_gt, "NE", 1),
        "code": "ne_multiple",
    }
}


def parse_json(raw):
    """Return parsed JSON if str, else pass through."""
    return json.loads(raw) if isinstance(raw, str) else raw

def build_ne_type_fn(key: str):
    """
    Build classifier for NE type.

    Input:
        key (str): base column name (e.g., output_b_v2).

    Output:
        function: maps example → {'ne_type': ...}
    """
    col_name = f"parsed_{key}"

    def classify(val):
        for entry in NE_TYPE.values():
            if entry["check"](val):
                return {"ne_type": entry["code"]}

    def classify_other():
        return {"ne_type": "type_unrecognized"}

    def fn(example):
        val_raw = example.get(col_name)
        val = parse_json(val_raw)

        if is_dict(val):
            return classify(val)

        return classify_other()

    return fn
