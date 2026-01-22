import streamlit as st
import pyttsx3
import threading
import speech_recognition as sr
import pythoncom

from streamlit.runtime.scriptrunner import add_script_run_ctx

# Global TTS Engine Reference
tts_engine = None

import os
import uuid

def speak(text):
    # Backward compatibility or fallback (Optional: could just pass)
    pass

def text_to_speech_file(text):
    """
    Generates audio file using pyttsx3 and returns the bytes.
    """
    try:
        engine = pyttsx3.init()
        # Temp file
        filename = f"temp_{uuid.uuid4()}.wav"
        
        # Configure voice
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 145)
        
        # Save to file
        engine.save_to_file(text, filename)
        engine.runAndWait()
        
        # Read bytes
        with open(filename, "rb") as f:
            data = f.read()
            
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)
            
        return data
        
    except Exception as e:
        print(f"TTS Generation Error: {e}")
        return None

def stop_voice_now():
    """Forcefully stop the global engine."""
    global tts_engine
    
    # Set flag
    if 'shutup' in st.session_state:
        st.session_state['shutup'] = True
    
    # Direct stop (might fail across threads but worth a shot)
    if tts_engine:
        try:
            tts_engine.stop()
        except: pass

import io

def transcribe_audio_bytes(audio_bytes):
    """
    Transcribes audio bytes (WAV) using SpeechRecognition.
    """
    try:
        r = sr.Recognizer()
        
        # Convert bytes to file-like object
        audio_file = io.BytesIO(audio_bytes)
        
        with sr.AudioFile(audio_file) as source:
            # Record the data from the file
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
            
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"Transcription Error: {e}")
        return None
