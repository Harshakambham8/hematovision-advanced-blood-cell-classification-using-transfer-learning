import os
import uuid
from werkzeug.utils import secure_filename
from pathlib import Path
from config import Config

def is_allowed_file(filename: str) -> bool:
    """Check if uploaded filename has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def generate_unique_filename(filename: str) -> str:
    """Generate a sanitized, unique filename to prevent collisions and directory traversal."""
    clean_name = secure_filename(filename)
    unique_prefix = uuid.uuid4().hex[:12]
    return f"{unique_prefix}_{clean_name}"
