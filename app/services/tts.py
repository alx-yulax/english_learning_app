from pathlib import Path
from gtts import gTTS


def generate_tts(text: str, output_path: Path) -> None:
    tts = gTTS(text=text, lang="en")
    tts.save(str(output_path))
