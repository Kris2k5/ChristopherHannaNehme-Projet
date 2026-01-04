# Data Directory

## Overview
This directory contains sample social media data and analysis outputs for the sentiment analysis project.

## Files

### `sample_social_media.csv`
Sample social media dataset with 100+ entries for testing and demonstration.

**Columns:**
- `text`: The social media post/comment content
- `timestamp`: Date and time of the post
- `platform`: Social media platform (Twitter, Facebook, Instagram, Reddit)
- `product_mention`: Product or brand mentioned in the post

**Sentiment Mix:**
- Approximately 40% positive sentiments
- Approximately 30% neutral sentiments
- Approximately 30% negative sentiments

### `output_results.csv` (Generated)
Output file created after running sentiment analysis. Contains all original columns plus:
- `compound_score`: Overall sentiment score (-1 to 1)
- `positive_score`: Positive sentiment component (0 to 1)
- `neutral_score`: Neutral sentiment component (0 to 1)
- `negative_score`: Negative sentiment component (0 to 1)
- `sentiment`: Classification (Positive, Negative, or Neutral)

## Data Sources
The sample data is synthetic and created for demonstration purposes. It represents typical social media content patterns including:
- Product reviews and opinions
- Emojis and informal language
- Mix of sentiment polarities
- Different platform styles

## Usage

### Loading Data
```python
import pandas as pd

# Load sample data
df = pd.read_csv('data/sample_social_media.csv')
print(f"Loaded {len(df)} social media posts")
```

### Data Characteristics
- **Total Entries**: 100+
- **Time Range**: January 15-16, 2024
- **Platforms**: Twitter, Facebook, Instagram, Reddit
- **Language**: English
- **Format**: CSV with UTF-8 encoding

## Privacy & Ethics
All data in this project is synthetic and does not contain real user information or personally identifiable information (PII).

## Extending the Dataset
To add your own data, ensure your CSV file includes:
1. A `text` column with the content to analyze
2. Optional: `timestamp` column for time-series analysis
3. Optional: `platform` column for platform comparison
4. Optional: Any other metadata columns

The sentiment analyzer will automatically process any column named `text` and add sentiment scores.
