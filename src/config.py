"""
Configuration for Email Urgency Detection System
Defines urgency keywords, weights, thresholds, and scoring rules
"""

# Urgency Keywords with Weights
URGENCY_KEYWORDS = {
    # Critical keywords (weight: 15)
    'critical': {
        'urgent': 15,
        'asap': 15,
        'immediately': 15,
        'emergency': 15,
        'critical': 15,
        'now': 15,
    },
    # High keywords (weight: 12)
    'high': {
        'soon': 12,
        'quickly': 12,
        'time-sensitive': 12,
        'deadline': 12,
        'urgent need': 12,
        'expire': 12,
        'expires': 12,
        'expiring': 12,
        'time constraint': 12,
    },
    # Medium keywords (weight: 8)
    'medium': {
        'please': 8,
        'need': 8,
        'important': 8,
        'waiting': 8,
        'required': 8,
        'necessary': 8,
        'response': 8,
        'follow up': 8,
        'follow-up': 8,
    }
}

# Time-based urgency indicators (weight: 12)
TIME_KEYWORDS = {
    'today': 12,
    'by eod': 12,
    'end of day': 12,
    'within 24 hours': 12,
    'by 5pm': 12,
    'by 5 pm': 12,
    'this afternoon': 12,
    'this morning': 12,
    'by noon': 12,
    'within hours': 12,
    'within hour': 12,
}

# Action request keywords (weight: 8)
ACTION_KEYWORDS = {
    'call me': 8,
    'need response': 8,
    'please respond': 8,
    'get back': 8,
    'respond asap': 8,
    'waiting for': 8,
    'need to know': 8,
    'let me know': 8,
    'confirm': 8,
    'approval needed': 8,
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

# Score constraints
MAX_URGENCY_SCORE = 100

# Display settings
KEYWORD_DISPLAY_LENGTH = 80

# Paths
DATA_DIR = "data"
INPUT_FILE = "sample_emails.csv"
OUTPUT_FILE = "output_results.csv"
RESULTS_DIR = "results"
CHARTS_DIR = "results/charts"
DASHBOARD_FILE = "results/urgency_dashboard.html"

# Chart colors
CHART_COLORS = {
    'critical': '#ff4444',  # Red
    'high': '#ff9944',      # Orange
    'medium': '#ffdd44',    # Yellow
    'low': '#44ff44',       # Green
}

# Chart settings
CHART_DPI = 300
CHART_WIDTH = 12
CHART_HEIGHT = 8
