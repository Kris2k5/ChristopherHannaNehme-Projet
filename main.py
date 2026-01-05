#!/usr/bin/env python3
"""
Email Urgency Detection System - Main Script
"""

import os
import pandas as pd
from src.urgency_detector import UrgencyDetector
from src.dashboard_generator import DashboardGenerator
from src.config import DATA_DIR, INPUT_FILE, OUTPUT_FILE, RESULTS_DIR, DASHBOARD_FILE


def load_emails(filepath: str) -> pd.DataFrame:
    """
    Load emails from CSV file
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        DataFrame with email data
    """
    return pd.read_csv(filepath)


def analyze_emails(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze urgency for all emails
    
    Args:
        df: DataFrame with email data
        
    Returns:
        DataFrame with urgency analysis results
    """
    detector = UrgencyDetector()
    results = []
    
    for idx, row in df.iterrows():
        email_data = row.to_dict()
        result = detector.detect_urgency(email_data)
        result['timestamp'] = row['timestamp']
        results.append(result)
    
    return pd.DataFrame(results)


def save_results(results_df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    Save results to CSV file
    
    Args:
        results_df: DataFrame with analysis results
        output_path: Path to save CSV file
        
    Returns:
        Sorted DataFrame with priority_rank added
    """
    # Sort by urgency_score (descending) and timestamp (ascending for ties)
    results_df = results_df.sort_values(
        by=['urgency_score', 'timestamp'], 
        ascending=[False, True]
    ).reset_index(drop=True)
    
    # Add unique priority rank (1 to N)
    results_df['priority_rank'] = range(1, len(results_df) + 1)
    
    # Reorder columns
    columns = ['email_id', 'sender', 'subject', 'urgency_score', 'urgency_level', 
               'flagged_keywords', 'priority_rank', 'timestamp']
    results_df = results_df[columns]
    
    # Save to CSV
    results_df.to_csv(output_path, index=False)
    return results_df


def main():
    """Main function to run the email urgency detection system"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     EMAIL URGENCY DETECTION SYSTEM                       ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    # Construct file paths
    input_path = os.path.join(DATA_DIR, INPUT_FILE)
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    
    # Step 1: Load emails
    print("[1/3] Loading emails from data/sample_emails.csv...")
    emails_df = load_emails(input_path)
    print(f"      ✓ Loaded {len(emails_df)} emails successfully\n")
    
    # Step 2: Analyze urgency
    print("[2/3] Analyzing urgency levels...")
    results_df = analyze_emails(emails_df)
    print("      ✓ Analysis complete\n")
    
    # Step 3: Save CSV and generate dashboard
    print("[3/3] Generating outputs...")
    
    # Save CSV
    results_df = save_results(results_df, output_path)
    print("      ✓ Saved CSV: data/output_results.csv")
    
    # Generate HTML dashboard
    os.makedirs(RESULTS_DIR, exist_ok=True)
    generator = DashboardGenerator()
    generator.generate_dashboard(results_df)
    print("      ✓ Saved dashboard: results/urgency_dashboard.html\n")
    
    # Display summary
    print("═══════════════════════════════════════════════════════════")
    print("ANALYSIS SUMMARY")
    print("═══════════════════════════════════════════════════════════")
    print(f"Total Emails Analyzed: {len(results_df)}\n")
    
    print("Urgency Distribution:")
    dist = results_df['urgency_level'].value_counts()
    for level in ['Critical', 'High', 'Medium', 'Low']:
        count = dist.get(level, 0)
        pct = (count / len(results_df)) * 100
        emoji = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}[level]
        print(f"  {emoji} {level:8} {count:2} emails ({pct:5.1f}%)")
    
    print("\nTop 5 Most Urgent Emails:")
    top5 = results_df.nsmallest(5, 'priority_rank')
    for idx, row in top5.iterrows():
        print(f"  #{int(row['priority_rank'])} [Score: {int(row['urgency_score']):3}] {row['subject'][:60]}")
    
    print("\n═══════════════════════════════════════════════════════════")
    print("✓ All outputs generated successfully!")
    print("\n📊 View Dashboard: Open results/urgency_dashboard.html in your browser")
    print("📄 View Data: Check data/output_results.csv")
    print("═══════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    main()
