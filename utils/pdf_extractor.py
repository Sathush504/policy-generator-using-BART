"""PDF text extraction utilities"""

import PyPDF2
from typing import Optional

def extract_text_from_pdf(pdf_file) -> Optional[str]:
    """
    Extract text content from uploaded PDF file
    
    Args:
        pdf_file: Uploaded file object from Streamlit
        
    Returns:
        Extracted text as string or None if extraction fails
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def get_word_frequency(text: str, top_n: int = 15) -> dict:
    """
    Get most frequent words in text
    
    Args:
        text: Input text
        top_n: Number of top words to return
        
    Returns:
        Dictionary of word: frequency pairs
    """
    import re
    from collections import Counter
    
    # Remove special characters and convert to lowercase
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                  'to', 'for', 'of', 'as', 'by', 'with', 'from', 'is', 'are',
                  'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                  'do', 'does', 'did', 'will', 'would', 'should', 'can', 'could',
                  'may', 'might', 'must', 'shall', 'this', 'that', 'these', 'those'}
    
    filtered_words = [word for word in words if word not in stop_words]
    
    word_freq = Counter(filtered_words)
    return dict(word_freq.most_common(top_n))