import re
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

def parse_emotion_status(response_text: str) -> Tuple[str, Optional[Dict[str, int]]]:
    """
    Parse emotional status from LLM response text.
    Supports multiple formats including Japanese with full-width colons, English, and tagged formats.
    
    Args:
        response_text: The full response text from the LLM
        
    Returns:
        Tuple of (cleaned_response, emotion_status_dict)
        emotion_status_dict contains 'understanding', 'anxiety', 'satisfaction' keys
    """
    japanese_simple_pattern = r'理解度：(\d+)/10,?\s*不安：(\d+)/10,?\s*満足度：(\d+)/10'
    
    japanese_simple_colon_pattern = r'理解度:(\d+)/10,?\s*不安:(\d+)/10,?\s*満足度:(\d+)/10'
    
    japanese_pattern = r'\[EMOTION_STATUS\]理解度:(\d+)/10,不安:(\d+)/10,満足度:(\d+)/10\[/EMOTION_STATUS\]'
    
    japanese_pattern_malformed = r'【EMOTION_STATUS\]理解度:(\d+)/10,不安:(\d+)/10,満足度:(\d+)/10】'
    
    japanese_pattern_brackets = r'【EMOTION_STATUS】理解度(\d+)/10,\s*不安(\d+)/10,\s*満足度(\d+)/10'
    
    japanese_natural_pattern = r'理解度(\d+)/10、不安(\d+)/10、満足度(\d+)/10'
    
    english_pattern = r'\[EMOTION_STATUS\]understanding:(\d+)/10,anxiety:(\d+)/10,satisfaction:(\d+)/10\[/EMOTION_STATUS\]'
    
    english_pattern_alt = r'\[EMOTION_STATUS\]Understanding:(\d+)/10,Anxiety:(\d+)/10,Satisfaction:(\d+)/10\[/EMOTION_STATUS\]'
    
    english_simple_pattern = r'understanding:\s*(\d+)/10,?\s*anxiety:\s*(\d+)/10,?\s*satisfaction:\s*(\d+)/10'
    english_simple_cap_pattern = r'Understanding:\s*(\d+)/10,?\s*Anxiety:\s*(\d+)/10,?\s*Satisfaction:\s*(\d+)/10'
    
    patterns_to_try = [
        (japanese_simple_pattern, 'Japanese-simple-fullwidth'),
        (japanese_simple_colon_pattern, 'Japanese-simple-colon'),
        (japanese_natural_pattern, 'Japanese-natural'),
        (japanese_pattern_brackets, 'Japanese-brackets'),
        (japanese_pattern, 'Japanese-tagged'),
        (japanese_pattern_malformed, 'Japanese-malformed'),
        (english_simple_pattern, 'English-simple'),
        (english_simple_cap_pattern, 'English-simple-cap'),
        (english_pattern, 'English-tagged'),
        (english_pattern_alt, 'English-tagged-alt')
    ]
    
    for pattern, pattern_name in patterns_to_try:
        match = re.search(pattern, response_text)
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
                
                cleaned_response = re.sub(pattern, '', response_text).strip()
                
                logger.info(f"Parsed emotion status: {emotion_status} (pattern: {pattern_name})")
                return cleaned_response, emotion_status
                
            except (ValueError, IndexError) as e:
                logger.error(f"Error parsing emotion status values: {e}")
                continue
    
    logger.warning("No emotion status found in response (tried all Japanese and English patterns)")
    return response_text, None

def get_default_emotion_status() -> Dict[str, int]:
    """Get default emotional status values"""
    return {
        'understanding': 2,
        'anxiety': 5,
        'satisfaction': 0
    }
