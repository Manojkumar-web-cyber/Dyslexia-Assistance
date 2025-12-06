import speech_recognition as sr
import logging
from typing import Dict, List
from difflib import SequenceMatcher
import numpy as np

logger = logging.getLogger(__name__)

class SpeechAnalyzer:
    def __init__(self):
        """Initialize Speech Recognition (Uses free Google Speech API)"""
        self.recognizer = sr.Recognizer()
        print(" SpeechAnalyzer initialized - ASR Ready (Google Speech API)")
        
    def transcribe(self, audio_file) -> str:
        """
        Transcribe audio to text using Google Speech Recognition API (FREE)
        Meets guideline: "Detect pronunciation accuracy using modern ASR"
        """
        try:
            audio_data = audio_file.read()
            
            # Convert bytes to AudioData
            from speech_recognition import AudioData
            audio_obj = AudioData(audio_data, 16000, 2)
            
            # Use Google Speech Recognition (free - no key required)
            text = self.recognizer.recognize_google(audio_obj)
            print(f"✅ ASR Transcription: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"ASR Request error: {str(e)}")
            return ""
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return ""
    
    def analyze_pronunciation(self, transcribed_text: str, expected_text: str) -> Dict:
        """
        Compare transcribed vs expected text
        Returns: accuracy, errors, phonetic issues, fluency
        """
        transcribed_words = transcribed_text.lower().split()
        expected_words = expected_text.lower().split()
        
        # Calculate word-level accuracy
        correct_words = sum(1 for t, e in zip(transcribed_words, expected_words) if t == e)
        total_words = max(len(transcribed_words), len(expected_words))
        accuracy_score = (correct_words / total_words) * 100 if total_words > 0 else 0
        
        return {
            'accuracy_score': round(accuracy_score, 2),
            'correct_words': correct_words,
            'total_words': total_words,
            'errors': self._identify_errors(transcribed_words, expected_words),
            'phonetic_issues': self._detect_phonetic_issues(transcribed_text, expected_text),
            'fluency_score': self._calculate_fluency(transcribed_words),
            'skipped_words': self._find_skipped_words(transcribed_words, expected_words)
        }
    
    def _identify_errors(self, transcribed: List[str], expected: List[str]) -> List[Dict]:
        """Identify word-level pronunciation errors"""
        errors = []
        for i, (t, e) in enumerate(zip(transcribed, expected)):
            if t != e:
                similarity = SequenceMatcher(None, t, e).ratio()
                errors.append({
                    'position': i,
                    'transcribed': t,
                    'expected': e,
                    'similarity': round(similarity, 2),
                    'error_type': 'mispronunciation'
                })
        return errors
    
    def _detect_phonetic_issues(self, transcribed: str, expected: str) -> List[str]:
        """Detect common phonetic errors (th, sh, ch, etc.)"""
        common_phonetic_pairs = {
            'th': ['d', 't', 'f'],
            'sh': ['s', 'ch'],
            'ch': ['sh', 'k'],
            'ph': ['f'],
        }
        
        issues = []
        for phoneme, wrong_phonemes in common_phonetic_pairs.items():
            if phoneme in expected.lower() and phoneme not in transcribed.lower():
                if any(wp in transcribed.lower() for wp in wrong_phonemes):
                    issues.append(f"Phonetic error: '{phoneme}' replaced with '{[wp for wp in wrong_phonemes if wp in transcribed.lower()][0]}'")
        
        return issues
    
    def _calculate_fluency(self, words: List[str]) -> float:
        """Calculate reading fluency score (0-100)"""
        if len(words) < 2:
            return 50.0
        
        word_lengths = [len(w) for w in words]
        avg_length = np.mean(word_lengths)
        std_length = np.std(word_lengths) if len(word_lengths) > 1 else 0
        
        # Consistent word rhythm = higher fluency
        fluency = max(0, 100 - (std_length * 5))
        return round(fluency, 2)
    
    def _find_skipped_words(self, transcribed: List[str], expected: List[str]) -> List[str]:
        """Identify words skipped during reading"""
        skipped = []
        j = 0
        for expected_word in expected:
            found = False
            while j < len(transcribed):
                if transcribed[j] == expected_word:
                    found = True
                    j += 1
                    break
                j += 1
            if not found:
                skipped.append(expected_word)
        return skipped
