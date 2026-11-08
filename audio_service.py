"""
Audio Service for AgroVision
Generates voice advisories for farmers in regional languages using Google Text-to-Speech (gTTS).
Enables accessibility for farmers who prefer audio guidance over text.
"""

import io
from typing import Optional
from gtts import gTTS

def generate_voice_advisory(text: str, lang_code: str = "en") -> Optional[bytes]:
    """
    Convert text advisory into an MP3 byte stream.
    Falls back gracefully if voice synthesis fails.
    """
    if not text or not text.strip():
        return None

    # Sanitize and truncate to avoid excessive network payload
    clean_text = text.strip()[:600]

    # Map supported language code
    supported_gtts_codes = {
        "en": "en",
        "hi": "hi",
        "kn": "kn",
        "te": "te",
        "ta": "ta",
        "mr": "mr",
        "bn": "bn",
        "es": "es"
    }
    target_code = supported_gtts_codes.get(lang_code, "en")

    try:
        tts = gTTS(text=clean_text, lang=target_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        # If specific regional language fails, fallback to English if different
        if target_code != "en":
            try:
                tts = gTTS(text=clean_text, lang="en", slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                return fp.read()
            except Exception:
                pass
    return None
