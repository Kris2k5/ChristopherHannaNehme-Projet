"""
Urgency Detector Module
Main urgency detection engine with rule-based keyword matching
"""

from typing import Dict, List, Tuple
from src.config import (
    URGENCY_KEYWORDS, TIME_KEYWORDS, ACTION_KEYWORDS,
    URGENCY_THRESHOLDS, SUBJECT_WEIGHT_MULTIPLIER, MAX_URGENCY_SCORE
)
from src.email_analyzer import EmailAnalyzer


class UrgencyDetector:
    """Rule-based urgency detection system for email analysis"""
    
    def __init__(self):
        self.analyzer = EmailAnalyzer()
        self.urgency_keywords = URGENCY_KEYWORDS
        self.time_keywords = TIME_KEYWORDS
        self.action_keywords = ACTION_KEYWORDS
        self.thresholds = URGENCY_THRESHOLDS
        self.subject_multiplier = SUBJECT_WEIGHT_MULTIPLIER
    
    def calculate_keyword_score(self, text: str, keywords_dict: Dict) -> Tuple[int, List[str]]:
        """
        Calculate urgency score from keywords in text
        Each unique keyword is counted only ONCE to prevent over-counting
        
        Args:
            text: Text to analyze
            keywords_dict: Dictionary of keywords with their weights
            
        Returns:
            Tuple of (score, list of found keywords)
        """
        score = 0
        found_keywords = []
        text_lower = text.lower()
        
        for keyword, weight in keywords_dict.items():
            if keyword in text_lower:
                score += weight
                found_keywords.append(keyword)
        
        return score, found_keywords
    
    def contains_time_constraint(self, text: str) -> Tuple[bool, int, List[str]]:
        """
        Check if text contains time-based urgency indicators
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (has_time_constraint, score, list of found keywords)
        """
        text_clean = self.analyzer.preprocess_text(text)
        score, keywords = self.calculate_keyword_score(text_clean, self.time_keywords)
        return score > 0, score, keywords
    
    def contains_action_words(self, text: str) -> Tuple[bool, int, List[str]]:
        """
        Check if text contains action request keywords
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (has_action_words, score, list of found keywords)
        """
        text_clean = self.analyzer.preprocess_text(text)
        score, keywords = self.calculate_keyword_score(text_clean, self.action_keywords)
        return score > 0, score, keywords
    
    def calculate_urgency_score(self, subject: str, body: str) -> Tuple[int, List[str]]:
        """
        Calculate overall urgency score for an email with proper score distribution
        
        Implementation prevents duplicate keyword counting:
        - Body keywords counted once (max 70 points from body)
        - Subject gets separate analysis with bonus points (max 30 points)
        - Final score capped at 100
        
        Args:
            subject: Email subject line
            body: Email body text
            
        Returns:
            Tuple of (final score, list of all flagged keywords)
        """
        body_score = 0
        body_keywords = set()  # Use set to track unique keywords
        
        # Analyze body for critical keywords
        body_clean = self.analyzer.preprocess_text(body)
        for category, keywords_dict in self.urgency_keywords.items():
            score, keywords = self.calculate_keyword_score(body_clean, keywords_dict)
            body_score += score
            body_keywords.update(keywords)
        
        # Check for time-based urgency in body
        has_time, time_score, time_keywords = self.contains_time_constraint(body)
        body_score += time_score
        body_keywords.update(time_keywords)
        
        # Check for action requests in body
        has_action, action_score, action_keywords = self.contains_action_words(body)
        body_score += action_score
        body_keywords.update(action_keywords)
        
        # Cap body score at 70 points maximum
        body_score = min(body_score, 70)
        
        # Analyze subject line separately for bonus points (max 30)
        subject_clean = self.analyzer.preprocess_text(subject)
        subject_score = 0
        subject_keywords = set()
        
        # Check all keyword categories in subject
        for category, keywords_dict in self.urgency_keywords.items():
            score, keywords = self.calculate_keyword_score(subject_clean, keywords_dict)
            subject_score += score
            subject_keywords.update(keywords)
        
        # Check time keywords in subject
        score, keywords = self.calculate_keyword_score(subject_clean, self.time_keywords)
        subject_score += score
        subject_keywords.update(keywords)
        
        # Check action keywords in subject
        score, keywords = self.calculate_keyword_score(subject_clean, self.action_keywords)
        subject_score += score
        subject_keywords.update(keywords)
        
        # Cap subject bonus at 30 points
        subject_bonus = min(subject_score, 30)
        
        # Calculate final score (max 100)
        final_score = min(body_score + subject_bonus, MAX_URGENCY_SCORE)
        
        # Combine keywords for display
        all_keywords = list(body_keywords) + [f"{kw} (subject)" for kw in subject_keywords]
        
        return final_score, all_keywords
    
    def classify_urgency_level(self, score: int) -> str:
        """
        Classify urgency level based on score
        
        Args:
            score: Urgency score (0-100)
            
        Returns:
            Urgency level string: Critical, High, Medium, or Low
        """
        if score >= self.thresholds['critical']:
            return "Critical"
        elif score >= self.thresholds['high']:
            return "High"
        elif score >= self.thresholds['medium']:
            return "Medium"
        else:
            return "Low"
    
    def detect_urgency(self, email_data: Dict) -> Dict:
        """
        Detect urgency level for a single email
        
        Args:
            email_data: Dictionary with email fields (subject, body, etc.)
            
        Returns:
            Dictionary with urgency analysis results
        """
        subject = email_data.get('subject', '')
        body = email_data.get('body', '')
        
        # Calculate urgency score and get flagged keywords
        urgency_score, flagged_keywords = self.calculate_urgency_score(subject, body)
        
        # Classify urgency level
        urgency_level = self.classify_urgency_level(urgency_score)
        
        # Generate report
        result = self.analyzer.generate_urgency_report(
            email_data, urgency_score, urgency_level, flagged_keywords
        )
        
        return result
    
    def flag_high_priority(self, urgency_level: str) -> bool:
        """
        Flag email as high priority if it needs immediate attention
        
        Args:
            urgency_level: Urgency level classification
            
        Returns:
            Boolean indicating if email should be flagged
        """
        return urgency_level in ["Critical", "High"]
