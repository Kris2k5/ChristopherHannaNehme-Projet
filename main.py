"""
Email Urgency Detection System - Main Entry Point
Run this script to analyze email urgency and generate results
"""

import os
import pandas as pd
from src.urgency_detector import UrgencyDetector
from src.config import DATA_DIR, INPUT_FILE, OUTPUT_FILE, KEYWORD_DISPLAY_LENGTH


def load_emails(filepath: str) -> pd.DataFrame:
    """Load emails from CSV file"""
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} emails.")
        return df
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        print(f"Please ensure the file exists at: {os.path.abspath(filepath)}")
        print(f"Expected CSV format: email_id,sender,subject,body,timestamp")
        return None
    except Exception as e:
        print(f"Error loading emails: {e}")
        return None


def analyze_emails(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze urgency for all emails"""
    detector = UrgencyDetector()
    results = []
    
    print("\nAnalyzing urgency levels...")
    total = len(df)
    
    for idx, row in df.iterrows():
        # Show progress
        if (idx + 1) % 10 == 0 or (idx + 1) == total:
            progress = int((idx + 1) / total * 20)
            bar = "=" * progress + " " * (20 - progress)
            print(f"\r[{bar}] {idx + 1}/{total}", end="")
        
        # Analyze email
        email_data = row.to_dict()
        result = detector.detect_urgency(email_data)
        result['timestamp'] = row['timestamp']
        results.append(result)
    
    print()  # New line after progress bar
    return pd.DataFrame(results)


def calculate_statistics(results_df: pd.DataFrame) -> dict:
    """Calculate summary statistics"""
    stats = {
        'total': len(results_df),
        'critical': len(results_df[results_df['urgency_level'] == 'Critical']),
        'high': len(results_df[results_df['urgency_level'] == 'High']),
        'medium': len(results_df[results_df['urgency_level'] == 'Medium']),
        'low': len(results_df[results_df['urgency_level'] == 'Low']),
    }
    return stats


def display_results(results_df: pd.DataFrame, stats: dict):
    """Display results to console"""
    print("\n" + "=" * 50)
    print("=== Email Urgency Detection System ===")
    print("=" * 50)
    
    print("\nResults:")
    print("-" * 50)
    print(f"Total emails analyzed: {stats['total']}")
    print(f"  🔴 Critical (76-100): {stats['critical']} emails")
    print(f"  🟠 High (51-75): {stats['high']} emails")
    print(f"  🟡 Medium (26-50): {stats['medium']} emails")
    print(f"  🟢 Low (0-25): {stats['low']} emails")
    
    # Get top 5 most urgent emails
    print("\nTop 5 Most Urgent Emails:")
    print("-" * 50)
    top_5 = results_df.nlargest(5, 'urgency_score')
    
    for idx, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"{idx}. [Score: {row['urgency_score']}] \"{row['subject']}\"")
        print(f"   From: {row['sender']}")
        print(f"   Level: {row['urgency_level']}")
        print(f"   Keywords: {row['flagged_keywords'][:KEYWORD_DISPLAY_LENGTH]}...")
        print()


def save_results(results_df: pd.DataFrame, output_path: str):
    """Save results to CSV file"""
    try:
        # Add priority rank
        results_df['priority_rank'] = results_df['urgency_score'].rank(ascending=False, method='min').astype(int)
        
        # Reorder columns
        columns = ['email_id', 'sender', 'subject', 'urgency_score', 'urgency_level', 
                   'flagged_keywords', 'priority_rank', 'timestamp']
        results_df = results_df[columns]
        
        # Save to CSV
        results_df.to_csv(output_path, index=False)
        print(f"\nResults saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False


def main():
    """Main function to run the email urgency detection system"""
    
    # Construct file paths
    input_path = os.path.join(DATA_DIR, INPUT_FILE)
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    
    print("=" * 50)
    print("=== Email Urgency Detection System ===")
    print("=" * 50)
    
    # Load emails
    print(f"\nLoading emails from {input_path}...")
    df = load_emails(input_path)
    
    if df is None:
        return
    
    # Analyze emails
    results_df = analyze_emails(df)
    
    # Calculate statistics
    stats = calculate_statistics(results_df)
    
    # Display results
    display_results(results_df, stats)
    
    # Save results
    save_results(results_df, output_path)
    
    print("\n" + "=" * 50)
    print("Analysis complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
