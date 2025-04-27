# app/utils/file_utils.py

import os

TEMP_TEXT_DIR = "temp/texts"

os.makedirs(TEMP_TEXT_DIR, exist_ok=True)

def save_temp_text_file(session_id: str, text: str) -> str:
    """
    Save uploaded text into a temporary file.
    """
    filepath = os.path.join(TEMP_TEXT_DIR, f"{session_id}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath


# app/utils/file_utils.py (continued)

def load_temp_text(session_id: str) -> str:
    """
    Load saved text from temporary file.
    """
    filepath = os.path.join("temp/texts", f"{session_id}.txt")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
