"""
Dashboard Generator Module
Creates interactive HTML dashboard for email urgency visualization
"""

import os
from typing import Dict
import pandas as pd
from datetime import datetime
from src.config import DASHBOARD_FILE, CHART_COLORS


class DashboardGenerator:
    """Generates interactive HTML dashboard for urgency analysis"""
    
    def __init__(self, output_path: str = DASHBOARD_FILE):
        """
        Initialize dashboard generator
        
        Args:
            output_path: Path to save HTML dashboard
        """
        self.output_path = output_path
        self.colors = CHART_COLORS
        
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
        stats = self._calculate_statistics(results_df)
        
        # Generate HTML
        html = self._generate_html(results_df, stats)
        
        # Save to file
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return self.output_path
    
    def _calculate_statistics(self, results_df: pd.DataFrame) -> Dict:
        """Calculate summary statistics"""
        stats = {
            'total': len(results_df),
            'critical': len(results_df[results_df['urgency_level'] == 'Critical']),
            'high': len(results_df[results_df['urgency_level'] == 'High']),
            'medium': len(results_df[results_df['urgency_level'] == 'Medium']),
            'low': len(results_df[results_df['urgency_level'] == 'Low']),
            'avg_score': results_df['urgency_score'].mean(),
            'median_score': results_df['urgency_score'].median(),
        }
        
        # Get highest urgency email
        if len(results_df) > 0:
            highest = results_df.loc[results_df['urgency_score'].idxmax()]
            stats['highest_email'] = {
                'subject': highest['subject'],
                'sender': highest['sender'],
                'score': highest['urgency_score']
            }
        
        # Get most common keywords
        all_keywords = []
        for kw_str in results_df['flagged_keywords']:
            if pd.notna(kw_str) and kw_str != 'None':
                keywords = [k.strip() for k in str(kw_str).split(',')]
                all_keywords.extend(keywords)
        
        if all_keywords:
            from collections import Counter
            keyword_counts = Counter(all_keywords)
            stats['top_keywords'] = keyword_counts.most_common(5)
        else:
            stats['top_keywords'] = []
        
        return stats
    
    def _generate_html(self, results_df: pd.DataFrame, stats: Dict) -> str:
        """Generate complete HTML content"""
        
        # Prepare data for charts
        dist_data = self._prepare_distribution_data(results_df)
        scores_data = self._prepare_scores_data(results_df)
        timeline_data = self._prepare_timeline_data(results_df)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Urgency Detection Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
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
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .stat-card h3 {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-card.critical .value {{ color: {self.colors['critical']}; }}
        .stat-card.high .value {{ color: {self.colors['high']}; }}
        .stat-card.medium .value {{ color: {self.colors['medium']}; }}
        .stat-card.low .value {{ color: {self.colors['low']}; }}
        
        .charts-section {{
            padding: 30px;
        }}
        
        .chart-container {{
            background: white;
            padding: 25px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .chart-container h2 {{
            margin-bottom: 20px;
            color: #333;
            font-size: 1.5em;
        }}
        
        .chart-wrapper {{
            position: relative;
            height: 400px;
        }}
        
        .table-container {{
            padding: 30px;
            background: white;
        }}
        
        .table-container h2 {{
            margin-bottom: 20px;
            color: #333;
            font-size: 1.5em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }}
        
        thead {{
            background: #667eea;
            color: white;
            position: sticky;
            top: 0;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
        }}
        
        th:hover {{
            background: #5568d3;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .level-critical {{ background-color: {self.colors['critical']}22; }}
        .level-high {{ background-color: {self.colors['high']}22; }}
        .level-medium {{ background-color: {self.colors['medium']}22; }}
        .level-low {{ background-color: {self.colors['low']}22; }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            font-weight: bold;
            color: white;
        }}
        
        .badge-critical {{ background: {self.colors['critical']}; }}
        .badge-high {{ background: {self.colors['high']}; }}
        .badge-medium {{ background: {self.colors['medium']}; }}
        .badge-low {{ background: {self.colors['low']}; }}
        
        .info-section {{
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .info-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .info-card h3 {{
            margin-bottom: 10px;
            color: #667eea;
        }}
        
        footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Email Urgency Detection Dashboard</h1>
            <p>Analysis completed on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>Total Emails Analyzed: <strong>{stats['total']}</strong></p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card critical">
                <h3>🔴 Critical</h3>
                <div class="value">{stats['critical']}</div>
                <p>{stats['critical']/stats['total']*100:.1f}% of total</p>
            </div>
            <div class="stat-card high">
                <h3>🟠 High</h3>
                <div class="value">{stats['high']}</div>
                <p>{stats['high']/stats['total']*100:.1f}% of total</p>
            </div>
            <div class="stat-card medium">
                <h3>🟡 Medium</h3>
                <div class="value">{stats['medium']}</div>
                <p>{stats['medium']/stats['total']*100:.1f}% of total</p>
            </div>
            <div class="stat-card low">
                <h3>🟢 Low</h3>
                <div class="value">{stats['low']}</div>
                <p>{stats['low']/stats['total']*100:.1f}% of total</p>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <h2>📈 Urgency Distribution</h2>
                <div class="chart-wrapper">
                    <canvas id="distributionChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>📊 Urgency Scores</h2>
                <div class="chart-wrapper">
                    <canvas id="scoresChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h2>📅 Timeline Trends</h2>
                <div class="chart-wrapper">
                    <canvas id="timelineChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="table-container">
            <h2>📋 Top 20 Most Urgent Emails</h2>
            <div style="overflow-x: auto; max-height: 600px; overflow-y: auto;">
                <table id="emailTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">Rank</th>
                            <th onclick="sortTable(1)">Score</th>
                            <th onclick="sortTable(2)">Level</th>
                            <th onclick="sortTable(3)">Sender</th>
                            <th onclick="sortTable(4)">Subject</th>
                            <th onclick="sortTable(5)">Keywords</th>
                            <th onclick="sortTable(6)">Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {self._generate_table_rows(results_df)}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="info-section">
            <div class="info-card">
                <h3>📊 Summary Statistics</h3>
                <p><strong>Average Urgency Score:</strong> {stats['avg_score']:.1f}</p>
                <p><strong>Median Urgency Score:</strong> {stats['median_score']:.1f}</p>
            </div>
            
            <div class="info-card">
                <h3>🏆 Highest Urgency Email</h3>
                <p><strong>Subject:</strong> {stats['highest_email']['subject']}</p>
                <p><strong>From:</strong> {stats['highest_email']['sender']}</p>
                <p><strong>Score:</strong> {stats['highest_email']['score']}</p>
            </div>
            
            <div class="info-card">
                <h3>🔑 Most Common Urgency Keywords</h3>
                <ul>
                    {self._generate_keyword_list(stats['top_keywords'])}
                </ul>
            </div>
        </div>
        
        <footer>
            <p>Email Urgency Detection System v1.0 | Generated with ❤️ by Christopher Hanna Nehme</p>
        </footer>
    </div>
    
    <script>
        // Distribution Pie Chart
        const distCtx = document.getElementById('distributionChart').getContext('2d');
        new Chart(distCtx, {{
            type: 'pie',
            data: {{
                labels: {dist_data['labels']},
                datasets: [{{
                    data: {dist_data['values']},
                    backgroundColor: {dist_data['colors']},
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            font: {{ size: 14 }},
                            padding: 15
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.label || '';
                                let value = context.parsed || 0;
                                let total = context.dataset.data.reduce((a, b) => a + b, 0);
                                let percentage = ((value / total) * 100).toFixed(1);
                                return label + ': ' + value + ' emails (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Scores Bar Chart
        const scoresCtx = document.getElementById('scoresChart').getContext('2d');
        new Chart(scoresCtx, {{
            type: 'bar',
            data: {{
                labels: {scores_data['labels']},
                datasets: [{{
                    label: 'Urgency Score',
                    data: {scores_data['values']},
                    backgroundColor: {scores_data['colors']},
                    borderColor: '#333',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        callbacks: {{
                            title: function(context) {{
                                return 'Email ID: ' + context[0].label;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 105,
                        grid: {{ color: '#eee' }},
                        title: {{
                            display: true,
                            text: 'Urgency Score',
                            font: {{ size: 14, weight: 'bold' }}
                        }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        title: {{
                            display: true,
                            text: 'Email ID (sorted by priority)',
                            font: {{ size: 14, weight: 'bold' }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Timeline Stacked Bar Chart
        const timelineCtx = document.getElementById('timelineChart').getContext('2d');
        new Chart(timelineCtx, {{
            type: 'bar',
            data: {{
                labels: {timeline_data['labels']},
                datasets: [
                    {{
                        label: 'Critical',
                        data: {timeline_data['critical']},
                        backgroundColor: '{self.colors["critical"]}',
                        borderColor: '#333',
                        borderWidth: 1
                    }},
                    {{
                        label: 'High',
                        data: {timeline_data['high']},
                        backgroundColor: '{self.colors["high"]}',
                        borderColor: '#333',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Medium',
                        data: {timeline_data['medium']},
                        backgroundColor: '{self.colors["medium"]}',
                        borderColor: '#333',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Low',
                        data: {timeline_data['low']},
                        backgroundColor: '{self.colors["low"]}',
                        borderColor: '#333',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{
                            font: {{ size: 14 }},
                            padding: 15
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        stacked: true,
                        beginAtZero: true,
                        grid: {{ color: '#eee' }},
                        title: {{
                            display: true,
                            text: 'Number of Emails',
                            font: {{ size: 14, weight: 'bold' }}
                        }}
                    }},
                    x: {{
                        stacked: true,
                        grid: {{ display: false }},
                        title: {{
                            display: true,
                            text: 'Date',
                            font: {{ size: 14, weight: 'bold' }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Table sorting function
        function sortTable(n) {{
            const table = document.getElementById("emailTable");
            let switching = true;
            let dir = "asc";
            let switchcount = 0;
            
            while (switching) {{
                switching = false;
                const rows = table.rows;
                
                for (let i = 1; i < (rows.length - 1); i++) {{
                    let shouldSwitch = false;
                    const x = rows[i].getElementsByTagName("TD")[n];
                    const y = rows[i + 1].getElementsByTagName("TD")[n];
                    
                    let xContent = x.textContent.toLowerCase();
                    let yContent = y.textContent.toLowerCase();
                    
                    // Try to parse as numbers for numeric columns
                    const xNum = parseFloat(xContent);
                    const yNum = parseFloat(yContent);
                    
                    if (!isNaN(xNum) && !isNaN(yNum)) {{
                        if (dir === "asc" && xNum > yNum) shouldSwitch = true;
                        if (dir === "desc" && xNum < yNum) shouldSwitch = true;
                    }} else {{
                        if (dir === "asc" && xContent > yContent) shouldSwitch = true;
                        if (dir === "desc" && xContent < yContent) shouldSwitch = true;
                    }}
                    
                    if (shouldSwitch) {{
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                        switchcount++;
                        break;
                    }}
                }}
                
                if (switchcount === 0 && dir === "asc") {{
                    dir = "desc";
                    switching = true;
                }}
            }}
        }}
    </script>
</body>
</html>"""
        
        return html
    
    def _prepare_distribution_data(self, results_df: pd.DataFrame) -> Dict:
        """Prepare data for distribution pie chart"""
        counts = results_df['urgency_level'].value_counts()
        
        levels = ['Critical', 'High', 'Medium', 'Low']
        values = [int(counts.get(level, 0)) for level in levels]
        colors = [self.colors['critical'], self.colors['high'], 
                 self.colors['medium'], self.colors['low']]
        
        return {
            'labels': str(levels),
            'values': str(values),
            'colors': str(colors)
        }
    
    def _prepare_scores_data(self, results_df: pd.DataFrame) -> Dict:
        """Prepare data for scores bar chart"""
        df_sorted = results_df.sort_values('priority_rank')
        
        def get_color(level: str) -> str:
            level_map = {
                'Critical': self.colors['critical'],
                'High': self.colors['high'],
                'Medium': self.colors['medium'],
                'Low': self.colors['low']
            }
            return level_map.get(level, self.colors['low'])
        
        labels = [str(int(eid)) for eid in df_sorted['email_id'].tolist()]
        values = [int(score) for score in df_sorted['urgency_score'].tolist()]
        colors = [get_color(level) for level in df_sorted['urgency_level'].tolist()]
        
        return {
            'labels': str(labels),
            'values': str(values),
            'colors': str(colors)
        }
    
    def _prepare_timeline_data(self, results_df: pd.DataFrame) -> Dict:
        """Prepare data for timeline chart"""
        df = results_df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Group by date and urgency level
        date_urgency = df.groupby(['date', 'urgency_level']).size().unstack(fill_value=0)
        
        # Ensure all levels exist
        for level in ['Critical', 'High', 'Medium', 'Low']:
            if level not in date_urgency.columns:
                date_urgency[level] = 0
        
        labels = [str(date) for date in date_urgency.index]
        critical = [int(v) for v in date_urgency['Critical'].tolist()]
        high = [int(v) for v in date_urgency['High'].tolist()]
        medium = [int(v) for v in date_urgency['Medium'].tolist()]
        low = [int(v) for v in date_urgency['Low'].tolist()]
        
        return {
            'labels': str(labels),
            'critical': str(critical),
            'high': str(high),
            'medium': str(medium),
            'low': str(low)
        }
    
    def _generate_table_rows(self, results_df: pd.DataFrame) -> str:
        """Generate HTML table rows for top 20 emails"""
        top_20 = results_df.sort_values('priority_rank').head(20)
        
        rows = []
        for _, row in top_20.iterrows():
            level_class = f"level-{row['urgency_level'].lower()}"
            badge_class = f"badge-{row['urgency_level'].lower()}"
            
            # Truncate subject and keywords
            subject = str(row['subject'])[:60] + ('...' if len(str(row['subject'])) > 60 else '')
            keywords = str(row['flagged_keywords'])[:50] + ('...' if len(str(row['flagged_keywords'])) > 50 else '')
            
            row_html = f"""
                        <tr class="{level_class}">
                            <td>{int(row['priority_rank'])}</td>
                            <td><strong>{int(row['urgency_score'])}</strong></td>
                            <td><span class="badge {badge_class}">{row['urgency_level']}</span></td>
                            <td>{row['sender']}</td>
                            <td><strong>{subject}</strong></td>
                            <td>{keywords}</td>
                            <td>{row['timestamp']}</td>
                        </tr>"""
            rows.append(row_html)
        
        return '\n'.join(rows)
    
    def _generate_keyword_list(self, top_keywords) -> str:
        """Generate HTML list of top keywords"""
        if not top_keywords:
            return '<li>No keywords found</li>'
        
        items = []
        for keyword, count in top_keywords:
            items.append(f'<li><strong>{keyword}</strong>: {count} occurrences</li>')
        
        return '\n'.join(items)
