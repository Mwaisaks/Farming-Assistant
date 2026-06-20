import whisper

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def transcribe(audio_path: str) -> str:
    """Transcribe audio file to text. Supports Hindi, English, and mixed speech."""
    model = _load_model()
    result = model.transcribe(audio_path, task="transcribe")
    return result["text"].strip()
