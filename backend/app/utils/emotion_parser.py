import re
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

def parse_emotion_status(response_text: str) -> Tuple[str, Optional[Dict[str, int]]]:
    """
    Parse emotional status from LLM response text.
    
    Args:
        response_text: The full response text from the LLM
        
    Returns:
        Tuple of (cleaned_response, emotion_status_dict)
        emotion_status_dict contains 'understanding', 'anxiety', 'satisfaction' keys
    """
    pattern = r'\[EMOTION_STATUS\]理解度:(\d+)/10,不安:(\d+)/10,満足度:(\d+)/10\[/EMOTION_STATUS\]'
    
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
            
            logger.info(f"Parsed emotion status: {emotion_status}")
            return cleaned_response, emotion_status
            
        except (ValueError, IndexError) as e:
            logger.error(f"Error parsing emotion status values: {e}")
            return response_text, None
    else:
        logger.warning("No emotion status found in response")
        return response_text, None

def get_default_emotion_status() -> Dict[str, int]:
    """Get default emotional status values"""
    return {
        'understanding': 2,
        'anxiety': 5,
        'satisfaction': 0
    }
