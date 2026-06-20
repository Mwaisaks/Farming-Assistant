import tempfile
import os
from gtts import gTTS


def _detect_lang(text: str) -> str:
    """Return 'hi' if text contains Devanagari script, else 'en'."""
    for ch in text:
        if "ऀ" <= ch <= "ॿ":
            return "hi"
    return "en"


def speak(text: str, lang: str = None) -> str:
    """Convert text to speech. Returns path to a temporary mp3 file."""
    if lang is None:
        lang = _detect_lang(text)

    tts = gTTS(text=text, lang=lang, slow=False)

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.close()
    tts.save(tmp.name)

    return tmp.name


def cleanup(path: str) -> None:
    """Remove a temp audio file after it has been served."""
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
