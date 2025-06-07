"""Audio transcription utilities."""

from typing import List
import speech_recognition as sr


def transcribe_audio(audio_path: str) -> List[str]:
    """Transcribe an audio file into a list of sentences.

    Parameters
    ----------
    audio_path:
        Path to an audio file extracted from a video.

    Returns
    -------
    List[str]
        Sentences recognized from the audio.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="zh-CN")
    except sr.UnknownValueError:
        text = ""
    return text.split()
