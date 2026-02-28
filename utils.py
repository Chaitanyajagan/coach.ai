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

import re
from collections import Counter

def calculate_ats_score_local(resume_text, job_desc):
    """
    Calculates ATS score locally without using any external API.
    Performs basic keyword extraction and matching.
    """
    # Define a basic set of stop words to ignore
    stop_words = set([
        "and", "the", "to", "of", "in", "for", "with", "on", "a", "an", "is", "as", 
        "at", "by", "this", "that", "it", "are", "be", "or", "from", "your", "you", 
        "will", "we", "our", "can", "have", "has", "role", "responsibilities", "key", 
        "skills", "experience", "work", "team", "development", "years", "using", "plus"
    ])
    
    # Simple word tokenization functions
    def tokenize(text):
        if not text:
            return []
        # Convert to lowercase and find words
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        # Filter out stop words
        return [w for w in words if w not in stop_words]

    resume_words = tokenize(resume_text)
    jd_words = tokenize(job_desc)
    
    # If job description is empty, return 0
    if not jd_words:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": "Job description is empty. Cannot calculate ATS score."
        }
        
    # Find unique meaningful words
    resume_set = set(resume_words)
    jd_set = set(jd_words)
    
    # Calculate matches
    matched = jd_set.intersection(resume_set)
    missing = jd_set.difference(resume_set)
    
    # Score is the percentage of JD keywords found in the resume
    score = int((len(matched) / len(jd_set)) * 100) if jd_set else 0
    
    # To avoid listing 50 individual words, top 10 matches/missing sorted by length
    # Assuming longer words are more specific skills/tools (e.g. javascript, tensorflow)
    matched_list = sorted(list(matched), key=len, reverse=True)[:15]
    missing_list = sorted(list(missing), key=len, reverse=True)[:15]
    
    # Generate a suggestion based on the score
    suggestions = ""
    if score >= 80:
        suggestions = "Excellent match! Your resume covers most of the key requirements."
    elif score >= 50:
        suggestions = "Good match, but you could improve by adding some of the missing keywords to your resume."
    else:
        suggestions = "Your resume seems to be missing many key requirements from the job description. Consider tailoring it more specifically to this role."

    return {
        "score": score,
        "matched_keywords": [m.capitalize() for m in matched_list],
        "missing_keywords": [m.capitalize() for m in missing_list],
        "suggestions": suggestions
    }
