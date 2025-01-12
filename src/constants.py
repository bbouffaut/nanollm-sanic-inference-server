import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from configurable .env file location
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", "config/.env")
load_dotenv(ENV_FILE_PATH)

# Model paths
DEFAULT_MODEL_PATH = "models/model.gguf"
MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", DEFAULT_MODEL_PATH)

# Ensure the model path is absolute
MODEL_PATH = str(Path(MODEL_PATH).absolute())
