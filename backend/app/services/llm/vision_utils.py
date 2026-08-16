import base64
from typing import Tuple

def validate_and_decode_base64_image(base64_str: str) -> Tuple[bool, str]:
    """
    Validates if a string is a valid base64 image payload.
    Returns (is_valid, mime_type_or_error).
    """
    if not base64_str:
        return False, "Empty payload"
    
    clean_str = base64_str
    mime_type = "image/png"
    if "," in base64_str:
        header, clean_str = base64_str.split(",", 1)
        if "image/jpeg" in header:
            mime_type = "image/jpeg"
        elif "image/webp" in header:
            mime_type = "image/webp"

    try:
        decoded = base64.b64decode(clean_str)
        if len(decoded) == 0:
            return False, "Zero byte payload"
        return True, mime_type
    except Exception as e:
        return False, f"Invalid base64 encoding: {str(e)}"
