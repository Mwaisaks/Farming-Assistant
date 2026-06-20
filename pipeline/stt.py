import os
from groq import Groq

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def transcribe(audio_path: str) -> str:
    """Transcribe audio file to text via Groq Whisper API. Supports Hindi, English, and mixed speech."""
    client = _get_client()
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=f,
        )
    return result.text.strip()
