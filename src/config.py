"""
Configuration settings for the Social Media Sentiment Analysis project.
"""
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Data files
SAMPLE_DATA_FILE = os.path.join(DATA_DIR, 'sample_social_media.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'output_results.csv')

# Sentiment Analysis Settings
SENTIMENT_THRESHOLDS = {
    'positive': 0.05,      # Compound score > 0.05 is positive
    'negative': -0.05,     # Compound score < -0.05 is negative
    'neutral_min': -0.05,  # Between -0.05 and 0.05 is neutral
    'neutral_max': 0.05
}

# Alert System Settings
ALERT_SETTINGS = {
    'negative_threshold': -0.5,     # Flag comments with compound score < -0.5
    'spike_window': 10,             # Number of consecutive negative comments to trigger alert
    'min_negative_ratio': 0.7,      # Minimum ratio of negative comments in window
}

# Visualization Settings
VIZ_SETTINGS = {
    'figure_size': (12, 8),
    'pie_colors': ['#2ecc71', '#95a5a6', '#e74c3c'],  # Green, Gray, Red
    'histogram_bins': 30,
    'dpi': 300,
    'style': 'seaborn-v0_8-darkgrid',
    'max_words_wordcloud': 100,
    'wordcloud_width': 800,
    'wordcloud_height': 400,
}

# Text Preprocessing Settings
PREPROCESSING = {
    'remove_urls': True,
    'remove_mentions': True,
    'remove_hashtags': False,  # Keep hashtags as they contain sentiment
    'remove_special_chars': True,
    'lowercase': True,
    'remove_stopwords': False,  # Keep stopwords for VADER (it uses them)
    'min_text_length': 3,
}

# Supported platforms
SUPPORTED_PLATFORMS = ['Twitter', 'Facebook', 'Instagram', 'Reddit', 'TikTok']

# Output formats
OUTPUT_FORMATS = {
    'csv': True,
    'html_dashboard': True,
    'png_charts': True,
    'pdf_report': False,  # Optional
}
