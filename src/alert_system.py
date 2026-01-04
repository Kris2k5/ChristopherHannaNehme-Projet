"""
Alert system for detecting sentiment spikes and anomalies.
Monitors negative sentiment trends and generates alerts for brand reputation management.
"""
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from config import ALERT_SETTINGS


class SentimentAlertSystem:
    """
    Alert system for monitoring sentiment trends and detecting negative spikes.
    """
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the alert system.
        
        Args:
            config: Optional dictionary with alert settings.
                   If None, uses default settings from config.py
        """
        self.config = config or ALERT_SETTINGS
        self.alerts = []
        
    def detect_negative_spike(
        self, 
        df: pd.DataFrame,
        window_size: Optional[int] = None
    ) -> List[Dict]:
        """
        Detect consecutive negative sentiment spikes.
        
        Args:
            df: DataFrame with sentiment analysis results
            window_size: Number of consecutive items to check (default from config)
            
        Returns:
            List of alert dictionaries
        """
        if 'compound_score' not in df.columns:
            return []
        
        window_size = window_size or self.config['spike_window']
        negative_threshold = self.config['negative_threshold']
        min_ratio = self.config['min_negative_ratio']
        
        alerts = []
        
        # Check rolling window for negative spikes
        for i in range(len(df) - window_size + 1):
            window = df.iloc[i:i+window_size]
            negative_count = (window['compound_score'] < negative_threshold).sum()
            negative_ratio = negative_count / window_size
            
            if negative_ratio >= min_ratio:
                alert = {
                    'alert_type': 'Negative Spike Detected',
                    'severity': 'High',
                    'start_index': i,
                    'end_index': i + window_size - 1,
                    'negative_count': negative_count,
                    'negative_ratio': negative_ratio,
                    'avg_compound_score': window['compound_score'].mean(),
                    'timestamp': datetime.now().isoformat(),
                    'message': f'Detected {negative_count}/{window_size} highly negative comments '
                              f'(ratio: {negative_ratio:.1%}) in consecutive window'
                }
                alerts.append(alert)
        
        return alerts
    
    def flag_high_priority_comments(
        self, 
        df: pd.DataFrame,
        threshold: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Flag high-priority negative comments.
        
        Args:
            df: DataFrame with sentiment analysis results
            threshold: Compound score threshold (default from config)
            
        Returns:
            DataFrame with flagged comments
        """
        if 'compound_score' not in df.columns:
            return pd.DataFrame()
        
        threshold = threshold or self.config['negative_threshold']
        
        df = df.copy()
        df['high_priority'] = df['compound_score'] < threshold
        
        # Filter and sort high priority comments
        high_priority_df = df[df['high_priority']].copy()
        high_priority_df = high_priority_df.sort_values('compound_score').reset_index(drop=True)
        
        return high_priority_df
    
    def detect_sentiment_drop(
        self, 
        df: pd.DataFrame,
        time_column: str = 'timestamp',
        drop_threshold: float = 0.3
    ) -> List[Dict]:
        """
        Detect sudden drops in average sentiment over time.
        
        Args:
            df: DataFrame with sentiment analysis and timestamp
            time_column: Name of the timestamp column
            drop_threshold: Minimum sentiment drop to trigger alert
            
        Returns:
            List of alert dictionaries
        """
        if time_column not in df.columns or 'compound_score' not in df.columns:
            return []
        
        df = df.copy()
        df[time_column] = pd.to_datetime(df[time_column])
        df = df.sort_values(time_column)
        
        # Calculate rolling average
        window = 5
        if len(df) < window * 2:
            return []
        
        df['rolling_avg'] = df['compound_score'].rolling(window=window, center=False).mean()
        
        alerts = []
        
        # Detect drops
        for i in range(window, len(df) - window):
            prev_avg = df['rolling_avg'].iloc[i-window:i].mean()
            curr_avg = df['rolling_avg'].iloc[i:i+window].mean()
            
            if prev_avg - curr_avg >= drop_threshold:
                alert = {
                    'alert_type': 'Sentiment Drop Detected',
                    'severity': 'Medium',
                    'timestamp': df[time_column].iloc[i].isoformat(),
                    'previous_avg': prev_avg,
                    'current_avg': curr_avg,
                    'drop_magnitude': prev_avg - curr_avg,
                    'message': f'Sentiment dropped by {prev_avg - curr_avg:.2f} '
                              f'(from {prev_avg:.2f} to {curr_avg:.2f})'
                }
                alerts.append(alert)
        
        return alerts
    
    def analyze_platform_alerts(
        self, 
        df: pd.DataFrame,
        negative_threshold_pct: float = 50.0
    ) -> List[Dict]:
        """
        Detect platforms with unusually high negative sentiment.
        
        Args:
            df: DataFrame with sentiment and platform data
            negative_threshold_pct: Percentage threshold for negative sentiment
            
        Returns:
            List of alert dictionaries
        """
        if 'platform' not in df.columns or 'sentiment' not in df.columns:
            return []
        
        alerts = []
        
        for platform in df['platform'].unique():
            platform_df = df[df['platform'] == platform]
            total = len(platform_df)
            
            if total < 5:  # Skip if too few samples
                continue
            
            negative_count = (platform_df['sentiment'] == 'Negative').sum()
            negative_pct = (negative_count / total) * 100
            
            if negative_pct >= negative_threshold_pct:
                alert = {
                    'alert_type': 'Platform Alert',
                    'severity': 'Medium',
                    'platform': platform,
                    'negative_percentage': negative_pct,
                    'negative_count': negative_count,
                    'total_count': total,
                    'timestamp': datetime.now().isoformat(),
                    'message': f'{platform} has {negative_pct:.1f}% negative sentiment '
                              f'({negative_count}/{total} posts)'
                }
                alerts.append(alert)
        
        return alerts
    
    def generate_alert_report(
        self, 
        df: pd.DataFrame,
        include_high_priority: bool = True
    ) -> Dict:
        """
        Generate comprehensive alert report.
        
        Args:
            df: DataFrame with sentiment analysis results
            include_high_priority: Whether to include high priority comments
            
        Returns:
            Dictionary with complete alert information
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(df),
            'alerts': []
        }
        
        # Detect negative spikes
        spike_alerts = self.detect_negative_spike(df)
        report['alerts'].extend(spike_alerts)
        
        # Detect sentiment drops (if timestamp available)
        if 'timestamp' in df.columns:
            drop_alerts = self.detect_sentiment_drop(df)
            report['alerts'].extend(drop_alerts)
        
        # Platform alerts (if platform available)
        if 'platform' in df.columns:
            platform_alerts = self.analyze_platform_alerts(df)
            report['alerts'].extend(platform_alerts)
        
        # High priority comments
        if include_high_priority:
            high_priority = self.flag_high_priority_comments(df)
            if len(high_priority) > 0:
                report['high_priority_count'] = len(high_priority)
                report['high_priority_comments'] = high_priority.head(10).to_dict('records')
        
        # Summary
        report['alert_count'] = len(report['alerts'])
        report['has_critical_alerts'] = any(
            alert.get('severity') == 'High' for alert in report['alerts']
        )
        
        return report
    
    def create_alert_summary(self, report: Dict) -> str:
        """
        Create human-readable alert summary.
        
        Args:
            report: Alert report dictionary
            
        Returns:
            Formatted alert summary string
        """
        lines = [
            "=" * 70,
            "SENTIMENT ALERT SUMMARY",
            "=" * 70,
            f"Generated: {report['timestamp']}",
            f"Total Posts Analyzed: {report['total_analyzed']}",
            f"Total Alerts: {report['alert_count']}",
            ""
        ]
        
        if report['has_critical_alerts']:
            lines.append("⚠️  CRITICAL ALERTS DETECTED ⚠️")
            lines.append("")
        
        # List all alerts
        if report['alerts']:
            lines.append("ALERTS:")
            lines.append("-" * 70)
            for i, alert in enumerate(report['alerts'], 1):
                lines.append(f"{i}. [{alert['severity']}] {alert['alert_type']}")
                lines.append(f"   {alert['message']}")
                lines.append("")
        else:
            lines.append("✓ No alerts detected - sentiment appears normal")
            lines.append("")
        
        # High priority comments
        if 'high_priority_count' in report and report['high_priority_count'] > 0:
            lines.append(f"HIGH PRIORITY COMMENTS: {report['high_priority_count']}")
            lines.append("-" * 70)
            for i, comment in enumerate(report.get('high_priority_comments', [])[:5], 1):
                lines.append(f"{i}. Score: {comment.get('compound_score', 0):.3f}")
                text = comment.get('text', '')[:100]
                lines.append(f"   {text}...")
                lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def save_alert_report(
        self, 
        report: Dict, 
        output_path: str,
        format: str = 'txt'
    ) -> str:
        """
        Save alert report to file.
        
        Args:
            report: Alert report dictionary
            output_path: Path to save the report
            format: Format ('txt' or 'json')
            
        Returns:
            Path where report was saved
        """
        if format == 'txt':
            summary = self.create_alert_summary(report)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
        elif format == 'json':
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return output_path


def quick_alert_check(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Quick convenience function to check for alerts.
    
    Args:
        df: DataFrame with sentiment analysis results
        
    Returns:
        Tuple of (has_alerts, summary_message)
    """
    alert_system = SentimentAlertSystem()
    report = alert_system.generate_alert_report(df)
    
    has_alerts = report['alert_count'] > 0 or report.get('high_priority_count', 0) > 0
    
    if has_alerts:
        message = f"⚠️  {report['alert_count']} alerts detected"
        if report.get('high_priority_count', 0) > 0:
            message += f", {report['high_priority_count']} high priority comments"
    else:
        message = "✓ No alerts - sentiment appears normal"
    
    return has_alerts, message
