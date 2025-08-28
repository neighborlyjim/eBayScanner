# utils.py - Common utility functions to avoid code duplication
from datetime import datetime, timezone
import re

def calculate_time_left(end_time_str):
    """Calculate time left from eBay end time string"""
    try:
        # Parse eBay datetime format
        end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        diff = end_time - now
        
        if diff.total_seconds() <= 0:
            return "Ended"
            
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes} minutes"
            
    except Exception as e:
        return "Unknown"

def extract_model_from_title(title):
    """Extract model/brand from title"""
    # Simple extraction - you could make this more sophisticated
    words = title.split()
    for i, word in enumerate(words):
        if len(word) > 2 and (word.isupper() or any(char.isdigit() for char in word)):
            return ' '.join(words[i:i+2])
    return words[0] if words else "Unknown"

def format_price(price):
    """Format price consistently"""
    try:
        return f"${float(price):.2f}"
    except (ValueError, TypeError):
        return "N/A"

def safe_get_attribute(obj, attr_path, default=None):
    """Safely get nested attributes from objects"""
    try:
        attrs = attr_path.split('.')
        result = obj
        for attr in attrs:
            result = getattr(result, attr)
        return result
    except (AttributeError, TypeError):
        return default

def calculate_discount_percentage(original_price, current_price):
    """Calculate discount percentage between two prices"""
    try:
        original = float(original_price)
        current = float(current_price)
        if original <= 0:
            return 0
        return int(((original - current) / original) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def validate_search_query(query):
    """Validate and sanitize search queries"""
    if not query or not isinstance(query, str):
        return None
    
    # Remove special characters that might cause issues
    cleaned = re.sub(r'[<>{}[\]\\]', '', query.strip())
    
    # Ensure minimum length
    if len(cleaned) < 2:
        return None
        
    return cleaned

def determine_urgency(time_left_str):
    """Determine urgency level based on time left"""
    if not time_left_str or time_left_str == "Unknown":
        return "low"
    
    if "minute" in time_left_str.lower():
        try:
            minutes = int(time_left_str.split()[0])
            return "critical" if minutes < 30 else "high"
        except (ValueError, IndexError):
            return "medium"
    elif "h" in time_left_str.lower() and "d" not in time_left_str.lower():
        return "high"
    else:
        return "medium"
