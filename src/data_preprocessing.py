"""
Text preprocessing module for social media content.
Handles cleaning, normalization, and preparation of text data for sentiment analysis.
"""
import re
import string
from typing import List, Optional
import pandas as pd
from config import PREPROCESSING


class TextPreprocessor:
    """
    Preprocessor for social media text data.
    Cleans and normalizes text while preserving sentiment-relevant information.
    """
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the preprocessor with configuration.
        
        Args:
            config: Optional dictionary with preprocessing settings.
                   If None, uses default settings from config.py
        """
        self.config = config or PREPROCESSING
        
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def remove_mentions(self, text: str) -> str:
        """Remove @mentions from text."""
        return re.sub(r'@\w+', '', text)
    
    def remove_hashtags(self, text: str) -> str:
        """Remove hashtags but keep the text."""
        # Replace #hashtag with hashtag (remove # but keep word)
        return re.sub(r'#(\w+)', r'\1', text)
    
    def remove_special_characters(self, text: str) -> str:
        """Remove special characters except basic punctuation."""
        # Keep basic punctuation that's important for sentiment
        # Remove everything except: letters, numbers, whitespace, and .!?,-
        pattern = r'[^a-zA-Z0-9\s.!?,\-]'
        return re.sub(pattern, '', text)
    
    def remove_extra_whitespace(self, text: str) -> str:
        """Remove extra whitespace and normalize."""
        return ' '.join(text.split())
    
    def handle_emojis(self, text: str) -> str:
        """
        Handle emojis - currently keeps them as VADER can process some emojis.
        Can be extended to convert emojis to text descriptions.
        """
        # For now, keep emojis as VADER handles them
        return text
    
    def clean_text(self, text: str) -> str:
        """
        Apply all preprocessing steps to text.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        if not isinstance(text, str):
            return ""
        
        # Apply preprocessing steps based on configuration
        cleaned = text
        
        if self.config.get('remove_urls', True):
            cleaned = self.remove_urls(cleaned)
        
        if self.config.get('remove_mentions', True):
            cleaned = self.remove_mentions(cleaned)
        
        if self.config.get('remove_hashtags', False):
            cleaned = self.remove_hashtags(cleaned)
        
        cleaned = self.handle_emojis(cleaned)
        
        if self.config.get('remove_special_chars', True):
            cleaned = self.remove_special_characters(cleaned)
        
        if self.config.get('lowercase', True):
            cleaned = cleaned.lower()
        
        cleaned = self.remove_extra_whitespace(cleaned)
        
        # Filter out very short texts
        min_length = self.config.get('min_text_length', 3)
        if len(cleaned.strip()) < min_length:
            return ""
        
        return cleaned.strip()
    
    def preprocess_dataframe(self, df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
        """
        Preprocess all text in a DataFrame.
        
        Args:
            df: DataFrame containing text data
            text_column: Name of the column containing text
            
        Returns:
            DataFrame with additional 'cleaned_text' column
        """
        df = df.copy()
        df['cleaned_text'] = df[text_column].apply(self.clean_text)
        
        # Remove rows with empty cleaned text
        df = df[df['cleaned_text'].str.len() > 0].reset_index(drop=True)
        
        return df
    
    def tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization by splitting on whitespace.
        
        Args:
            text: Input text string
            
        Returns:
            List of tokens
        """
        return text.split()
    
    def get_statistics(self, df: pd.DataFrame, text_column: str = 'text') -> dict:
        """
        Get preprocessing statistics.
        
        Args:
            df: DataFrame with text data
            text_column: Name of the text column
            
        Returns:
            Dictionary with preprocessing statistics
        """
        original_count = len(df)
        df_processed = self.preprocess_dataframe(df, text_column)
        processed_count = len(df_processed)
        
        stats = {
            'original_count': original_count,
            'processed_count': processed_count,
            'removed_count': original_count - processed_count,
            'removal_rate': (original_count - processed_count) / original_count if original_count > 0 else 0,
            'avg_length_before': df[text_column].str.len().mean() if len(df) > 0 else 0,
            'avg_length_after': df_processed['cleaned_text'].str.len().mean() if len(df_processed) > 0 else 0,
        }
        
        return stats


def preprocess_text(text: str) -> str:
    """
    Convenience function to preprocess a single text string.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    preprocessor = TextPreprocessor()
    return preprocessor.clean_text(text)


def preprocess_batch(texts: List[str]) -> List[str]:
    """
    Convenience function to preprocess a batch of texts.
    
    Args:
        texts: List of raw text strings
        
    Returns:
        List of cleaned text strings
    """
    preprocessor = TextPreprocessor()
    return [preprocessor.clean_text(text) for text in texts]
