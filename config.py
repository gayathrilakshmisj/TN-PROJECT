import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-secret-key")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Upload configurations
    UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_IMAGE_UPLOAD_MB", 16)) * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

    # Mock & Fallback config
    MOCK_FALLBACK_ON_ERROR = os.getenv("MOCK_FALLBACK_ON_ERROR", "True").lower() in ("true", "1", "yes")

# Ensure upload directory exists
Config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
