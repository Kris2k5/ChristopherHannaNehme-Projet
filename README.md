# 🎯 Email Urgency Detection System v1.0

A production-ready email urgency detection system with advanced visualization features. Automatically analyzes email urgency, generates interactive dashboards, and creates high-quality charts for data-driven decision making.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-minimal-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Overview

This system uses rule-based keyword detection to automatically analyze email urgency and prioritize follow-up actions. It processes emails to identify time-sensitive requests, urgent business needs, and high-priority leads that require immediate attention.

**New in v1.0:**
- 📊 Interactive HTML Dashboard
- 📈 High-quality PNG Charts (300 DPI)
- 🎯 Unique Priority Ranking (1-55)
- 📉 Realistic Score Distribution
- 🔍 Enhanced Error Handling

## ✨ Key Features

✅ **Intelligent Scoring System**
- Urgency score: 0-100 scale with realistic distribution
- Each keyword counted only once (no duplicate scoring)
- Body content analysis (max 70 points)
- Subject line bonus scoring (max 30 points)

✅ **Interactive Visualizations**
- HTML dashboard with Chart.js
- Distribution pie chart
- Urgency scores bar chart
- Timeline trends chart
- Color-coded email table (top 20 most urgent)

✅ **High-Quality PNG Charts**
- 300 DPI resolution for presentations
- Professional styling with matplotlib
- Three comprehensive charts

✅ **Production-Ready**
- Comprehensive error handling
- Auto-creates output directories
- Clear error messages with solutions
- Works on Windows, Mac, and Linux

## 🚀 Quick Start

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Kris2k5/ChristopherHannaNehme-Projet.git
cd ChristopherHannaNehme-Projet

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the system
python main.py
```

## 📊 Output Files

The system generates 5 output files:

1. **CSV Results** (`data/output_results.csv`) - Complete analysis with rankings
2. **HTML Dashboard** (`results/urgency_dashboard.html`) - Interactive visualization
3. **Distribution Chart** (`results/charts/urgency_distribution.png`) - Pie chart
4. **Scores Chart** (`results/charts/urgency_scores.png`) - Bar chart with thresholds
5. **Timeline Chart** (`results/charts/urgency_timeline.png`) - Trends over time

## 📸 Screenshots

### Interactive Dashboard
![Dashboard](https://github.com/user-attachments/assets/0f6bb213-90ec-4650-b57f-bb6f349e820f)

### Distribution Chart
![Distribution](https://github.com/user-attachments/assets/7f41d993-920c-496d-8408-98c305cdaf5f)

## 🔍 How It Works

### Scoring Algorithm

1. **Analyze email body** → max 70 points
   - Critical keywords (weight: 15): urgent, ASAP, immediately
   - High keywords (weight: 12): soon, deadline, time-sensitive
   - Medium keywords (weight: 8): please, need, important

2. **Analyze subject line** → max 30 points bonus
   - Separate scoring to prevent double-counting

3. **Final classification**:
   - Critical: 76-100
   - High: 51-75
   - Medium: 26-50
   - Low: 0-25

## 💡 Use Cases

- **Sales Teams**: Prioritize follow-up with hot leads
- **Customer Support**: Identify urgent issues
- **Business Development**: Flag time-sensitive opportunities
- **Account Management**: Respond to critical client requests

## 🛠 Technologies

- Python 3.8+
- Pandas (data manipulation)
- Matplotlib (chart generation)
- Chart.js (interactive charts)

## 📝 License

MIT License

## 👤 Author

**Christopher Hanna Nehme**

---

**Ready for production use!** 🚀
