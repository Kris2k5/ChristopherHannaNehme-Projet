"""
Chart Generator Module
Generates PNG visualization charts for email urgency analysis
"""

import os
from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from src.config import CHART_COLORS, CHART_DPI, CHART_WIDTH, CHART_HEIGHT, CHARTS_DIR


class ChartGenerator:
    """Generates high-quality PNG charts for urgency analysis"""
    
    def __init__(self, output_dir: str = CHARTS_DIR):
        """
        Initialize chart generator
        
        Args:
            output_dir: Directory to save charts
        """
        self.output_dir = output_dir
        self.colors = CHART_COLORS
        self.dpi = CHART_DPI
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_all_charts(self, results_df: pd.DataFrame) -> Dict[str, str]:
        """
        Generate all charts and return their file paths
        
        Args:
            results_df: DataFrame with urgency analysis results
            
        Returns:
            Dictionary mapping chart names to file paths
        """
        chart_paths = {}
        
        # Generate distribution pie chart
        dist_path = self.generate_distribution_chart(results_df)
        chart_paths['distribution'] = dist_path
        
        # Generate scores bar chart
        scores_path = self.generate_scores_chart(results_df)
        chart_paths['scores'] = scores_path
        
        # Generate timeline chart
        timeline_path = self.generate_timeline_chart(results_df)
        chart_paths['timeline'] = timeline_path
        
        return chart_paths
    
    def generate_distribution_chart(self, results_df: pd.DataFrame) -> str:
        """
        Generate pie chart showing distribution of urgency levels
        
        Args:
            results_df: DataFrame with urgency analysis results
            
        Returns:
            Path to saved chart file
        """
        # Count emails by urgency level
        counts = results_df['urgency_level'].value_counts()
        
        # Define order and colors
        levels = ['Critical', 'High', 'Medium', 'Low']
        colors = [self.colors['critical'], self.colors['high'], 
                 self.colors['medium'], self.colors['low']]
        
        # Prepare data in correct order
        sizes = [counts.get(level, 0) for level in levels]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(CHART_WIDTH, CHART_HEIGHT), dpi=self.dpi)
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=levels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 14, 'weight': 'bold'}
        )
        
        # Enhance autotext (percentages)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(16)
            autotext.set_weight('bold')
        
        # Add count in legend
        legend_labels = [f'{level}: {count} emails' for level, count in zip(levels, sizes)]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        
        ax.set_title('Email Urgency Distribution', fontsize=20, weight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save chart
        output_path = os.path.join(self.output_dir, 'urgency_distribution.png')
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_scores_chart(self, results_df: pd.DataFrame) -> str:
        """
        Generate bar chart showing urgency scores for all emails
        
        Args:
            results_df: DataFrame with urgency analysis results
            
        Returns:
            Path to saved chart file
        """
        # Sort by priority rank
        df_sorted = results_df.sort_values('priority_rank')
        
        # Assign colors based on urgency level
        def get_color(level: str) -> str:
            level_map = {
                'Critical': self.colors['critical'],
                'High': self.colors['high'],
                'Medium': self.colors['medium'],
                'Low': self.colors['low']
            }
            return level_map.get(level, self.colors['low'])
        
        bar_colors = df_sorted['urgency_level'].apply(get_color)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(CHART_WIDTH, CHART_HEIGHT), dpi=self.dpi)
        
        # Create bar chart
        bars = ax.bar(
            range(len(df_sorted)), 
            df_sorted['urgency_score'],
            color=bar_colors,
            edgecolor='black',
            linewidth=0.5
        )
        
        # Add threshold lines
        ax.axhline(y=75, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Critical threshold (76)')
        ax.axhline(y=50, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='High threshold (51)')
        ax.axhline(y=25, color='gold', linestyle='--', linewidth=2, alpha=0.7, label='Medium threshold (26)')
        
        # Customize chart
        ax.set_xlabel('Email ID (sorted by priority)', fontsize=14, weight='bold')
        ax.set_ylabel('Urgency Score', fontsize=14, weight='bold')
        ax.set_title('Urgency Scores by Email', fontsize=20, weight='bold', pad=20)
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
        ax.legend(loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        # Save chart
        output_path = os.path.join(self.output_dir, 'urgency_scores.png')
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_timeline_chart(self, results_df: pd.DataFrame) -> str:
        """
        Generate timeline chart showing urgency trends over time
        
        Args:
            results_df: DataFrame with urgency analysis results
            
        Returns:
            Path to saved chart file
        """
        # Convert timestamp to datetime
        results_df['timestamp'] = pd.to_datetime(results_df['timestamp'])
        results_df['date'] = results_df['timestamp'].dt.date
        
        # Group by date and urgency level
        date_urgency = results_df.groupby(['date', 'urgency_level']).size().unstack(fill_value=0)
        
        # Ensure all levels are present
        for level in ['Critical', 'High', 'Medium', 'Low']:
            if level not in date_urgency.columns:
                date_urgency[level] = 0
        
        # Reorder columns
        date_urgency = date_urgency[['Critical', 'High', 'Medium', 'Low']]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(CHART_WIDTH, CHART_HEIGHT), dpi=self.dpi)
        
        # Create stacked bar chart
        bottom = None
        for level in ['Low', 'Medium', 'High', 'Critical']:  # Bottom to top
            color_key = level.lower()
            if bottom is None:
                ax.bar(date_urgency.index, date_urgency[level], 
                      label=level, color=self.colors[color_key], edgecolor='black', linewidth=0.5)
                bottom = date_urgency[level]
            else:
                ax.bar(date_urgency.index, date_urgency[level], 
                      bottom=bottom, label=level, color=self.colors[color_key], 
                      edgecolor='black', linewidth=0.5)
                bottom = bottom + date_urgency[level]
        
        # Customize chart
        ax.set_xlabel('Date', fontsize=14, weight='bold')
        ax.set_ylabel('Number of Emails', fontsize=14, weight='bold')
        ax.set_title('Urgency Trends Over Time', fontsize=20, weight='bold', pad=20)
        ax.legend(loc='upper left', fontsize=12, title='Urgency Level')
        ax.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
        
        # Format x-axis dates
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Save chart
        output_path = os.path.join(self.output_dir, 'urgency_timeline.png')
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
