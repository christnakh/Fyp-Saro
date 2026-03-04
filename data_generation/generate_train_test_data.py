"""
Generate Large Dataset and Split into Train/Test Sets
======================================================

This script generates a large synthetic dataset and splits it into training
and testing sets for machine learning model development. The dataset size
is chosen to ensure sufficient data for robust model training.

Key considerations:
- Minimum 10x the number of features (we have ~16 features, so 3000 samples is sufficient)
- 80/20 train/test split is standard practice
- Reproducible through random seed control

Author: FYP Team G09
Date: 2026
"""

import pandas as pd  # DataFrame operations
import numpy as np  # Numerical operations
from sklearn.model_selection import train_test_split  # Data splitting utility
import os  # File system operations
import sys  # System-specific parameters and functions

# ============================================================================
# PATH CONFIGURATION
# ============================================================================
# Add parent directory to Python path to enable imports
# This allows importing from the data_generation module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_generation.synthetic_data_generator import SteelWasteDataGenerator

def generate_and_split_data(n_projects: int = 3000, test_size: float = 0.2, seed: int = 42):
    """
    Generate a large dataset and split into train/test sets.
    
    This function creates a synthetic dataset large enough for machine learning,
    then splits it into training and testing subsets. The training set is used
    to train the model, while the test set is held out for final evaluation.
    
    Dataset size rationale:
    - Rule of thumb: 10x the number of features minimum
    - We have ~16 features, so 3000 samples provides good coverage
    - Larger datasets generally lead to better model performance
    
    Train/test split rationale:
    - 80% training, 20% testing is standard practice
    - Test set should be large enough for reliable evaluation
    - 20% of 3000 = 600 test samples (sufficient for evaluation)
    
    Args:
        n_projects: Total number of projects to generate (default: 3000)
        test_size: Proportion of data for testing (default: 0.2 = 20%)
            - 0.2 means 20% test, 80% train
        seed: Random seed for reproducibility (default: 42)
    
    Returns:
        tuple: (train_df, test_df) - Training and testing DataFrames
    """
    print("=" * 70)
    print("Generating Large Dataset for Machine Learning")
    print("=" * 70)
    
    # Create generator
    generator = SteelWasteDataGenerator(seed=seed)
    
    # Generate full dataset
    print(f"\nGenerating {n_projects} projects...")
    df = generator.generate_dataset(n_projects=n_projects, start_id=1000)
    
    print(f"\nDataset Statistics:")
    print(f"  Total projects: {len(df)}")
    print(f"  Average waste: {df['steel_waste_percentage'].mean():.2f}%")
    print(f"  Std deviation: {df['steel_waste_percentage'].std():.2f}%")
    print(f"  Min waste: {df['steel_waste_percentage'].min():.2f}%")
    print(f"  Max waste: {df['steel_waste_percentage'].max():.2f}%")
    
    # Split into train and test
    print(f"\nSplitting data into train/test sets (test_size={test_size:.0%})...")
    train_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=seed,
        stratify=None  # Can't stratify on continuous target, but we'll ensure distribution
    )
    
    print(f"\nSplit Results:")
    print(f"  Training set: {len(train_df)} projects ({len(train_df)/len(df):.1%})")
    print(f"  Test set: {len(test_df)} projects ({len(test_df)/len(df):.1%})")
    
    print(f"\nTraining Set Statistics:")
    print(f"  Average waste: {train_df['steel_waste_percentage'].mean():.2f}%")
    print(f"  Std deviation: {train_df['steel_waste_percentage'].std():.2f}%")
    
    print(f"\nTest Set Statistics:")
    print(f"  Average waste: {test_df['steel_waste_percentage'].mean():.2f}%")
    print(f"  Std deviation: {test_df['steel_waste_percentage'].std():.2f}%")
    
    # Get parent directory path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(parent_dir, 'data')
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Save datasets to data folder
    train_file = os.path.join(data_dir, 'train_data.csv')
    test_file = os.path.join(data_dir, 'test_data.csv')
    full_file = os.path.join(data_dir, 'full_dataset.csv')
    
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)
    df.to_csv(full_file, index=False)
    
    print(f"\nFiles saved to data/ folder:")
    print(f"  - {train_file} ({len(train_df)} rows)")
    print(f"  - {test_file} ({len(test_df)} rows)")
    print(f"  - {full_file} ({len(df)} rows)")
    
    # Show distribution comparison
    print(f"\nDistribution Comparison:")
    print(f"  Train waste range: {train_df['steel_waste_percentage'].min():.2f}% - {train_df['steel_waste_percentage'].max():.2f}%")
    print(f"  Test waste range: {test_df['steel_waste_percentage'].min():.2f}% - {test_df['steel_waste_percentage'].max():.2f}%")
    
    return train_df, test_df


def main():
    """Main function to generate and split data."""
    # Generate 3000 projects (good for ML - rule of thumb: 10x features minimum)
    # We have ~16 features, so 3000 is more than sufficient
    train_df, test_df = generate_and_split_data(
        n_projects=3000,
        test_size=0.2,
        seed=42
    )
    
    print("\n" + "=" * 70)
    print("Data Generation Complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run 'model_comparison.py' to train and compare 10 ML models")
    print("  2. The best model will be automatically selected and saved")
    print("=" * 70)


if __name__ == "__main__":
    main()

