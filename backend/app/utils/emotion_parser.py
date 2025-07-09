import re
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

def parse_emotion_status(response_text: str) -> Tuple[str, Optional[Dict[str, int]]]:
    """
    Parse emotional status from LLM response text.
    Supports both Japanese and English formats.
    
    Args:
        response_text: The full response text from the LLM
        
    Returns:
        Tuple of (cleaned_response, emotion_status_dict)
        emotion_status_dict contains 'understanding', 'anxiety', 'satisfaction' keys
    """
    japanese_pattern = r'\[EMOTION_STATUS\]理解度:(\d+)/10,不安:(\d+)/10,満足度:(\d+)/10\[/EMOTION_STATUS\]'
    
    english_pattern = r'\[EMOTION_STATUS\]understanding:(\d+)/10,anxiety:(\d+)/10,satisfaction:(\d+)/10\[/EMOTION_STATUS\]'
    
    english_pattern_alt = r'\[EMOTION_STATUS\]Understanding:(\d+)/10,Anxiety:(\d+)/10,Satisfaction:(\d+)/10\[/EMOTION_STATUS\]'
    
    match = re.search(japanese_pattern, response_text)
    pattern_used = japanese_pattern
    
    if not match:
        match = re.search(english_pattern, response_text)
        pattern_used = english_pattern
        
    if not match:
        match = re.search(english_pattern_alt, response_text)
        pattern_used = english_pattern_alt
    
    if match:
        try:
            understanding = int(match.group(1))
            anxiety = int(match.group(2))
            satisfaction = int(match.group(3))
            
            understanding = max(0, min(10, understanding))
            anxiety = max(0, min(10, anxiety))
            satisfaction = max(0, min(10, satisfaction))
            
            emotion_status = {
                'understanding': understanding,
                'anxiety': anxiety,
                'satisfaction': satisfaction
            }
            
            cleaned_response = re.sub(pattern_used, '', response_text).strip()
            
            logger.info(f"Parsed emotion status: {emotion_status} (pattern: {'Japanese' if pattern_used == japanese_pattern else 'English'})")
            return cleaned_response, emotion_status
            
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing emotion status values: {e}")
            return response_text, None
    else:
        logger.warning("No emotion status found in response (tried Japanese and English patterns)")
        return response_text, None

def get_default_emotion_status() -> Dict[str, int]:
    """Get default emotional status values"""
    return {
        'understanding': 2,
        'anxiety': 5,
        'satisfaction': 0
    }
