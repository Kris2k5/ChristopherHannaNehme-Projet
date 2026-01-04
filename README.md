# 🎯 Email Urgency Detection for High-Priority Leads

A lightweight, production-ready machine learning project that detects urgency in prospect emails and flags high-priority leads for follow-up.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-minimal-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Overview

This system uses rule-based keyword detection to automatically analyze email urgency and prioritize follow-up actions. It processes emails to identify time-sensitive requests, urgent business needs, and high-priority leads that require immediate attention.

### What Problem Does It Solve?

**Sales and business development teams face challenges:**
- Hundreds of emails daily from prospects and leads
- Difficulty prioritizing which emails need immediate response
- Missing time-sensitive opportunities due to delayed responses
- Inconsistent urgency assessment across team members

**This system provides:**
- Automated urgency detection based on keywords and patterns
- Consistent urgency scoring (0-100) across all emails
- Clear prioritization (Critical, High, Medium, Low)
- Instant identification of emails requiring immediate action

## ✨ Features

✅ **Rule-Based Urgency Detection**
- Keyword matching with weighted scoring
- Subject line analysis (weighted 1.5x higher)
- Time-based urgency indicators ("today", "by EOD", "within 24 hours")
- Action request detection ("call me", "need response", "waiting for")

✅ **Intelligent Scoring System**
- Urgency score: 0-100 scale
- Critical keywords: "urgent", "ASAP", "immediately" (weight: 20)
- High keywords: "soon", "deadline", "time-sensitive" (weight: 15)
- Medium keywords: "please", "need", "important" (weight: 10)

✅ **Clear Classification**
- **Critical** (76-100): Requires immediate attention
- **High** (51-75): Should respond today
- **Medium** (26-50): Respond within 1-2 days
- **Low** (0-25): Standard follow-up

✅ **Fast & Simple**
- Single command to run: `python main.py`
- Processes 50+ emails in seconds
- Generates CSV output with results
- Console summary with top urgent emails

## 🚀 Quick Start

### Installation (2 Simple Steps)

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the system**
```bash
python main.py
```

That's it! The system will analyze all emails and generate results.

## 📊 Usage Examples

### Basic Usage

```bash
python main.py
```

### Expected Output

```
=== Email Urgency Detection System ===

Loading emails from data/sample_emails.csv...
Loaded 55 emails.

Analyzing urgency levels...
[====================] 55/55

Results:
--------
Total emails analyzed: 55
  🔴 Critical (76-100): 23 emails
  🟠 High (51-75): 3 emails
  🟡 Medium (26-50): 5 emails
  🟢 Low (0-25): 24 emails

Top 5 Most Urgent Emails:
1. [Score: 100] "URGENT: Contract expires today - need signature ASAP"
2. [Score: 100] "Emergency: System down call immediately"
3. [Score: 100] "Need proposal by 5pm deadline - please respond"
4. [Score: 97] "Critical: Meeting moved to this afternoon"
5. [Score: 85] "Immediately need contract revisions"

Results saved to: data/output_results.csv
```

## 🔍 How Urgency Scoring Works

The system uses a **weighted keyword matching approach**:

### 1. Critical Keywords (Weight: 20 each)
- urgent, ASAP, immediately, emergency, critical, now

### 2. Time-Based Keywords (Weight: 15 each)
- today, by EOD, end of day, within 24 hours, by 5pm, this afternoon

### 3. High Priority Keywords (Weight: 15 each)
- soon, quickly, deadline, time-sensitive, expires

### 4. Action Request Keywords (Weight: 10 each)
- call me, need response, please respond, waiting for, approval needed

### 5. Medium Priority Keywords (Weight: 10 each)
- please, need, important, waiting, required, necessary

### Scoring Logic

```python
1. Scan email body for keywords → sum weights
2. Scan subject line for keywords → sum weights × 1.5 (higher priority)
3. Add bonus points for:
   - Multiple urgency indicators
   - Time constraints
   - Action requests
4. Cap final score at 100
5. Classify based on thresholds:
   - Critical: 76-100
   - High: 51-75
   - Medium: 26-50
   - Low: 0-25
```

## 📁 Project Structure

```
ChristopherHannaNehme-Projet/
├── README.md                          # This file
├── product_specification.md           # Detailed specification
├── requirements.txt                   # Python dependencies (minimal!)
├── .gitignore                         # Python gitignore
├── data/
│   ├── sample_emails.csv              # Sample email data (55 emails)
│   └── output_results.csv             # Results (auto-generated)
├── src/
│   ├── __init__.py
│   ├── urgency_detector.py            # Main urgency detection engine
│   ├── email_analyzer.py              # Email text analysis
│   └── config.py                      # Configuration (keywords, thresholds)
└── main.py                            # Main script to run the project
```

## 📥 Input Format

CSV file with the following columns:
- `email_id`: Unique identifier
- `sender`: Email address of sender
- `subject`: Email subject line
- `body`: Email body text
- `timestamp`: When email was received

**Example:**
```csv
email_id,sender,subject,body,timestamp
1,john@company.com,URGENT: Need response,Please respond ASAP...,2024-01-15 09:30:00
```

## 📤 Output Format

CSV file with analysis results:
- `email_id`: Original email ID
- `sender`: Sender email
- `subject`: Email subject
- `urgency_score`: Calculated score (0-100)
- `urgency_level`: Classification (Critical/High/Medium/Low)
- `flagged_keywords`: Detected urgency keywords
- `priority_rank`: Ranking by urgency (1 = most urgent)
- `timestamp`: Original timestamp

## 🛠 Technologies Used

- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and CSV processing
- **OpenPyXL**: Excel file support
- **Rule-Based NLP**: Keyword detection and pattern matching

## 💡 Use Cases

1. **Sales Teams**: Prioritize follow-up with hot leads
2. **Customer Support**: Identify urgent customer issues
3. **Business Development**: Flag time-sensitive opportunities
4. **Account Management**: Respond quickly to critical client requests
5. **Executive Assistants**: Route urgent communications first

## 📈 Example Results

### Critical Email (Score: 100)
```
Subject: URGENT: Contract expires today - need signature ASAP
Body: Hi team we need the contract signed immediately as it expires 
      today by 5pm. This is critical for closing the deal.
      
Detected Keywords: urgent, ASAP, immediately, critical, expires, 
                   today, by 5pm, need response
Urgency Level: Critical
Priority Rank: 1
```

### Low Priority Email (Score: 10)
```
Subject: Quick question about your services
Body: Hi I have a quick question about your consulting services. 
      When you get a chance could you please provide some information?
      
Detected Keywords: please
Urgency Level: Low
Priority Rank: 37
```

## ⚙️ Configuration

All urgency keywords and thresholds can be customized in `src/config.py`:

```python
# Adjust keyword weights
URGENCY_KEYWORDS = {
    'critical': {'urgent': 20, 'ASAP': 20, ...},
    'high': {'soon': 15, 'deadline': 15, ...},
    'medium': {'please': 10, 'need': 10, ...}
}

# Adjust thresholds
URGENCY_THRESHOLDS = {
    'critical': 76,  # 76-100
    'high': 51,      # 51-75
    'medium': 26,    # 26-50
    'low': 0         # 0-25
}
```

## 🎯 Success Criteria

✅ Runs with single command: `python main.py`  
✅ Installation takes < 1 minute  
✅ Only 2 dependencies in requirements.txt  
✅ Produces clear CSV output  
✅ Console output is readable and informative  
✅ Code is simple enough to explain in 5 minutes  
✅ Works immediately after cloning  

## 🔮 Future Enhancements

- Machine learning model for improved accuracy
- Real-time email integration (Gmail, Outlook)
- Multi-language support
- Web dashboard interface
- Email auto-response suggestions
- Integration with CRM systems

## 🤝 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues.

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Christopher Hanna Nehme**

---

**Ready for immediate demonstration and production use!** 🚀
