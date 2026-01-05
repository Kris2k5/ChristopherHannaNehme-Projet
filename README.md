# 🎯 Email Urgency Detection System

A lightweight email urgency detection system with clean HTML visualization. Automatically analyzes email urgency and generates an interactive dashboard for data-driven decision making.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-minimal-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Overview

This system uses rule-based keyword detection to automatically analyze email urgency and prioritize follow-up actions. It processes emails to identify time-sensitive requests, urgent business needs, and high-priority leads that require immediate attention.

**Key Features:**
- 📊 Clean HTML Dashboard with CSS visualizations
- 🎯 Unique Priority Ranking
- 📉 Realistic Score Distribution
- ⚡ Fast execution (< 5 seconds)

## ✨ Key Features

✅ **Intelligent Scoring System**
- Urgency score: 0-100 scale with realistic distribution
- Each keyword counted only once (no duplicate scoring)
- Body content analysis (max 70 points)
- Subject line bonus scoring (max 30 points)

✅ **Clean HTML Dashboard**
- Pure HTML/CSS visualization (no external JavaScript libraries)
- Simple colored progress bars for distribution
- Color-coded email table (top 30 most urgent)
- Responsive design
- Lightweight and fast to generate

✅ **Production-Ready**
- Minimal dependencies (pandas, openpyxl only)
- Auto-creates output directories
- Works on Windows, Mac, and Linux
- Fast execution (< 5 seconds)

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

The system generates 2 output files:

1. **CSV Results** (`data/output_results.csv`) - Complete analysis with rankings
2. **HTML Dashboard** (`results/urgency_dashboard.html`) - Clean, simple visualization

## 📸 Dashboard Preview

### Clean HTML Dashboard
The dashboard provides a simple, fast visualization of email urgency distribution with color-coded priority emails.

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
