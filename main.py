"""
Email Urgency Detection System - Main Entry Point
Run this script to analyze email urgency and generate results
"""

import os
import sys
import pandas as pd
from src.urgency_detector import UrgencyDetector
from src.chart_generator import ChartGenerator
from src.dashboard_generator import DashboardGenerator
from src.config import (
    DATA_DIR, INPUT_FILE, OUTPUT_FILE, KEYWORD_DISPLAY_LENGTH,
    RESULTS_DIR, CHARTS_DIR, DASHBOARD_FILE
)


def load_emails(filepath: str) -> pd.DataFrame:
    """
    Load emails from CSV file with error handling
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        DataFrame with email data or None if error
    """
    try:
        if not os.path.exists(filepath):
            print(f"\n❌ ERROR: File '{filepath}' not found")
            print(f"💡 SOLUTION: Ensure the file exists at: {os.path.abspath(filepath)}")
            print(f"   Expected CSV format: email_id,sender,subject,body,timestamp")
            return None
        
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_cols = ['email_id', 'sender', 'subject', 'body', 'timestamp']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"\n❌ ERROR: CSV missing required columns: {', '.join(missing_cols)}")
            print(f"💡 SOLUTION: Ensure CSV has columns: {', '.join(required_cols)}")
            return None
        
        if len(df) == 0:
            print(f"\n❌ ERROR: CSV file is empty")
            print(f"💡 SOLUTION: Add email data to the CSV file")
            return None
        
        print(f"         ✓ Loaded {len(df)} emails successfully")
        return df
        
    except PermissionError:
        print(f"\n❌ ERROR: Permission denied reading '{filepath}'")
        print(f"💡 SOLUTION: Check file permissions")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: Failed to load emails: {e}")
        print(f"💡 SOLUTION: Verify CSV file format and encoding")
        return None


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
    
    print("         ✓ Analysis complete")
    
    for idx, row in df.iterrows():
        # Analyze email
        email_data = row.to_dict()
        result = detector.detect_urgency(email_data)
        result['timestamp'] = row['timestamp']
        results.append(result)
    
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


def display_summary(results_df: pd.DataFrame, stats: dict):
    """
    Display comprehensive analysis summary
    
    Args:
        results_df: DataFrame with analysis results
        stats: Dictionary with summary statistics
    """
    print("\n" + "═" * 63)
    print("ANALYSIS SUMMARY")
    print("═" * 63)
    print(f"Total Emails Analyzed: {stats['total']}")
    print()
    print("Urgency Distribution:")
    print(f"  🔴 Critical (76-100):  {stats['critical']:2d} emails ({stats['critical']/stats['total']*100:5.1f}%)")
    print(f"  🟠 High (51-75):       {stats['high']:2d} emails ({stats['high']/stats['total']*100:5.1f}%)")
    print(f"  🟡 Medium (26-50):     {stats['medium']:2d} emails ({stats['medium']/stats['total']*100:5.1f}%)")
    print(f"  🟢 Low (0-25):         {stats['low']:2d} emails ({stats['low']/stats['total']*100:5.1f}%)")
    print()
    
    # Get top 5 most urgent emails
    print("Top 5 Most Urgent Emails:")
    top_5 = results_df.nlargest(5, 'urgency_score')
    
    for idx, (_, row) in enumerate(top_5.iterrows(), 1):
        subject = str(row['subject'])[:60]
        if len(str(row['subject'])) > 60:
            subject += '...'
        print(f"  #{idx} [Score: {int(row['urgency_score'])}] {subject}")
    
    print()
    print("═" * 63)


def save_results(results_df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """
    Save results to CSV file and return sorted DataFrame with rankings
    
    Args:
        results_df: DataFrame with analysis results
        output_path: Path to save CSV file
        
    Returns:
        Sorted DataFrame with priority_rank added, or None if error
    """
    try:
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Sort by urgency_score (descending) and timestamp (ascending for ties)
        # Earlier emails get higher priority when scores are equal
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
        print(f"         ✓ Saved to: {output_path}")
        return results_df
        
    except PermissionError:
        print(f"\n❌ ERROR: Permission denied writing to '{output_path}'")
        print(f"💡 SOLUTION: Check file permissions and close file if open")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: Failed to save results: {e}")
        print(f"💡 SOLUTION: Verify output directory exists and is writable")
        return None


def generate_charts(results_df: pd.DataFrame) -> bool:
    """
    Generate PNG charts
    
    Args:
        results_df: DataFrame with analysis results
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create charts directory if needed
        os.makedirs(CHARTS_DIR, exist_ok=True)
        
        generator = ChartGenerator()
        chart_paths = generator.generate_all_charts(results_df)
        
        for chart_type, path in chart_paths.items():
            print(f"         ✓ Created: {path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to generate charts: {e}")
        print(f"💡 SOLUTION: Ensure matplotlib is installed and directory is writable")
        return False


def generate_dashboard(results_df: pd.DataFrame) -> bool:
    """
    Generate HTML dashboard
    
    Args:
        results_df: DataFrame with analysis results
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create results directory if needed
        os.makedirs(RESULTS_DIR, exist_ok=True)
        
        generator = DashboardGenerator()
        dashboard_path = generator.generate_dashboard(results_df)
        
        print(f"         ✓ Created: {dashboard_path}")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to generate dashboard: {e}")
        print(f"💡 SOLUTION: Ensure output directory is writable")
        return False


def main():
    """Main function to run the email urgency detection system"""
    
    # Print header
    print()
    print("╔" + "═" * 62 + "╗")
    print("║" + " " * 15 + "EMAIL URGENCY DETECTION SYSTEM v1.0" + " " * 11 + "║")
    print("╚" + "═" * 62 + "╝")
    print()
    
    # Construct file paths
    input_path = os.path.join(DATA_DIR, INPUT_FILE)
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    
    # Step 1: Load emails
    print("[1/5] Loading emails from data/sample_emails.csv...")
    df = load_emails(input_path)
    
    if df is None:
        print("\n❌ Failed to load emails. Exiting.")
        sys.exit(1)
    
    # Step 2: Analyze emails
    print("\n[2/5] Analyzing urgency levels...")
    results_df = analyze_emails(df)
    
    # Step 3: Generate CSV results (and get sorted df with rankings)
    print("\n[3/5] Generating CSV results...")
    results_df = save_results(results_df, output_path)
    if results_df is None:
        print("\n❌ Failed to save results. Exiting.")
        sys.exit(1)
    
    # Step 4: Generate charts
    print("\n[4/5] Generating charts...")
    if not generate_charts(results_df):
        print("\n⚠️  Warning: Charts generation failed, continuing...")
    
    # Step 5: Generate dashboard
    print("\n[5/5] Generating HTML dashboard...")
    if not generate_dashboard(results_df):
        print("\n⚠️  Warning: Dashboard generation failed, continuing...")
    
    # Display summary
    stats = calculate_statistics(results_df)
    display_summary(results_df, stats)
    
    print("✓ All outputs generated successfully!")
    print()
    print("📊 View Dashboard: Open results/urgency_dashboard.html in your browser")
    print("📈 View Charts: Check results/charts/ folder")
    print("📄 View Data: Check data/output_results.csv")
    print("═" * 63)
    print()


if __name__ == "__main__":
    main()
