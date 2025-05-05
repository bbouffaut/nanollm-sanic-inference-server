import os
from pathlib import Path
import sys
from dotenv import load_dotenv

# Load environment variables from configurable .env file location
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", "config/.env")
load_dotenv(ENV_FILE_PATH)

# Check if VIRTUAL_ENV is present in the loaded environment variables
if not os.getenv("UV_PROJECT_ENVIRONMENT"):
    print(f"ERROR: UV_PROJECT_ENVIRONMENT environment variable is not set in {ENV_FILE_PATH}")
    print("Make sure UV_PROJECT_ENVIRONMENT is defined in your environment file")
    sys.exit(1)
else:
    UV_PROJECT_ENVIRONMENT = os.getenv("UV_PROJECT_ENVIRONMENT")
    print(f'Use VIRTUAL_ENV: {UV_PROJECT_ENVIRONMENT}')

MODELS_PARAMS_FILE = os.getenv("MODELS_PARAMS_FILE", {})
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
