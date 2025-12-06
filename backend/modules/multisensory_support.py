import re
from typing import Dict, List
import logging
import pyttsx3

logger = logging.getLogger(__name__)

class MultisensorySupportEngine:
    def __init__(self):
        """
        Initialize Multisensory Support Engine
        Meets guideline: "Provide multisensory support (TTS, color cues, hints)"
        Provides: Text-to-speech, visual cues, pronunciation hints, syllable breakdown
        """
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Slower speech for dyslexic readers
            print(" MultisensorySupportEngine initialized - TTS + Visual Support Ready")
        except:
            self.tts_engine = None
        
    def generate_support(self, text: str, support_type: str = 'all') -> Dict:
        """
        Generate comprehensive multisensory support
        """
        support = {}
        
        if support_type in ['all', 'tts']:
            support['tts_url'] = self._generate_tts(text)
        
        if support_type in ['all', 'visual']:
            support['visual_cues'] = self._generate_visual_cues(text)
        
        if support_type in ['all', 'hints']:
            support['hints'] = self._generate_hints(text)
        
        if support_type in ['all']:
            support['syllable_breakdown'] = self._break_into_syllables(text)
        
        print(f"✅ Multisensory support generated: {support_type}")
        return support
    
    def _generate_tts(self, text: str) -> str:
        """Generate text-to-speech locally using pyttsx3 (FREE)"""
        try:
            if self.tts_engine:
                output_file = "/tmp/tts_output.mp3"
                self.tts_engine.save_to_file(text, output_file)
                self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
        
        return f"/api/tts?text={text}"
    
    def _generate_visual_cues(self, text: str) -> Dict:
        """Generate color cues and visual highlights for text"""
        word_cues = []
        for word in text.split():
            cue = {
                'word': word,
                'color': self._get_word_color(word),
                'markers': self._mark_phonemes(word)
            }
            word_cues.append(cue)
        
        return {
            'highlighted_text': text,
            'word_cues': word_cues,
            'phonetic_markers': self._identify_phonetic_markers(text),
            'syllable_marks': self._mark_syllables(text)
        }
    
    def _generate_hints(self, text: str) -> Dict:
        """Generate pronunciation hints for difficult words"""
        hints = {}
        difficult_patterns = ['th', 'ch', 'sh', 'ph', 'gh']
        
        for word in text.split():
            for pattern in difficult_patterns:
                if pattern in word.lower():
                    hints[word] = self._get_pronunciation_hint(word, pattern)
                    break
        
        return hints
    
    def _break_into_syllables(self, text: str) -> Dict:
        """Break words into syllables for pronunciation learning"""
        syllable_breakdown = {}
        
        for word in text.split():
            syllables = self._split_word_syllables(word)
            syllable_breakdown[word] = {
                'syllables': syllables,
                'count': len(syllables),
                'stress_pattern': 'primary'
            }
        
        return syllable_breakdown
    
    def _get_word_color(self, word: str) -> str:
        """Assign color based on word characteristics"""
        vowel_count = sum(1 for char in word.lower() if char in 'aeiou')
        vowel_ratio = vowel_count / len(word) if len(word) > 0 else 0
        
        if vowel_ratio > 0.5:
            return '#FFE6E6'  # Light red - vowel heavy
        elif vowel_ratio < 0.2:
            return '#E6F2FF'  # Light blue - consonant heavy
        else:
            return '#E6FFE6'  # Light green - balanced
    
    def _mark_phonemes(self, word: str) -> List[Dict]:
        """Mark difficult phonemes in a word"""
        phoneme_markers = []
        challenging_phonemes = {
            'th': {'pronunciation': 'theta', 'difficulty': 'high'},
            'ch': {'pronunciation': 'chi', 'difficulty': 'medium'},
            'sh': {'pronunciation': 'sha', 'difficulty': 'medium'},
            'ph': {'pronunciation': 'fa', 'difficulty': 'low'}
        }
        
        for phoneme, info in challenging_phonemes.items():
            if phoneme in word.lower():
                phoneme_markers.append({
                    'phoneme': phoneme,
                    'position': word.lower().find(phoneme),
                    'info': info
                })
        
        return phoneme_markers
    
    def _mark_syllables(self, text: str) -> Dict:
        """Mark syllable boundaries visually"""
        markup = {}
        for word in text.split():
            syllables = self._split_word_syllables(word)
            markup[word] = '•'.join(syllables)
        
        return markup
    
    def _split_word_syllables(self, word: str) -> List[str]:
        """Split word into syllables"""
        syllables = re.split(r'([aeiou]+)', word)
        return [s for s in syllables if s]
    
    def _identify_phonetic_markers(self, text: str) -> List[Dict]:
        """Identify phonetic markers in text"""
        markers = []
        challenging_phonemes = ['th', 'ch', 'sh', 'ph', 'gh']
        
        for phoneme in challenging_phonemes:
            if phoneme in text.lower():
                markers.append({
                    'phoneme': phoneme,
                    'positions': [m.start() for m in re.finditer(phoneme, text.lower())]
                })
        
        return markers
    
    def _get_pronunciation_hint(self, word: str, challenging_part: str) -> Dict:
        """Get specific pronunciation hint for challenging part"""
        hints_db = {
            'th': {'position': 'between teeth', 'tip': 'Place tongue between teeth and voice'},
            'ch': {'position': 'soft palate', 'tip': 'Say "tsh" quickly'},
            'sh': {'position': 'teeth', 'tip': 'Round mouth, air flows over tongue'},
            'ph': {'position': 'lips and teeth', 'tip': 'Same as "f" sound'},
            'gh': {'position': 'silent', 'tip': 'Usually silent in English'}
        }
        
        return hints_db.get(
            challenging_part,
            {'position': 'middle', 'tip': 'Pronounce slowly and carefully'}
        )
