"""
Visualization module for sentiment analysis results.
Creates charts, graphs, and HTML dashboards for presentation.
"""
import os
from typing import Optional, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from config import VIZ_SETTINGS, RESULTS_DIR


# Set matplotlib style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


class SentimentVisualizer:
    """
    Creates visualizations for sentiment analysis results.
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save visualizations (default: RESULTS_DIR from config)
        """
        self.output_dir = output_dir or RESULTS_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.settings = VIZ_SETTINGS
        
    def plot_sentiment_distribution(
        self, 
        df: pd.DataFrame, 
        save_path: Optional[str] = None,
        show: bool = False
    ) -> str:
        """
        Create a pie chart of sentiment distribution.
        
        Args:
            df: DataFrame with 'sentiment' column
            save_path: Path to save the figure
            show: Whether to display the plot
            
        Returns:
            Path where the figure was saved
        """
        if 'sentiment' not in df.columns:
            raise ValueError("DataFrame must have 'sentiment' column")
        
        # Count sentiments
        sentiment_counts = df['sentiment'].value_counts()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        colors = self.settings['pie_colors']
        labels = sentiment_counts.index
        sizes = sentiment_counts.values
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors[:len(labels)],
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )
        
        ax.set_title('Sentiment Distribution', fontsize=16, weight='bold', pad=20)
        
        # Equal aspect ratio ensures circular pie
        ax.axis('equal')
        
        # Save figure
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'sentiment_distribution.png')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.settings['dpi'], bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def plot_sentiment_scores_histogram(
        self, 
        df: pd.DataFrame, 
        save_path: Optional[str] = None,
        show: bool = False
    ) -> str:
        """
        Create histogram of compound sentiment scores.
        
        Args:
            df: DataFrame with 'compound_score' column
            save_path: Path to save the figure
            show: Whether to display the plot
            
        Returns:
            Path where the figure was saved
        """
        if 'compound_score' not in df.columns:
            raise ValueError("DataFrame must have 'compound_score' column")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create histogram
        n, bins, patches = ax.hist(
            df['compound_score'], 
            bins=self.settings['histogram_bins'],
            edgecolor='black',
            alpha=0.7
        )
        
        # Color bars based on sentiment
        for i, patch in enumerate(patches):
            bin_center = (bins[i] + bins[i+1]) / 2
            if bin_center >= 0.05:
                patch.set_facecolor('#2ecc71')  # Green for positive
            elif bin_center <= -0.05:
                patch.set_facecolor('#e74c3c')  # Red for negative
            else:
                patch.set_facecolor('#95a5a6')  # Gray for neutral
        
        ax.set_xlabel('Compound Sentiment Score', fontsize=12, weight='bold')
        ax.set_ylabel('Frequency', fontsize=12, weight='bold')
        ax.set_title('Distribution of Sentiment Scores', fontsize=14, weight='bold', pad=15)
        ax.axvline(x=0, color='black', linestyle='--', linewidth=2, alpha=0.5)
        ax.grid(True, alpha=0.3)
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'sentiment_scores_histogram.png')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.settings['dpi'], bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def plot_time_series(
        self, 
        df: pd.DataFrame, 
        timestamp_column: str = 'timestamp',
        save_path: Optional[str] = None,
        show: bool = False
    ) -> str:
        """
        Create time series plot of sentiment over time.
        
        Args:
            df: DataFrame with timestamp and sentiment scores
            timestamp_column: Name of the timestamp column
            save_path: Path to save the figure
            show: Whether to display the plot
            
        Returns:
            Path where the figure was saved
        """
        if timestamp_column not in df.columns or 'compound_score' not in df.columns:
            raise ValueError(f"DataFrame must have '{timestamp_column}' and 'compound_score' columns")
        
        df = df.copy()
        df[timestamp_column] = pd.to_datetime(df[timestamp_column])
        df = df.sort_values(timestamp_column)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plot compound score over time
        ax.plot(df[timestamp_column], df['compound_score'], marker='o', linewidth=2, markersize=4, alpha=0.7)
        
        # Add threshold lines
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
        ax.axhline(y=0.05, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Positive Threshold')
        ax.axhline(y=-0.05, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Negative Threshold')
        
        ax.set_xlabel('Time', fontsize=12, weight='bold')
        ax.set_ylabel('Compound Sentiment Score', fontsize=12, weight='bold')
        ax.set_title('Sentiment Trend Over Time', fontsize=14, weight='bold', pad=15)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'sentiment_time_series.png')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.settings['dpi'], bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def create_wordcloud(
        self, 
        texts: List[str], 
        sentiment_type: str = 'positive',
        save_path: Optional[str] = None,
        show: bool = False
    ) -> str:
        """
        Create word cloud for specific sentiment.
        
        Args:
            texts: List of text strings
            sentiment_type: 'positive' or 'negative'
            save_path: Path to save the figure
            show: Whether to display the plot
            
        Returns:
            Path where the figure was saved
        """
        # Combine all texts
        combined_text = ' '.join(texts)
        
        if not combined_text.strip():
            # Create empty wordcloud
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f'No {sentiment_type} text available', 
                   ha='center', va='center', fontsize=14)
            ax.axis('off')
        else:
            # Create wordcloud
            colormap = 'Greens' if sentiment_type.lower() == 'positive' else 'Reds'
            
            wordcloud = WordCloud(
                width=self.settings['wordcloud_width'],
                height=self.settings['wordcloud_height'],
                background_color='white',
                colormap=colormap,
                max_words=self.settings['max_words_wordcloud'],
                relative_scaling=0.5,
                min_font_size=10
            ).generate(combined_text)
            
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
        
        title = f'{sentiment_type.capitalize()} Sentiment Word Cloud'
        ax.set_title(title, fontsize=16, weight='bold', pad=20)
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, f'wordcloud_{sentiment_type.lower()}.png')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.settings['dpi'], bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def plot_platform_comparison(
        self, 
        df: pd.DataFrame,
        save_path: Optional[str] = None,
        show: bool = False
    ) -> str:
        """
        Create bar chart comparing sentiment across platforms.
        
        Args:
            df: DataFrame with 'platform' and 'sentiment' columns
            save_path: Path to save the figure
            show: Whether to display the plot
            
        Returns:
            Path where the figure was saved
        """
        if 'platform' not in df.columns or 'sentiment' not in df.columns:
            raise ValueError("DataFrame must have 'platform' and 'sentiment' columns")
        
        # Create pivot table
        platform_sentiment = pd.crosstab(df['platform'], df['sentiment'], normalize='index') * 100
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        platform_sentiment.plot(kind='bar', ax=ax, color=self.settings['pie_colors'], width=0.8)
        
        ax.set_xlabel('Platform', fontsize=12, weight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=12, weight='bold')
        ax.set_title('Sentiment Distribution by Platform', fontsize=14, weight='bold', pad=15)
        ax.legend(title='Sentiment', title_fontsize=11, fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'platform_comparison.png')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=self.settings['dpi'], bbox_inches='tight')
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return save_path
    
    def generate_dashboard(
        self, 
        df: pd.DataFrame, 
        summary_stats: dict,
        save_path: Optional[str] = None
    ) -> str:
        """
        Generate HTML dashboard with all visualizations and statistics.
        
        Args:
            df: DataFrame with sentiment analysis results
            summary_stats: Dictionary with summary statistics
            save_path: Path to save the HTML file
            
        Returns:
            Path where the HTML was saved
        """
        if save_path is None:
            save_path = os.path.join(self.output_dir, 'dashboard.html')
        
        # Generate all visualizations
        pie_chart = self.plot_sentiment_distribution(df)
        histogram = self.plot_sentiment_scores_histogram(df)
        
        # Generate word clouds
        positive_texts = df[df['sentiment'] == 'Positive']['text'].tolist() if 'Positive' in df['sentiment'].values else []
        negative_texts = df[df['sentiment'] == 'Negative']['text'].tolist() if 'Negative' in df['sentiment'].values else []
        
        wordcloud_pos = self.create_wordcloud(positive_texts, 'positive') if positive_texts else None
        wordcloud_neg = self.create_wordcloud(negative_texts, 'negative') if negative_texts else None
        
        # Optional: time series and platform comparison
        time_series = None
        platform_chart = None
        
        if 'timestamp' in df.columns:
            try:
                time_series = self.plot_time_series(df)
            except:
                pass
        
        if 'platform' in df.columns:
            try:
                platform_chart = self.plot_platform_comparison(df)
            except:
                pass
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Social Media Sentiment Analysis Dashboard</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    margin-bottom: 10px;
                }}
                .subtitle {{
                    text-align: center;
                    color: #7f8c8d;
                    margin-bottom: 30px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .stat-card.positive {{
                    background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
                }}
                .stat-card.negative {{
                    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                }}
                .stat-card.neutral {{
                    background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
                }}
                .stat-value {{
                    font-size: 2em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .stat-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                .chart-section {{
                    margin-bottom: 40px;
                }}
                .chart-title {{
                    color: #2c3e50;
                    font-size: 1.5em;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                .chart-container {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .chart-container img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .grid-2 {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                    gap: 30px;
                }}
                footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ecf0f1;
                    color: #7f8c8d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Social Media Sentiment Analysis Dashboard</h1>
                <p class="subtitle">Real-time insights into public sentiment and brand perception</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Total Analyzed</div>
                        <div class="stat-value">{summary_stats.get('total_analyzed', 0)}</div>
                    </div>
                    <div class="stat-card positive">
                        <div class="stat-label">Positive</div>
                        <div class="stat-value">{summary_stats.get('positive_percentage', 0):.1f}%</div>
                        <div class="stat-label">({summary_stats.get('positive_count', 0)} posts)</div>
                    </div>
                    <div class="stat-card neutral">
                        <div class="stat-label">Neutral</div>
                        <div class="stat-value">{summary_stats.get('neutral_percentage', 0):.1f}%</div>
                        <div class="stat-label">({summary_stats.get('neutral_count', 0)} posts)</div>
                    </div>
                    <div class="stat-card negative">
                        <div class="stat-label">Negative</div>
                        <div class="stat-value">{summary_stats.get('negative_percentage', 0):.1f}%</div>
                        <div class="stat-label">({summary_stats.get('negative_count', 0)} posts)</div>
                    </div>
                </div>
                
                <div class="chart-section">
                    <h2 class="chart-title">📊 Sentiment Distribution</h2>
                    <div class="grid-2">
                        <div class="chart-container">
                            <img src="{os.path.basename(pie_chart)}" alt="Sentiment Distribution Pie Chart">
                        </div>
                        <div class="chart-container">
                            <img src="{os.path.basename(histogram)}" alt="Sentiment Scores Histogram">
                        </div>
                    </div>
                </div>
                
                {f'''
                <div class="chart-section">
                    <h2 class="chart-title">📈 Sentiment Trend</h2>
                    <div class="chart-container">
                        <img src="{os.path.basename(time_series)}" alt="Sentiment Time Series">
                    </div>
                </div>
                ''' if time_series else ''}
                
                {f'''
                <div class="chart-section">
                    <h2 class="chart-title">🌐 Platform Comparison</h2>
                    <div class="chart-container">
                        <img src="{os.path.basename(platform_chart)}" alt="Platform Comparison">
                    </div>
                </div>
                ''' if platform_chart else ''}
                
                {f'''
                <div class="chart-section">
                    <h2 class="chart-title">☁️ Word Clouds</h2>
                    <div class="grid-2">
                        {'<div class="chart-container"><img src="' + os.path.basename(wordcloud_pos) + '" alt="Positive Word Cloud"></div>' if wordcloud_pos else ''}
                        {'<div class="chart-container"><img src="' + os.path.basename(wordcloud_neg) + '" alt="Negative Word Cloud"></div>' if wordcloud_neg else ''}
                    </div>
                </div>
                ''' if (wordcloud_pos or wordcloud_neg) else ''}
                
                <div class="chart-section">
                    <h2 class="chart-title">📋 Detailed Statistics</h2>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #ecf0f1;">
                            <th style="padding: 12px; text-align: left; border: 1px solid #bdc3c7;">Metric</th>
                            <th style="padding: 12px; text-align: right; border: 1px solid #bdc3c7;">Value</th>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ecf0f1;">Average Compound Score</td>
                            <td style="padding: 10px; border: 1px solid #ecf0f1; text-align: right;">{summary_stats.get('avg_compound_score', 0):.4f}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="padding: 10px; border: 1px solid #ecf0f1;">Average Positive Score</td>
                            <td style="padding: 10px; border: 1px solid #ecf0f1; text-align: right;">{summary_stats.get('avg_positive_score', 0):.4f}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ecf0f1;">Average Neutral Score</td>
                            <td style="padding: 10px; border: 1px solid #ecf0f1; text-align: right;">{summary_stats.get('avg_neutral_score', 0):.4f}</td>
                        </tr>
                        <tr style="background-color: #f9f9f9;">
                            <td style="padding: 10px; border: 1px solid #ecf0f1;">Average Negative Score</td>
                            <td style="padding: 10px; border: 1px solid #ecf0f1; text-align: right;">{summary_stats.get('avg_negative_score', 0):.4f}</td>
                        </tr>
                    </table>
                </div>
                
                <footer>
                    <p>Generated by Social Media Sentiment Analysis System</p>
                    <p>Powered by VADER Sentiment Analysis</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        # Write HTML file
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return save_path
