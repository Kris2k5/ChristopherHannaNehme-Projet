"""
Configuration for Email Urgency Detection System
Defines urgency keywords, weights, thresholds, and scoring rules
"""

# Urgency Keywords with Weights
URGENCY_KEYWORDS = {
    # Critical keywords (weight: 20)
    'critical': {
        'urgent': 20,
        'asap': 20,
        'immediately': 20,
        'emergency': 20,
        'critical': 20,
        'now': 20,
    },
    # High keywords (weight: 15)
    'high': {
        'soon': 15,
        'quickly': 15,
        'time-sensitive': 15,
        'deadline': 15,
        'urgent need': 15,
        'expire': 15,
        'expires': 15,
        'expiring': 15,
        'time constraint': 15,
    },
    # Medium keywords (weight: 10)
    'medium': {
        'please': 10,
        'need': 10,
        'important': 10,
        'waiting': 10,
        'required': 10,
        'necessary': 10,
        'response': 10,
        'follow up': 10,
        'follow-up': 10,
    }
}

# Time-based urgency indicators (weight: 15)
TIME_KEYWORDS = {
    'today': 15,
    'by eod': 15,
    'end of day': 15,
    'within 24 hours': 15,
    'by 5pm': 15,
    'by 5 pm': 15,
    'this afternoon': 15,
    'this morning': 15,
    'by noon': 15,
    'within hours': 15,
    'within hour': 15,
}

# Action request keywords (weight: 10)
ACTION_KEYWORDS = {
    'call me': 10,
    'need response': 10,
    'please respond': 10,
    'get back': 10,
    'respond asap': 10,
    'waiting for': 10,
    'need to know': 10,
    'let me know': 10,
    'confirm': 10,
    'approval needed': 10,
}

# Urgency level thresholds
URGENCY_THRESHOLDS = {
    'critical': 76,  # 76-100
    'high': 51,      # 51-75
    'medium': 26,    # 26-50
    'low': 0,        # 0-25
}

# Subject line weight multiplier
SUBJECT_WEIGHT_MULTIPLIER = 1.5

# Paths
DATA_DIR = "data"
INPUT_FILE = "sample_emails.csv"
OUTPUT_FILE = "output_results.csv"
