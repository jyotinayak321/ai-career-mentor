from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    APP_NAME: str = "AI Career Mentor"
    DEBUG: bool = True

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "meri-secret-key"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    MONGODB_URL: str = os.getenv(
        "MONGODB_URL",
        "mongodb://localhost:27017"
    )
    DB_NAME: str = "career_mentor_db"

    # Claude AI
    ANTHROPIC_API_KEY: str = os.getenv(
        "ANTHROPIC_API_KEY", ""
    )
    CLAUDE_MODEL: str = "claude-sonnet-4-5"

    # Groq AI (Free!)
    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY", ""
    )
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    FAISS_INDEX_PATH: str = "./faiss_data"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # RapidAPI — Real Jobs
    RAPIDAPI_KEY: str = os.getenv(
        "RAPIDAPI_KEY", ""
    )
    RAPIDAPI_HOST: str = "jsearch.p.rapidapi.com"

settings = Settings()