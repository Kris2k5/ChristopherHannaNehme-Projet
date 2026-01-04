# 🎯 Social Media Sentiment Analysis System

A production-ready machine learning project for analyzing sentiment in social media content to assess public response to promotions and brand mentions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![VADER](https://img.shields.io/badge/sentiment-VADER-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Overview

This system performs real-time sentiment analysis on social media posts from platforms like Twitter, Facebook, Instagram, and Reddit. It uses VADER (Valence Aware Dictionary and sEntiment Reasoner), specifically optimized for social media text, to classify content as positive, negative, or neutral.

### Key Features

✅ **Sentiment Analysis Engine**
- VADER-based sentiment scoring optimized for social media
- Handles emojis, slang, and informal language
- Real-time and batch processing capabilities
- Multi-platform support (Twitter, Facebook, Instagram, Reddit)

✅ **Advanced Text Preprocessing**
- URL and mention removal
- Emoji handling
- Special character normalization
- Text standardization

✅ **Rich Visualizations**
- Sentiment distribution pie charts
- Score histograms
- Time-series trend analysis
- Word clouds for positive/negative content
- Platform comparison charts
- Interactive HTML dashboards

✅ **Alert System**
- Negative sentiment spike detection
- High-priority comment flagging
- Platform-specific alerts
- Automated alert reports

✅ **Production Ready**
- Comprehensive unit tests
- Clean, modular code
- Detailed documentation
- Easy to deploy and maintain

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Kris2k5/ChristopherHannaNehme-Projet.git
cd ChristopherHannaNehme-Projet
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data (required for VADER)**
```python
import nltk
nltk.download('vader_lexicon')
```

### Basic Usage

```python
import pandas as pd
from src.sentiment_analyzer import SentimentAnalyzer
from src.visualization import SentimentVisualizer
from src.alert_system import SentimentAlertSystem

# Load data
df = pd.read_csv('data/sample_social_media.csv')

# Analyze sentiment
analyzer = SentimentAnalyzer()
results = analyzer.analyze_dataframe(df)

# Get summary statistics
summary = analyzer.get_sentiment_summary(results)
print(summary)

# Generate visualizations
visualizer = SentimentVisualizer()
visualizer.plot_sentiment_distribution(results)
visualizer.generate_dashboard(results, summary)

# Check for alerts
alert_system = SentimentAlertSystem()
report = alert_system.generate_alert_report(results)
print(alert_system.create_alert_summary(report))

# Save results
results.to_csv('data/output_results.csv', index=False)
```

### Quick Analysis

```python
from src.sentiment_analyzer import quick_analyze

sentiment, score = quick_analyze("This product is amazing! Love it!")
print(f"Sentiment: {sentiment}, Score: {score:.3f}")
# Output: Sentiment: Positive, Score: 0.836
```

## 📁 Project Structure

```
ChristopherHannaNehme-Projet/
├── README.md                          # This file
├── product_specification.md           # Detailed product specification
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── data/
│   ├── sample_social_media.csv       # Sample dataset (100+ entries)
│   ├── output_results.csv            # Analysis results (generated)
│   └── README.md                     # Data documentation
│
├── src/
│   ├── __init__.py
│   ├── config.py                     # Configuration settings
│   ├── sentiment_analyzer.py         # Main sentiment engine
│   ├── data_preprocessing.py         # Text preprocessing
│   ├── visualization.py              # Charts & dashboards
│   └── alert_system.py               # Alert detection
│
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py              # Unit tests
│
├── notebooks/
│   └── sentiment_analysis_demo.ipynb # Interactive demo
│
├── results/                          # Generated visualizations
│   └── .gitkeep
│
└── docs/
    ├── presentation_guide.md         # 5-minute presentation guide
    └── qa_preparation.md             # Q&A preparation
```

## 🔧 Technologies Used

- **Python 3.8+**: Core programming language
- **VADER Sentiment**: Social media-optimized sentiment analysis
- **pandas**: Data manipulation and analysis
- **matplotlib/seaborn**: Data visualization
- **WordCloud**: Text visualization
- **NLTK**: Natural language processing toolkit
- **pytest**: Testing framework
- **Jupyter**: Interactive notebooks

## 📊 How It Works

### 1. Data Preprocessing
- Removes URLs, mentions, and special characters
- Normalizes text while preserving sentiment indicators
- Handles emojis and emoticons

### 2. Sentiment Analysis
- Uses VADER algorithm optimized for social media
- Generates compound score (-1 to 1)
- Classifies as Positive (>0.05), Negative (<-0.05), or Neutral

### 3. Visualization
- Creates comprehensive charts and graphs
- Generates interactive HTML dashboard
- Produces presentation-ready visualizations

### 4. Alert System
- Monitors for negative sentiment spikes
- Flags high-priority negative comments
- Generates automated alert reports

## 📈 Results Interpretation

### Sentiment Scores

- **Compound Score**: Overall sentiment (-1 to 1)
  - `> 0.05`: Positive
  - `-0.05 to 0.05`: Neutral
  - `< -0.05`: Negative

- **Component Scores** (0 to 1):
  - `pos`: Proportion of positive sentiment
  - `neu`: Proportion of neutral sentiment
  - `neg`: Proportion of negative sentiment

### Example Output

```
Sentiment Summary:
------------------
Total Analyzed: 100
Positive: 42 (42.0%)
Negative: 28 (28.0%)
Neutral: 30 (30.0%)
Average Compound Score: 0.156
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v
```

## 📖 Documentation

- **[Product Specification](product_specification.md)**: Detailed system architecture and requirements
- **[Presentation Guide](docs/presentation_guide.md)**: 5-minute presentation structure
- **[Q&A Preparation](docs/qa_preparation.md)**: Expected questions and answers
- **[Data Documentation](data/README.md)**: Dataset details and format

## 🎯 Use Cases

1. **Brand Monitoring**: Track public sentiment about your brand
2. **Product Launch**: Assess reception of new products
3. **Campaign Analysis**: Measure effectiveness of marketing campaigns
4. **Crisis Detection**: Early warning for negative sentiment spikes
5. **Competitor Analysis**: Compare sentiment across brands
6. **Customer Feedback**: Analyze customer opinions at scale

## 🔮 Future Enhancements

- [ ] Real-time streaming data support
- [ ] Advanced ML models (BERT, RoBERTa)
- [ ] Multi-language support
- [ ] Aspect-based sentiment analysis
- [ ] API integration for social platforms
- [ ] Mobile dashboard application
- [ ] Historical trend comparison
- [ ] Sentiment prediction modeling

## 📊 Sample Visualizations

The system generates various visualizations:

- **Sentiment Distribution**: Pie chart showing proportion of each sentiment
- **Score Histogram**: Distribution of compound scores
- **Time Series**: Sentiment trends over time
- **Word Clouds**: Visual representation of frequently used words
- **Platform Comparison**: Sentiment breakdown by social media platform
- **HTML Dashboard**: Interactive web-based report

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Christopher Hanna Nehme**

## 🙏 Acknowledgments

- VADER Sentiment Analysis by C.J. Hutto
- NLTK team for natural language processing tools
- The open-source community for various libraries used

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Ready for immediate demonstration and production deployment!** 🚀
