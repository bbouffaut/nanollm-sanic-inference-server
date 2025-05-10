import os
from pathlib import Path
import sys
from dotenv import load_dotenv

# Load environment variables from configurable .env file location
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", "config/.env")
load_dotenv(ENV_FILE_PATH)

MODELS_PARAMS_FILE = os.getenv("MODELS_PARAMS_FILE", {})
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
PORT=int(os.getenv("PORT", 8000))
SANIC_WORKER_STARTUP_THRESHOLD=int(os.getenv("SANIC_WORKER_STARTUP_THRESHOLD", 300))
