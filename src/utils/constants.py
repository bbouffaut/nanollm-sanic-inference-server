import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from configurable .env file location
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", "config/.env")
load_dotenv(ENV_FILE_PATH)

# Model paths
DEFAULT_MODEL_PATH = "models/"
MODEL_PATH = os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)
# Ensure the model path is absolute
MODEL_PATH = str(Path(MODEL_PATH).absolute())

DEFAULT_MODEL_FILE = "model.gguf"
MODEL_FILE = os.getenv("MODEL_FILE", DEFAULT_MODEL_FILE)

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
