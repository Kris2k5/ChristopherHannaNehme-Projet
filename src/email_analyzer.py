"""
Email Analyzer Module
Handles text preprocessing and email content analysis
"""

import re
from typing import Dict, List, Tuple


class EmailAnalyzer:
    """Analyzes email content and extracts urgency indicators"""
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text by converting to lowercase and removing extra spaces
        
        Args:
            text: Raw text string
            
        Returns:
            Preprocessed text string
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_email_info(self, email_data: Dict) -> Dict:
        """
        Extract key information from email data
        
        Args:
            email_data: Dictionary containing email fields
            
        Returns:
            Dictionary with extracted information
        """
        return {
            'email_id': email_data.get('email_id', ''),
            'sender': email_data.get('sender', ''),
            'subject': email_data.get('subject', ''),
            'body': email_data.get('body', ''),
            'timestamp': email_data.get('timestamp', ''),
        }
    
    def detect_urgency_indicators(self, text: str, keywords_dict: Dict) -> List[str]:
        """
        Detect urgency keywords in text
        
        Args:
            text: Preprocessed text
            keywords_dict: Dictionary of keywords to search for
            
        Returns:
            List of detected keywords
        """
        detected = []
        text_lower = text.lower()
        
        for keyword in keywords_dict.keys():
            if keyword in text_lower:
                detected.append(keyword)
        
        return detected
    
    def count_urgency_keywords(self, text: str, keywords_dict: Dict) -> int:
        """
        Count total urgency keywords in text
        
        Args:
            text: Preprocessed text
            keywords_dict: Dictionary of keywords with weights
            
        Returns:
            Count of urgency keywords found
        """
        count = 0
        text_lower = text.lower()
        
        for keyword in keywords_dict.keys():
            if keyword in text_lower:
                count += 1
        
        return count
    
    def analyze_email_structure(self, subject: str, body: str) -> Dict:
        """
        Analyze email structure for urgency indicators
        
        Args:
            subject: Email subject line
            body: Email body text
            
        Returns:
            Dictionary with structural analysis
        """
        # Preprocess both
        subject_clean = self.preprocess_text(subject)
        body_clean = self.preprocess_text(body)
        
        # Check for all caps in subject (indicates urgency)
        has_caps_subject = subject.isupper() if subject else False
        
        # Check for exclamation marks
        exclamation_count = subject.count('!') + body.count('!')
        
        # Calculate lengths
        subject_length = len(subject_clean.split())
        body_length = len(body_clean.split())
        
        return {
            'subject_clean': subject_clean,
            'body_clean': body_clean,
            'has_caps_subject': has_caps_subject,
            'exclamation_count': exclamation_count,
            'subject_word_count': subject_length,
            'body_word_count': body_length,
        }
    
    def generate_urgency_report(self, email_data: Dict, urgency_score: int, 
                               urgency_level: str, flagged_keywords: List[str]) -> Dict:
        """
        Generate comprehensive urgency report for an email
        
        Args:
            email_data: Original email data
            urgency_score: Calculated urgency score
            urgency_level: Urgency level classification
            flagged_keywords: List of detected urgency keywords
            
        Returns:
            Dictionary containing full urgency report
        """
        return {
            'email_id': email_data.get('email_id', ''),
            'sender': email_data.get('sender', ''),
            'subject': email_data.get('subject', ''),
            'urgency_score': urgency_score,
            'urgency_level': urgency_level,
            'flagged_keywords': ', '.join(flagged_keywords) if flagged_keywords else 'None',
            'keyword_count': len(flagged_keywords),
        }
