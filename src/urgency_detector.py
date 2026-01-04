"""
Urgency Detector Module
Main urgency detection engine with rule-based keyword matching
"""

from typing import Dict, List, Tuple
from src.config import (
    URGENCY_KEYWORDS, TIME_KEYWORDS, ACTION_KEYWORDS,
    URGENCY_THRESHOLDS, SUBJECT_WEIGHT_MULTIPLIER
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
    
    def analyze_subject(self, subject: str) -> Tuple[int, List[str]]:
        """
        Analyze subject line for urgency with higher weight
        
        Args:
            subject: Email subject line
            
        Returns:
            Tuple of (weighted score, list of found keywords)
        """
        subject_clean = self.analyzer.preprocess_text(subject)
        total_score = 0
        all_keywords = []
        
        # Check critical keywords
        for keywords_dict in self.urgency_keywords.values():
            score, keywords = self.calculate_keyword_score(subject_clean, keywords_dict)
            total_score += score
            all_keywords.extend(keywords)
        
        # Check time keywords
        score, keywords = self.calculate_keyword_score(subject_clean, self.time_keywords)
        total_score += score
        all_keywords.extend(keywords)
        
        # Check action keywords
        score, keywords = self.calculate_keyword_score(subject_clean, self.action_keywords)
        total_score += score
        all_keywords.extend(keywords)
        
        return total_score, all_keywords
    
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
        Calculate overall urgency score for an email
        
        Args:
            subject: Email subject line
            body: Email body text
            
        Returns:
            Tuple of (final score, list of all flagged keywords)
        """
        urgency_score = 0
        all_keywords = []
        
        # Analyze body for critical keywords
        body_clean = self.analyzer.preprocess_text(body)
        for category, keywords_dict in self.urgency_keywords.items():
            score, keywords = self.calculate_keyword_score(body_clean, keywords_dict)
            urgency_score += score
            all_keywords.extend(keywords)
        
        # Check for time-based urgency in body
        has_time, time_score, time_keywords = self.contains_time_constraint(body)
        urgency_score += time_score
        all_keywords.extend(time_keywords)
        
        # Check for action requests in body
        has_action, action_score, action_keywords = self.contains_action_words(body)
        urgency_score += action_score
        all_keywords.extend(action_keywords)
        
        # Analyze subject line with higher weight
        subject_score, subject_keywords = self.analyze_subject(subject)
        weighted_subject_score = int(subject_score * self.subject_multiplier)
        urgency_score += weighted_subject_score
        all_keywords.extend([f"{kw} (subject)" for kw in subject_keywords])
        
        # Cap the final score at 100
        final_score = min(urgency_score, 100)
        
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
