"""
Sentiment Analysis Engine using VADER (Valence Aware Dictionary and sEntiment Reasoner).
VADER is specifically designed for social media text and handles emojis, slang, and intensifiers.
"""
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from data_preprocessing import TextPreprocessor
from config import SENTIMENT_THRESHOLDS


class SentimentAnalyzer:
    """
    Main sentiment analysis engine using VADER.
    Provides sentiment classification and scoring for social media text.
    """
    
    def __init__(self, use_preprocessing: bool = True):
        """
        Initialize the sentiment analyzer.
        
        Args:
            use_preprocessing: Whether to preprocess text before analysis
        """
        self.vader = SentimentIntensityAnalyzer()
        self.use_preprocessing = use_preprocessing
        self.preprocessor = TextPreprocessor() if use_preprocessing else None
        self.thresholds = SENTIMENT_THRESHOLDS
        
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with sentiment scores:
            - compound: Overall sentiment score (-1 to 1)
            - pos: Positive score (0 to 1)
            - neu: Neutral score (0 to 1)
            - neg: Negative score (0 to 1)
        """
        if not isinstance(text, str) or not text.strip():
            return {
                'compound': 0.0,
                'pos': 0.0,
                'neu': 1.0,
                'neg': 0.0
            }
        
        # Optionally preprocess
        if self.use_preprocessing and self.preprocessor:
            text = self.preprocessor.clean_text(text)
            if not text:
                return {
                    'compound': 0.0,
                    'pos': 0.0,
                    'neu': 1.0,
                    'neg': 0.0
                }
        
        # Get VADER scores
        scores = self.vader.polarity_scores(text)
        return scores
    
    def classify_sentiment(self, compound_score: float) -> str:
        """
        Classify sentiment based on compound score.
        
        Args:
            compound_score: VADER compound score (-1 to 1)
            
        Returns:
            Sentiment label: 'Positive', 'Negative', or 'Neutral'
        """
        if compound_score >= self.thresholds['positive']:
            return 'Positive'
        elif compound_score <= self.thresholds['negative']:
            return 'Negative'
        else:
            return 'Neutral'
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Analyze sentiment for a batch of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of sentiment score dictionaries
        """
        return [self.analyze_text(text) for text in texts]
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
        """
        Analyze sentiment for all texts in a DataFrame.
        
        Args:
            df: DataFrame containing text data
            text_column: Name of the column containing text
            
        Returns:
            DataFrame with added sentiment columns
        """
        df = df.copy()
        
        # Apply sentiment analysis
        sentiment_scores = df[text_column].apply(self.analyze_text)
        
        # Extract individual scores
        df['compound_score'] = sentiment_scores.apply(lambda x: x['compound'])
        df['positive_score'] = sentiment_scores.apply(lambda x: x['pos'])
        df['neutral_score'] = sentiment_scores.apply(lambda x: x['neu'])
        df['negative_score'] = sentiment_scores.apply(lambda x: x['neg'])
        
        # Classify sentiment
        df['sentiment'] = df['compound_score'].apply(self.classify_sentiment)
        
        return df
    
    def get_sentiment_summary(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Get summary statistics of sentiment analysis.
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Dictionary with summary statistics
        """
        if 'sentiment' not in df.columns:
            return {}
        
        total = len(df)
        sentiment_counts = df['sentiment'].value_counts()
        
        summary = {
            'total_analyzed': total,
            'positive_count': sentiment_counts.get('Positive', 0),
            'negative_count': sentiment_counts.get('Negative', 0),
            'neutral_count': sentiment_counts.get('Neutral', 0),
            'positive_percentage': (sentiment_counts.get('Positive', 0) / total * 100) if total > 0 else 0,
            'negative_percentage': (sentiment_counts.get('Negative', 0) / total * 100) if total > 0 else 0,
            'neutral_percentage': (sentiment_counts.get('Neutral', 0) / total * 100) if total > 0 else 0,
            'avg_compound_score': df['compound_score'].mean() if 'compound_score' in df.columns else 0,
            'avg_positive_score': df['positive_score'].mean() if 'positive_score' in df.columns else 0,
            'avg_negative_score': df['negative_score'].mean() if 'negative_score' in df.columns else 0,
            'avg_neutral_score': df['neutral_score'].mean() if 'neutral_score' in df.columns else 0,
        }
        
        return summary
    
    def get_top_sentiments(
        self, 
        df: pd.DataFrame, 
        sentiment_type: str = 'positive', 
        n: int = 10,
        text_column: str = 'text'
    ) -> pd.DataFrame:
        """
        Get top N most positive or negative comments.
        
        Args:
            df: DataFrame with sentiment analysis results
            sentiment_type: 'positive' or 'negative'
            n: Number of top comments to return
            text_column: Name of the text column
            
        Returns:
            DataFrame with top N comments
        """
        if 'compound_score' not in df.columns:
            return pd.DataFrame()
        
        # Sort based on sentiment type
        if sentiment_type.lower() == 'positive':
            sorted_df = df.nlargest(n, 'compound_score')
        else:  # negative
            sorted_df = df.nsmallest(n, 'compound_score')
        
        # Return relevant columns
        columns = [text_column, 'compound_score', 'sentiment']
        if 'platform' in df.columns:
            columns.append('platform')
        if 'timestamp' in df.columns:
            columns.append('timestamp')
        
        return sorted_df[columns].reset_index(drop=True)
    
    def analyze_by_platform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get sentiment summary grouped by platform.
        
        Args:
            df: DataFrame with sentiment results and 'platform' column
            
        Returns:
            DataFrame with sentiment statistics per platform
        """
        if 'platform' not in df.columns or 'sentiment' not in df.columns:
            return pd.DataFrame()
        
        platform_stats = []
        
        for platform in df['platform'].unique():
            platform_df = df[df['platform'] == platform]
            summary = self.get_sentiment_summary(platform_df)
            summary['platform'] = platform
            platform_stats.append(summary)
        
        return pd.DataFrame(platform_stats)
    
    def analyze_time_series(
        self, 
        df: pd.DataFrame, 
        timestamp_column: str = 'timestamp',
        freq: str = 'D'
    ) -> pd.DataFrame:
        """
        Analyze sentiment over time.
        
        Args:
            df: DataFrame with sentiment results and timestamp
            timestamp_column: Name of the timestamp column
            freq: Frequency for grouping ('D' for day, 'H' for hour, etc.)
            
        Returns:
            DataFrame with time-series sentiment statistics
        """
        if timestamp_column not in df.columns or 'compound_score' not in df.columns:
            return pd.DataFrame()
        
        df = df.copy()
        df[timestamp_column] = pd.to_datetime(df[timestamp_column])
        df.set_index(timestamp_column, inplace=True)
        
        # Resample and aggregate
        time_series = df.resample(freq).agg({
            'compound_score': ['mean', 'count'],
            'positive_score': 'mean',
            'negative_score': 'mean',
            'neutral_score': 'mean'
        })
        
        time_series.columns = ['_'.join(col).strip() for col in time_series.columns.values]
        time_series = time_series.reset_index()
        
        return time_series


def quick_analyze(text: str) -> Tuple[str, float]:
    """
    Quick convenience function to analyze a single text.
    
    Args:
        text: Input text string
        
    Returns:
        Tuple of (sentiment_label, compound_score)
    """
    analyzer = SentimentAnalyzer()
    scores = analyzer.analyze_text(text)
    sentiment = analyzer.classify_sentiment(scores['compound'])
    return sentiment, scores['compound']
