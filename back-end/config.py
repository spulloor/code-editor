import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Real-Time Collaborative Code Editor"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()