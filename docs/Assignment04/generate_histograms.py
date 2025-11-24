"""
Resource Loading Histogram Generator
Assignment 04 - Project Management
Mindful Eating Agent Project
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

def create_individual_histograms_initial():
    """Create initial resource loading histograms for each team member"""
    
    # Initial resource loading data
    weeks = list(range(1, 17))
    week_labels = [f'W{i}' for i in weeks]
    
    dawood_hours = [40, 40, 40, 32, 32, 40, 24, 24, 24, 24, 24, 32, 32, 40, 40, 16]
    gulsher_hours = [32, 40, 32, 40, 40, 32, 40, 48, 48, 48, 48, 48, 48, 32, 40, 16]
    ahsan_hours = [40, 32, 40, 40, 40, 32, 24, 48, 48, 48, 48, 40, 40, 40, 24, 8]
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    fig.suptitle('Initial Resource Loading Histograms (Before Leveling)', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Dawood Hussain
    ax1 = axes[0]
    bars1 = ax1.bar(week_labels, dawood_hours, color='#3498db', alpha=0.7, edgecolor='black')
    ax1.axhline(y=40, color='green', linestyle='--', linewidth=2, label='Standard Capacity (40h)')
    ax1.set_ylabel('Hours per Week', fontsize=11, fontweight='bold')
    ax1.set_title('Dawood Hussain - Project Manager', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 60)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Highlight under-allocation
    for i, (bar, hours) in enumerate(zip(bars1, dawood_hours)):
        if hours < 40:
            bar.set_color('#f39c12')
            bar.set_alpha(0.8)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars1, dawood_hours)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(hours)}h\n{int(hours/40*100)}%',
                ha='center', va='bottom', fontsize=8)
    
    # Gulsher Khan
    ax2 = axes[1]
    bars2 = ax2.bar(week_labels, gulsher_hours, color='#3498db', alpha=0.7, edgecolor='black')
    ax2.axhline(y=40, color='green', linestyle='--', linewidth=2, label='Standard Capacity (40h)')
    ax2.set_ylabel('Hours per Week', fontsize=11, fontweight='bold')
    ax2.set_title('Gulsher Khan - Technical Lead', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 60)
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Highlight over-allocation
    for i, (bar, hours) in enumerate(zip(bars2, gulsher_hours)):
        if hours > 40:
            bar.set_color('#e74c3c')
            bar.set_alpha(0.8)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars2, gulsher_hours)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(hours)}h\n{int(hours/40*100)}%',
                ha='center', va='bottom', fontsize=8)
    
    # Ahsan Faraz
    ax3 = axes[2]
    bars3 = ax3.bar(week_labels, ahsan_hours, color='#3498db', alpha=0.7, edgecolor='black')
    ax3.axhline(y=40, color='green', linestyle='--', linewidth=2, label='Standard Capacity (40h)')
    ax3.set_xlabel('Week Number', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Hours per Week', fontsize=11, fontweight='bold')
    ax3.set_title('Ahsan Faraz - AI/ML Developer', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 60)
    ax3.legend(loc='upper right')
    ax3.grid(axis='y', alpha=0.3)
    
    # Highlight over-allocation
    for i, (bar, hours) in enumerate(zip(bars3, ahsan_hours)):
        if hours > 40:
            bar.set_color('#e74c3c')
            bar.set_alpha(0.8)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars3, ahsan_hours)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(hours)}h\n{int(hours/40*100)}%',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('initial_individual_histograms.png', dpi=300, bbox_inches='tight')
    print("✓ Created: initial_individual_histograms.png")
    plt.close()


def create_individual_histograms_leveled():
    """Create leveled resource loading histograms for each team member"""
    
    # Leveled resource loading data
    weeks = list(range(1, 18))
    week_labels = [f'W{i}' for i in weeks]
    
    dawood_hours = [40, 40, 40, 32, 32, 40, 32, 32, 32, 32, 36, 36, 36, 40, 40, 40, 32]
    gulsher_hours = [32, 40, 32, 40, 40, 32, 40, 40, 40, 40, 40, 40, 40, 40, 40, 32, 24]
    ahsan_hours = [40, 32, 40, 40, 40, 32, 32, 40, 40, 40, 40, 40, 40, 40, 32, 24, 16]
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    fig.suptitle('Leveled Resource Loading Histograms (After Leveling)', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Dawood Hussain
    ax1 = axes[0]
    bars1 = ax1.bar(week_labels, dawood_hours, color='#27ae60', alpha=0.7, edgecolor='black')
    ax1.axhline(y=40, color='green', linestyle='--', linewidth=2, label='Standard Capacity (40h)')
    ax1.set_ylabel('Hours per Week', fontsize=11, fontweight='bold')
    ax1.set_title('Dawood Hussain - Project Manager (Leveled)', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 60)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars1, dawood_hours)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(hours)}h\n{int(hours/40*100)}%',
                ha='center', va='bottom', fontsize=8)
    
    # Gulsher Khan
    ax2 = axes[1]
    bars2 = ax2.bar(week_labels, gulsher_hours, color='#27ae60', alpha=0.7, edgecolor='black')
    ax2.axhline(y=40, color='green', linestyle='--', linewidth=2, label='Standard Capacity (40h)')
    ax2.set_ylabel('Hours per Week', fontsize=11, fontweight='bold')
    ax2.set_title('Gulsher Khan - Technical Lead (Leveled)', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 60)
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars2, gulsher_hours)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(hours)}h\n{int(hours/40*100)}%',
                ha='center', va='bottom', fontsize=8)
    
    # Ahsan Faraz
    ax3 = axes[2]
    bars3 = ax3.bar(week_labels, ahsan_hours, color='#27ae60', alpha=0.7, edgecolor='black')
    ax3.axhline(y=40, color='green', linestyle='--', linewidth=2, label='Standard Capacity (40h)')
    ax3.set_xlabel('Week Number', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Hours per Week', fontsize=11, fontweight='bold')
    ax3.set_title('Ahsan Faraz - AI/ML Developer (Leveled)', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 60)
    ax3.legend(loc='upper right')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars3, ahsan_hours)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(hours)}h\n{int(hours/40*100)}%',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('leveled_individual_histograms.png', dpi=300, bbox_inches='tight')
    print("✓ Created: leveled_individual_histograms.png")
    plt.close()


def create_project_level_comparison():
    """Create before/after comparison of project-level resource usage"""
    
    weeks = list(range(1, 17))
    week_labels = [f'W{i}' for i in weeks]
    
    # Initial total hours
    initial_total = [112, 112, 112, 112, 112, 104, 88, 120, 120, 120, 120, 120, 120, 112, 104, 40]
    
    # Leveled total hours (extended to 17 weeks)
    leveled_weeks = list(range(1, 18))
    leveled_week_labels = [f'W{i}' for i in leveled_weeks]
    leveled_total = [112, 112, 112, 112, 112, 104, 104, 112, 112, 112, 116, 116, 116, 120, 112, 96, 72]
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Project-Level Resource Usage: Before vs After Leveling', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Before leveling
    bars1 = ax1.bar(week_labels, initial_total, color='#3498db', alpha=0.7, edgecolor='black')
    ax1.axhline(y=120, color='red', linestyle='--', linewidth=2, label='Team Capacity (120h)')
    ax1.set_ylabel('Total Team Hours per Week', fontsize=11, fontweight='bold')
    ax1.set_title('BEFORE Leveling - Resource Over-allocation in Weeks 8-13', 
                  fontsize=12, fontweight='bold', color='#e74c3c')
    ax1.set_ylim(0, 140)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Highlight over-allocation
    for i, (bar, hours) in enumerate(zip(bars1, initial_total)):
        if hours > 120:
            bar.set_color('#e74c3c')
            bar.set_alpha(0.8)
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{int(hours)}h',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # After leveling
    bars2 = ax2.bar(leveled_week_labels, leveled_total, color='#27ae60', alpha=0.7, edgecolor='black')
    ax2.axhline(y=120, color='green', linestyle='--', linewidth=2, label='Team Capacity (120h)')
    ax2.set_xlabel('Week Number', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Total Team Hours per Week', fontsize=11, fontweight='bold')
    ax2.set_title('AFTER Leveling - Balanced Resource Distribution (Extended to 17 weeks)', 
                  fontsize=12, fontweight='bold', color='#27ae60')
    ax2.set_ylim(0, 140)
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (bar, hours) in enumerate(zip(bars2, leveled_total)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{int(hours)}h',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('project_level_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: project_level_comparison.png")
    plt.close()


def create_stacked_comparison():
    """Create stacked bar chart showing resource distribution"""
    
    weeks_initial = list(range(1, 17))
    week_labels_initial = [f'W{i}' for i in weeks_initial]
    
    # Initial data
    dawood_initial = [40, 40, 40, 32, 32, 40, 24, 24, 24, 24, 24, 32, 32, 40, 40, 16]
    gulsher_initial = [32, 40, 32, 40, 40, 32, 40, 48, 48, 48, 48, 48, 48, 32, 40, 16]
    ahsan_initial = [40, 32, 40, 40, 40, 32, 24, 48, 48, 48, 48, 40, 40, 40, 24, 8]
    
    # Leveled data
    weeks_leveled = list(range(1, 18))
    week_labels_leveled = [f'W{i}' for i in weeks_leveled]
    
    dawood_leveled = [40, 40, 40, 32, 32, 40, 32, 32, 32, 32, 36, 36, 36, 40, 40, 40, 32]
    gulsher_leveled = [32, 40, 32, 40, 40, 32, 40, 40, 40, 40, 40, 40, 40, 40, 40, 32, 24]
    ahsan_leveled = [40, 32, 40, 40, 40, 32, 32, 40, 40, 40, 40, 40, 40, 40, 32, 24, 16]
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))
    fig.suptitle('Resource Distribution: Stacked View Comparison', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Before leveling
    ax1.bar(week_labels_initial, dawood_initial, label='Dawood (PM)', 
            color='#3498db', alpha=0.8, edgecolor='black')
    ax1.bar(week_labels_initial, gulsher_initial, bottom=dawood_initial,
            label='Gulsher (Tech Lead)', color='#e74c3c', alpha=0.8, edgecolor='black')
    
    bottom_initial = [d + g for d, g in zip(dawood_initial, gulsher_initial)]
    ax1.bar(week_labels_initial, ahsan_initial, bottom=bottom_initial,
            label='Ahsan (AI/ML Dev)', color='#f39c12', alpha=0.8, edgecolor='black')
    
    ax1.axhline(y=120, color='red', linestyle='--', linewidth=2, label='Team Capacity')
    ax1.set_ylabel('Total Hours per Week', fontsize=11, fontweight='bold')
    ax1.set_title('BEFORE Leveling - Stacked Resource Distribution', 
                  fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 150)
    ax1.legend(loc='upper right', ncol=4)
    ax1.grid(axis='y', alpha=0.3)
    
    # After leveling
    ax2.bar(week_labels_leveled, dawood_leveled, label='Dawood (PM)', 
            color='#3498db', alpha=0.8, edgecolor='black')
    ax2.bar(week_labels_leveled, gulsher_leveled, bottom=dawood_leveled,
            label='Gulsher (Tech Lead)', color='#27ae60', alpha=0.8, edgecolor='black')
    
    bottom_leveled = [d + g for d, g in zip(dawood_leveled, gulsher_leveled)]
    ax2.bar(week_labels_leveled, ahsan_leveled, bottom=bottom_leveled,
            label='Ahsan (AI/ML Dev)', color='#9b59b6', alpha=0.8, edgecolor='black')
    
    ax2.axhline(y=120, color='green', linestyle='--', linewidth=2, label='Team Capacity')
    ax2.set_xlabel('Week Number', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Total Hours per Week', fontsize=11, fontweight='bold')
    ax2.set_title('AFTER Leveling - Balanced Stacked Distribution', 
                  fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 150)
    ax2.legend(loc='upper right', ncol=4)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('stacked_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: stacked_comparison.png")
    plt.close()


def main():
    """Generate all histograms"""
    print("\n" + "="*60)
    print("GENERATING RESOURCE LOADING HISTOGRAMS")
    print("Assignment 04 - Mindful Eating Agent Project")
    print("="*60 + "\n")
    
    print("Creating individual resource histograms (initial)...")
    create_individual_histograms_initial()
    
    print("Creating individual resource histograms (leveled)...")
    create_individual_histograms_leveled()
    
    print("Creating project-level comparison...")
    create_project_level_comparison()
    
    print("Creating stacked comparison...")
    create_stacked_comparison()
    
    print("\n" + "="*60)
    print("✓ ALL HISTOGRAMS GENERATED SUCCESSFULLY")
    print("="*60 + "\n")
    print("Generated files:")
    print("  1. initial_individual_histograms.png")
    print("  2. leveled_individual_histograms.png")
    print("  3. project_level_comparison.png")
    print("  4. stacked_comparison.png")
    print()


if __name__ == "__main__":
    main()
