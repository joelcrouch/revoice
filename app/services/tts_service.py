import pyttsx3

def get_available_voices():
    """
    Fetch available voices from pyttsx3 TTS engine.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    available_voices = []
    
    for voice in voices:
        available_voices.append({
            "id": voice.id,
            "name": voice.name,
            "gender": voice.gender if hasattr(voice, "gender") else "Unknown",
            "language": voice.languages[0] if voice.languages else "Unknown"
        })
    
    engine.stop()
    return available_voices

def synthesize_text(session_id: str, text: str, voice_id: str):
    """
    Synthesize text to speech with the selected voice.
    Save it to a temporary audio file.
    """
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    
    temp_audio_path = f"temp/audio/{session_id}.mp3"
    
    engine.save_to_file(text, temp_audio_path)
    engine.runAndWait()
    
    engine.stop()
    return temp_audio_path
