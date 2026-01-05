"""
Dashboard Generator Module
Creates simple HTML dashboard for email urgency visualization
"""

import os
import pandas as pd
from datetime import datetime
from src.config import DASHBOARD_FILE


class DashboardGenerator:
    """Generates simple HTML dashboard for urgency analysis"""
    
    def __init__(self, output_path: str = DASHBOARD_FILE):
        """
        Initialize dashboard generator
        
        Args:
            output_path: Path to save HTML dashboard
        """
        self.output_path = output_path
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    
    def generate_dashboard(self, results_df: pd.DataFrame) -> str:
        """
        Generate complete HTML dashboard
        
        Args:
            results_df: DataFrame with urgency analysis results
            
        Returns:
            Path to saved dashboard file
        """
        # Calculate statistics
        total = len(results_df)
        critical = len(results_df[results_df['urgency_level'] == 'Critical'])
        high = len(results_df[results_df['urgency_level'] == 'High'])
        medium = len(results_df[results_df['urgency_level'] == 'Medium'])
        low = len(results_df[results_df['urgency_level'] == 'Low'])
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Urgency Detection Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 15px;
        }}
        
        .summary {{
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .summary h2 {{
            margin-bottom: 15px;
            color: #333;
        }}
        
        .summary p {{
            font-size: 1.1em;
            margin-bottom: 15px;
        }}
        
        .summary ul {{
            list-style: none;
            font-size: 1.1em;
        }}
        
        .summary li {{
            margin: 10px 0;
        }}
        
        .distribution {{
            padding: 30px;
            background: white;
        }}
        
        .distribution h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .bar {{
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            min-width: 150px;
            transition: all 0.3s ease;
        }}
        
        .bar:hover {{
            transform: translateX(5px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        .bar.critical {{
            background: #ff4444;
        }}
        
        .bar.high {{
            background: #ff9944;
        }}
        
        .bar.medium {{
            background: #ffdd44;
            color: #333;
        }}
        
        .bar.low {{
            background: #44ff44;
            color: #333;
        }}
        
        .emails-table {{
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .emails-table h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        thead {{
            background: #667eea;
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .level-critical {{
            background-color: #ffcccc;
        }}
        
        .level-high {{
            background-color: #ffe0cc;
        }}
        
        .level-medium {{
            background-color: #ffffcc;
        }}
        
        .level-low {{
            background-color: #ccffcc;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        
        .badge-critical {{
            background: #ff4444;
        }}
        
        .badge-high {{
            background: #ff9944;
        }}
        
        .badge-medium {{
            background: #ffdd44;
            color: #333;
        }}
        
        .badge-low {{
            background: #44ff44;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Simple Header -->
        <header>
            <h1>Email Urgency Detection Dashboard</h1>
        </header>
        
        <!-- Summary Statistics -->
        <div class="summary">
            <h2>Analysis Summary</h2>
            <p><strong>Total Emails Analyzed:</strong> {total}</p>
            <ul>
                <li>🔴 <strong>Critical:</strong> {critical} emails ({critical/total*100:.1f}%)</li>
                <li>🟠 <strong>High:</strong> {high} emails ({high/total*100:.1f}%)</li>
                <li>🟡 <strong>Medium:</strong> {medium} emails ({medium/total*100:.1f}%)</li>
                <li>🟢 <strong>Low:</strong> {low} emails ({low/total*100:.1f}%)</li>
            </ul>
        </div>
        
        <!-- Simple Distribution Visualization -->
        <div class="distribution">
            <h2>📊 Urgency Distribution</h2>
            <div class="bar critical" style="width: {critical/total*100:.1f}%">Critical: {critical} ({critical/total*100:.1f}%)</div>
            <div class="bar high" style="width: {high/total*100:.1f}%">High: {high} ({high/total*100:.1f}%)</div>
            <div class="bar medium" style="width: {medium/total*100:.1f}%">Medium: {medium} ({medium/total*100:.1f}%)</div>
            <div class="bar low" style="width: {low/total*100:.1f}%">Low: {low} ({low/total*100:.1f}%)</div>
        </div>
        
        <!-- Top Priority Emails Table -->
        <div class="emails-table">
            <h2>📋 Top 30 Priority Emails</h2>
            <div style="overflow-x: auto; max-height: 600px; overflow-y: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Score</th>
                            <th>Level</th>
                            <th>Sender</th>
                            <th>Subject</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
{self._generate_table_rows(results_df)}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        # Save to file
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return self.output_path
    
    def _generate_table_rows(self, results_df: pd.DataFrame) -> str:
        """Generate HTML table rows for top 30 emails"""
        top_30 = results_df.sort_values('priority_rank').head(30)
        
        rows = []
        for _, row in top_30.iterrows():
            level_class = f"level-{row['urgency_level'].lower()}"
            badge_class = f"badge-{row['urgency_level'].lower()}"
            
            # Truncate subject
            subject = str(row['subject'])[:80] + ('...' if len(str(row['subject'])) > 80 else '')
            
            row_html = f"""                        <tr class="{level_class}">
                            <td>{int(row['priority_rank'])}</td>
                            <td><strong>{int(row['urgency_score'])}</strong></td>
                            <td><span class="badge {badge_class}">{row['urgency_level']}</span></td>
                            <td>{row['sender']}</td>
                            <td><strong>{subject}</strong></td>
                            <td>{row['timestamp']}</td>
                        </tr>"""
            rows.append(row_html)
        
        return '\n'.join(rows)
