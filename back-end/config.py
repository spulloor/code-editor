import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Real-Time Collaborative Code Editor"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # not used, but can be in future
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # currently in use
    OLLAMA_URL = os.getenv("OLLAMA_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")

settings = Settings()