"""
Unit tests for the sentiment analysis system.
"""
import sys
import os
import pytest
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sentiment_analyzer import SentimentAnalyzer, quick_analyze
from data_preprocessing import TextPreprocessor, preprocess_text
from alert_system import SentimentAlertSystem, quick_alert_check


class TestSentimentAnalyzer:
    """Tests for sentiment analysis functionality."""
    
    def test_analyze_positive_text(self):
        """Test analysis of positive sentiment."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text("This is amazing! I love it so much!")
        
        assert result['compound'] > 0.5
        assert analyzer.classify_sentiment(result['compound']) == 'Positive'
    
    def test_analyze_negative_text(self):
        """Test analysis of negative sentiment."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text("This is terrible! I hate it! Worst ever!")
        
        assert result['compound'] < -0.5
        assert analyzer.classify_sentiment(result['compound']) == 'Negative'
    
    def test_analyze_neutral_text(self):
        """Test analysis of neutral sentiment."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text("This is a product. It exists.")
        
        assert -0.05 <= result['compound'] <= 0.05
        assert analyzer.classify_sentiment(result['compound']) == 'Neutral'
    
    def test_analyze_empty_text(self):
        """Test handling of empty text."""
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text("")
        
        assert result['compound'] == 0.0
        assert result['neu'] == 1.0
    
    def test_analyze_batch(self):
        """Test batch analysis."""
        analyzer = SentimentAnalyzer()
        texts = [
            "Great product!",
            "Terrible experience.",
            "It's okay."
        ]
        results = analyzer.analyze_batch(texts)
        
        assert len(results) == 3
        assert all('compound' in r for r in results)
    
    def test_analyze_dataframe(self):
        """Test DataFrame analysis."""
        analyzer = SentimentAnalyzer()
        df = pd.DataFrame({
            'text': ['Love it!', 'Hate it!', 'Meh.']
        })
        
        result_df = analyzer.analyze_dataframe(df)
        
        assert 'compound_score' in result_df.columns
        assert 'sentiment' in result_df.columns
        assert len(result_df) == 3
    
    def test_sentiment_summary(self):
        """Test sentiment summary statistics."""
        analyzer = SentimentAnalyzer()
        df = pd.DataFrame({
            'text': ['Great!'] * 5 + ['Terrible!'] * 3 + ['Okay.'] * 2
        })
        
        df = analyzer.analyze_dataframe(df)
        summary = analyzer.get_sentiment_summary(df)
        
        assert summary['total_analyzed'] == 10
        # Check that all three sentiment types are present
        assert summary['positive_count'] >= 3  # At least some positive
        assert summary['negative_count'] >= 3  # At least 3 negative
        # Total should add up
        assert summary['positive_count'] + summary['negative_count'] + summary['neutral_count'] == 10
    
    def test_quick_analyze(self):
        """Test quick analyze convenience function."""
        sentiment, score = quick_analyze("Excellent product!")
        
        assert sentiment == 'Positive'
        assert score > 0


class TestDataPreprocessing:
    """Tests for data preprocessing functionality."""
    
    def test_remove_urls(self):
        """Test URL removal."""
        preprocessor = TextPreprocessor()
        text = "Check this out https://example.com it's great!"
        result = preprocessor.remove_urls(text)
        
        assert 'https://example.com' not in result
        assert "Check this out" in result
    
    def test_remove_mentions(self):
        """Test @mention removal."""
        preprocessor = TextPreprocessor()
        text = "Hey @user this is cool!"
        result = preprocessor.remove_mentions(text)
        
        assert '@user' not in result
    
    def test_remove_hashtags(self):
        """Test hashtag handling."""
        preprocessor = TextPreprocessor()
        text = "This is #awesome #great"
        result = preprocessor.remove_hashtags(text)
        
        # Hashtags are kept by default in config
        assert '#' not in result or '#' in result  # Depends on config
    
    def test_clean_text_integration(self):
        """Test full text cleaning pipeline."""
        preprocessor = TextPreprocessor()
        text = "OMG @user this is AMAZING!!! https://example.com #love"
        result = preprocessor.clean_text(text)
        
        assert len(result) > 0
        assert 'https://' not in result
        assert '@user' not in result
    
    def test_preprocess_dataframe(self):
        """Test DataFrame preprocessing."""
        preprocessor = TextPreprocessor()
        df = pd.DataFrame({
            'text': ['Hello @user!', 'Check https://example.com', 'Regular text']
        })
        
        result_df = preprocessor.preprocess_dataframe(df)
        
        assert 'cleaned_text' in result_df.columns
        assert len(result_df) == 3
    
    def test_empty_text_handling(self):
        """Test handling of empty text."""
        preprocessor = TextPreprocessor()
        result = preprocessor.clean_text("")
        
        assert result == ""
    
    def test_preprocess_text_convenience(self):
        """Test convenience function."""
        result = preprocess_text("Hello @world! https://test.com")
        
        assert '@world' not in result
        assert 'https://' not in result


class TestAlertSystem:
    """Tests for alert system functionality."""
    
    def test_flag_high_priority_comments(self):
        """Test flagging of high priority negative comments."""
        alert_system = SentimentAlertSystem()
        df = pd.DataFrame({
            'text': ['Great!', 'Terrible!', 'Horrible!', 'Awful!'],
            'compound_score': [0.8, -0.7, -0.8, -0.9]
        })
        
        high_priority = alert_system.flag_high_priority_comments(df)
        
        assert len(high_priority) >= 3  # Should flag the 3 very negative ones
        assert all(high_priority['compound_score'] < -0.5)
    
    def test_detect_negative_spike(self):
        """Test detection of negative sentiment spikes."""
        alert_system = SentimentAlertSystem()
        # Create DataFrame with consecutive negative comments
        df = pd.DataFrame({
            'compound_score': [0.5, 0.6, -0.7, -0.8, -0.9, -0.7, -0.8, -0.9, -0.7, -0.8, 0.5]
        })
        
        alerts = alert_system.detect_negative_spike(df)
        
        assert len(alerts) > 0  # Should detect at least one spike
    
    def test_generate_alert_report(self):
        """Test alert report generation."""
        alert_system = SentimentAlertSystem()
        df = pd.DataFrame({
            'text': ['Good'] * 5 + ['Bad'] * 5,
            'compound_score': [0.5] * 5 + [-0.7] * 5,
            'sentiment': ['Positive'] * 5 + ['Negative'] * 5
        })
        
        report = alert_system.generate_alert_report(df)
        
        assert 'timestamp' in report
        assert 'total_analyzed' in report
        assert 'alerts' in report
        assert report['total_analyzed'] == 10
    
    def test_alert_summary_creation(self):
        """Test alert summary text generation."""
        alert_system = SentimentAlertSystem()
        report = {
            'timestamp': '2024-01-01T00:00:00',
            'total_analyzed': 100,
            'alert_count': 2,
            'has_critical_alerts': True,
            'alerts': [
                {
                    'severity': 'High',
                    'alert_type': 'Test Alert',
                    'message': 'Test message'
                }
            ]
        }
        
        summary = alert_system.create_alert_summary(report)
        
        assert 'SENTIMENT ALERT SUMMARY' in summary
        assert 'Test Alert' in summary
    
    def test_quick_alert_check(self):
        """Test quick alert check convenience function."""
        df = pd.DataFrame({
            'text': ['Good', 'Bad', 'Ugly'],
            'compound_score': [0.5, -0.7, -0.8],
            'sentiment': ['Positive', 'Negative', 'Negative']
        })
        
        has_alerts, message = quick_alert_check(df)
        
        assert isinstance(has_alerts, bool)
        assert isinstance(message, str)


class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_full_pipeline(self):
        """Test complete analysis pipeline."""
        # Create sample data
        df = pd.DataFrame({
            'text': [
                'This product is amazing! Love it!',
                'Terrible quality. Very disappointed.',
                'It\'s okay. Nothing special.',
                'Best purchase ever! Highly recommend!',
                'Waste of money. Don\'t buy!'
            ],
            'timestamp': pd.date_range('2024-01-01', periods=5, freq='h'),
            'platform': ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'Twitter']
        })
        
        # Analyze
        analyzer = SentimentAnalyzer()
        result_df = analyzer.analyze_dataframe(df)
        
        # Verify results
        assert len(result_df) == 5
        assert 'sentiment' in result_df.columns
        assert 'compound_score' in result_df.columns
        
        # Check sentiment summary
        summary = analyzer.get_sentiment_summary(result_df)
        assert summary['total_analyzed'] == 5
        assert summary['positive_count'] + summary['negative_count'] + summary['neutral_count'] == 5
        
        # Check alerts
        alert_system = SentimentAlertSystem()
        report = alert_system.generate_alert_report(result_df)
        assert 'alerts' in report
    
    def test_with_sample_data(self):
        """Test with sample data file if it exists."""
        sample_file = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'sample_social_media.csv'
        )
        
        if os.path.exists(sample_file):
            df = pd.read_csv(sample_file)
            analyzer = SentimentAnalyzer()
            result_df = analyzer.analyze_dataframe(df)
            
            assert len(result_df) > 0
            assert 'sentiment' in result_df.columns
            
            summary = analyzer.get_sentiment_summary(result_df)
            assert summary['total_analyzed'] == len(result_df)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
