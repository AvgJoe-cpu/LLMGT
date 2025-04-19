from .inference import preview, main
from .models import get_pipe_fn, clear_model_cache

def model_entrypoint():
    pipe = get_pipe_fn()
    print("Model loaded.")