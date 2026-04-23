"""Text summarization using BART transformer model"""

from transformers import pipeline
import torch

class PolicySummarizer:
    def __init__(self):
        """Initialize BART summarization model"""
        self.device = 0 if torch.cuda.is_available() else -1
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=self.device
            )
        except Exception as e:
            print(f"Error loading model: {e}")
            self.summarizer = None
    
    def chunk_text(self, text: str, max_chunk_size: int = 1024) -> list:
        """
        Split text into manageable chunks
        
        Args:
            text: Input text
            max_chunk_size: Maximum words per chunk
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), max_chunk_size):
            chunk = ' '.join(words[i:i + max_chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def extractive_summarize(self, text: str, num_sentences: int = 5) -> str:
        """
        Simple extractive summarization
        
        Args:
            text: Input text
            num_sentences: Number of sentences to extract
            
        Returns:
            Summary text
        """
        import re
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) <= num_sentences:
            return '. '.join(sentences) + '.'
        
        # Simple scoring based on word frequency
        from collections import Counter
        words = re.findall(r'\b[a-z]+\b', text.lower())
        word_freq = Counter(words)
        
        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            score = sum(word_freq.get(word.lower(), 0) 
                       for word in re.findall(r'\b[a-z]+\b', sentence.lower()))
            sentence_scores.append((score, sentence))
        
        # Get top sentences
        sentence_scores.sort(reverse=True)
        top_sentences = [s[1] for s in sentence_scores[:num_sentences]]
        
        return '. '.join(top_sentences) + '.'
    
    def abstractive_summarize(self, text: str, max_length: int = 500, 
                             min_length: int = 100) -> str:
        """
        Abstractive summarization using BART
        
        Args:
            text: Input text
            max_length: Maximum summary length
            min_length: Minimum summary length
            
        Returns:
            Summary text
        """
        if not self.summarizer:
            return "Summarization model not available"
        
        try:
            # Handle long texts by chunking
            chunks = self.chunk_text(text, max_chunk_size=1024)
            summaries = []
            
            for chunk in chunks[:5]:  # Limit to first 5 chunks
                summary = self.summarizer(
                    chunk,
                    max_length=max_length // len(chunks[:5]),
                    min_length=min_length // len(chunks[:5]),
                    do_sample=False
                )[0]['summary_text']
                summaries.append(summary)
            
            return ' '.join(summaries)
        
        except Exception as e:
            print(f"Error in abstractive summarization: {e}")
            return self.extractive_summarize(text)
    
    def structured_summarize(self, text: str) -> dict:
        """
        Create structured summary with multiple sections
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with structured summary
        """
        summary = {
            "main_goals": "",
            "key_measures": "",
            "overall_direction": ""
        }
        
        # Try to identify sections
        import re
        
        # Look for common section headers
        goals_pattern = r'(goal|objective|purpose|aim)s?[\s\S]{100,1000}'
        measures_pattern = r'(measure|strategy|action|implementation)s?[\s\S]{100,1000}'
        
        goals_match = re.search(goals_pattern, text, re.IGNORECASE)
        measures_match = re.search(measures_pattern, text, re.IGNORECASE)
        
        if goals_match:
            summary["main_goals"] = self.extractive_summarize(
                goals_match.group(), num_sentences=3
            )
        else:
            # Use first part of document
            summary["main_goals"] = self.extractive_summarize(
                text[:2000], num_sentences=3
            )
        
        if measures_match:
            summary["key_measures"] = self.extractive_summarize(
                measures_match.group(), num_sentences=3
            )
        else:
            # Use middle part of document
            mid = len(text) // 2
            summary["key_measures"] = self.extractive_summarize(
                text[mid:mid+2000], num_sentences=3
            )
        
        # Overall direction from abstractive summary
        if self.summarizer:
            summary["overall_direction"] = self.abstractive_summarize(
                text, max_length=200, min_length=50
            )
        else:
            summary["overall_direction"] = self.extractive_summarize(
                text, num_sentences=3
            )
        
        return summary