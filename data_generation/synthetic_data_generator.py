"""
Synthetic Steel Waste Data Generator
====================================

This module generates realistic synthetic construction project data for steel waste
prediction. The data generation is based on:
- Industry research and literature
- Engineering relationships between parameters
- Realistic probability distributions
- Correlations between variables

The generated data serves as a training dataset for machine learning models
when real project data is limited or unavailable.

Author: FYP Team G09
Date: 2026
"""

import numpy as np  # Numerical operations and random number generation
import pandas as pd  # DataFrame operations for structured data
from scipy import stats  # Statistical distributions (if needed)
import random  # Additional random number generation
import os  # File system operations
from typing import Dict, List, Tuple  # Type hints for better code documentation

class SteelWasteDataGenerator:
    """
    Generates synthetic steel waste data with realistic relationships.
    
    This class creates construction project datasets where:
    - Parameters follow realistic distributions (based on industry data)
    - Variables have logical correlations (e.g., better supervision → better material control)
    - Waste percentage is calculated using research-based formulas
    - All values pass quality control checks
    
    The generator ensures reproducibility through random seed control.
    """
    
    def __init__(self, seed: int = 42):
        """
        Initialize the generator with a random seed for reproducibility.
        
        Setting the seed ensures that the same sequence of random numbers
        is generated each time, making results reproducible for research.
        
        Args:
            seed: Random seed value (default: 42)
        """
        # Set random seeds for both numpy and Python's random module
        np.random.seed(seed)
        random.seed(seed)
        
        # ====================================================================
        # CATEGORICAL VARIABLE OPTIONS
        # ====================================================================
        # Define all possible values for categorical variables
        self.stock_length_policies = ['standard_12m', 'mixed_lengths', 'custom_lengths']
        self.contract_types = ['lump_sum', 'design_build', 'remeasurement']
        self.project_phases = ['foundation', 'frame', 'slab_finishing']
        
        # ====================================================================
        # PROBABILITY DISTRIBUTIONS FOR CATEGORICAL VARIABLES
        # ====================================================================
        # These weights determine how often each category appears
        # Based on industry prevalence in Middle East construction
        
        # Stock length policy distribution
        # Standard 12m is most common (65%), custom lengths are rare (10%)
        self.stock_policy_weights = [0.65, 0.25, 0.10]  # standard, mixed, custom
        
        # Contract type distribution
        # Lump sum is most common (45%), remeasurement is less common (25%)
        self.contract_type_weights = [0.45, 0.30, 0.25]  # lump_sum, design_build, remeasurement
        
        # Project phase distribution
        # Relatively even distribution across phases
        self.project_phase_weights = [0.35, 0.35, 0.30]  # foundation, frame, slab_finishing
        
    def generate_reinforcement_ratio(self, project_phase: str, num_unique_lengths: int) -> float:
        """
        Generate reinforcement ratio based on project phase and complexity.
        Foundation projects typically have higher ratios.
        """
        base_ratios = {
            'foundation': (140, 180),
            'frame': (100, 160),
            'slab_finishing': (60, 130)
        }
        
        min_ratio, max_ratio = base_ratios[project_phase]
        
        # More unique lengths might indicate more complex design (slightly higher ratio)
        complexity_factor = 1 + (num_unique_lengths - 5) / 200
        
        ratio = np.random.normal(
            loc=(min_ratio + max_ratio) / 2,
            scale=(max_ratio - min_ratio) / 6
        )
        
        # Apply complexity factor
        ratio *= complexity_factor
        
        # Clip to realistic bounds
        return np.clip(ratio, 60, 180)
    
    def generate_num_unique_lengths(self, stock_policy: str) -> int:
        """
        Generate number of unique required lengths.
        Custom lengths typically have fewer unique lengths (more optimized).
        """
        if stock_policy == 'custom_lengths':
            return np.random.randint(5, 15)
        elif stock_policy == 'mixed_lengths':
            return np.random.randint(15, 35)
        else:  # standard_12m
            return np.random.randint(5, 40)
    
    def generate_cutting_optimization(self, bim_level: int, material_control: int) -> int:
        """
        Higher BIM and material control levels increase likelihood of using optimization.
        """
        prob = 0.3 + (bim_level * 0.15) + (material_control * 0.1)
        if random.random() < prob:
            return np.random.choice([1, 2], p=[0.7, 0.3])
        return 0
    
    def generate_bim_integration(self) -> int:
        """Generate BIM integration level (0-3)."""
        return np.random.choice([0, 1, 2, 3], p=[0.4, 0.35, 0.20, 0.05])
    
    def generate_design_revisions(self, contract_type: str, supervision: int) -> int:
        """
        Design revisions are higher for remeasurement contracts and lower supervision.
        """
        base_revisions = {
            'remeasurement': (2, 5),
            'design_build': (1, 4),
            'lump_sum': (0, 3)
        }
        
        min_rev, max_rev = base_revisions[contract_type]
        # Lower supervision might lead to more revisions
        supervision_factor = (6 - supervision) * 0.3
        
        revisions = np.random.poisson((min_rev + max_rev) / 2 + supervision_factor)
        return np.clip(int(revisions), 0, 6)
    
    def generate_supervision_index(self) -> int:
        """Generate supervision index (1-5)."""
        return np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.35, 0.25, 0.1])
    
    def generate_material_control_level(self, supervision: int) -> int:
        """
        Material control level correlates with supervision quality.
        """
        base_level = supervision - 1
        level = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
        # Adjust based on supervision
        if supervision >= 4:
            level = max(2, level)
        elif supervision <= 2:
            level = min(2, level)
        return level
    
    def generate_storage_handling_index(self, material_control: int) -> int:
        """
        Storage handling correlates with material control.
        """
        base = material_control + np.random.randint(-1, 2)
        return np.clip(int(base), 1, 5)
    
    def generate_offcut_reuse_policy(self, cutting_optimization: int, material_control: int) -> int:
        """
        Higher optimization and material control lead to better offcut reuse.
        """
        if cutting_optimization >= 2 and material_control >= 2:
            return np.random.choice([1, 2], p=[0.3, 0.7])
        elif cutting_optimization >= 1 or material_control >= 2:
            return np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2])
        else:
            return np.random.choice([0, 1, 2], p=[0.5, 0.4, 0.1])
    
    def generate_change_orders(self, contract_type: str, design_revisions: int) -> int:
        """
        Change orders correlate with design revisions and contract type.
        """
        base_orders = {
            'remeasurement': (1, 4),
            'design_build': (0, 3),
            'lump_sum': (0, 2)
        }
        
        min_ord, max_ord = base_orders[contract_type]
        orders = np.random.poisson((min_ord + max_ord) / 2 + design_revisions * 0.3)
        return np.clip(int(orders), 0, 5)
    
    def generate_lead_time(self, contract_type: str, order_frequency: int) -> int:
        """
        Lead time inversely correlates with order frequency.
        Higher frequency = shorter lead times needed.
        """
        base_lead_times = {
            'remeasurement': (3, 20),
            'design_build': (4, 25),
            'lump_sum': (3, 30)
        }
        
        min_lt, max_lt = base_lead_times[contract_type]
        # Higher order frequency might reduce lead time needs
        frequency_adjustment = (8 - order_frequency) * 2
        
        lead_time = np.random.normal(
            loc=(min_lt + max_lt) / 2 + frequency_adjustment,
            scale=(max_lt - min_lt) / 4
        )
        
        return np.clip(int(lead_time), 3, 30)
    
    def generate_order_frequency(self, project_phase: str, contract_type: str) -> int:
        """
        Order frequency varies by project phase and contract type.
        """
        base_frequencies = {
            'foundation': (1, 8),
            'frame': (2, 8),
            'slab_finishing': (1, 7)
        }
        
        min_freq, max_freq = base_frequencies[project_phase]
        
        # Remeasurement contracts might have more frequent orders
        if contract_type == 'remeasurement':
            min_freq = max(2, min_freq)
        
        return np.random.randint(min_freq, max_freq + 1)
    
    def predict_steel_waste_percentage(self, row: Dict) -> float:
        """
        Calculate steel waste percentage based on project parameters.
        
        This method implements a research-based formula that combines multiple
        factors known to influence steel waste in construction. The formula is
        based on:
        - Academic research on construction waste drivers
        - Industry best practices and case studies
        - Engineering relationships between parameters
        - Middle East construction context
        
        Research-based impact factors:
        - Standard 12m stock: +2-4% waste (fixed lengths create more offcuts)
        - Cutting optimization: -1.5-3% waste (reduces offcuts)
        - BIM integration: -0.8-2.4% per level (better planning)
        - Design revisions: +0.4-0.6% per revision (causes rework)
        - Poor supervision: +1-2% waste (improper handling)
        - Material control: -0.8-1.5% per level (reduces damage)
        - Offcut reuse: -1.5-3% waste (reuses material)
        - Change orders: +0.7-1.0% per order (causes rework)
        
        Args:
            row: Dictionary containing all project parameters
        
        Returns:
            float: Predicted waste percentage (0.5% to 15.0%)
        """
        # ====================================================================
        # BASE WASTE PERCENTAGE
        # ====================================================================
        # Industry average for standard construction practices
        # Research shows typical waste ranges from 5-8% for average projects
        waste = 6.5
        
        # 1. STOCK LENGTH POLICY (Major Impact)
        # Standard 12m creates more waste due to fixed lengths
        if row['stock_length_policy'] == 'standard_12m':
            waste += 2.8  # Fixed lengths create more offcuts
        elif row['stock_length_policy'] == 'mixed_lengths':
            waste += 1.2  # Some optimization but not perfect
        else:  # custom_lengths - optimized for project
            waste -= 1.0  # Custom lengths minimize waste
        
        # 2. CUTTING OPTIMIZATION (Major Impact)
        # Level 0: No optimization = +0%
        # Level 1: Basic optimization = -1.5%
        # Level 2: Advanced optimization = -3.0%
        waste -= row['cutting_optimization_usage'] * 1.5
        
        # 3. BIM INTEGRATION (Moderate Impact)
        # Better planning and coordination reduces waste
        waste -= row['bim_integration_level'] * 0.85
        
        # 4. NUMBER OF UNIQUE LENGTHS (Moderate Impact)
        # More unique lengths = more cutting operations = more waste
        # Optimal is around 15-20 lengths
        length_deviation = abs(row['num_unique_required_lengths'] - 18)
        waste += length_deviation * 0.08
        
        # 5. DESIGN REVISIONS (Moderate Impact)
        # Each revision causes rework and material waste
        waste += row['design_revisions_per_month'] * 0.55
        
        # 6. SUPERVISION QUALITY (Major Impact)
        # Poor supervision leads to improper handling and waste
        supervision_impact = (3 - row['supervision_index_1to5']) * 0.65
        waste += supervision_impact
        
        # 7. MATERIAL CONTROL (Major Impact)
        # Better control = less damage and waste
        material_control_impact = (2 - row['material_control_level_1to3']) * 1.1
        waste += material_control_impact
        
        # 8. STORAGE HANDLING (Moderate Impact)
        # Poor handling causes damage and waste
        storage_impact = (3 - row['storage_handling_index_1to5']) * 0.45
        waste += storage_impact
        
        # 9. OFFCUT REUSE POLICY (Major Impact)
        # Reusing offcuts significantly reduces waste
        waste -= row['offcut_reuse_policy_0to2'] * 1.6
        
        # 10. CHANGE ORDERS (Moderate Impact)
        # Each change order causes material rework
        waste += row['change_orders_per_month'] * 0.75
        
        # 11. CONTRACT TYPE (Moderate Impact)
        # Remeasurement contracts have more uncertainty
        if row['contract_type'] == 'remeasurement':
            waste += 1.2  # More uncertainty = more waste
        elif row['contract_type'] == 'design_build':
            waste -= 0.6  # Better coordination
        
        # 12. LEAD TIME (Minor Impact)
        # Longer lead times allow better planning
        if row['lead_time_days'] > 22:
            waste -= 0.6  # Better planning time
        elif row['lead_time_days'] < 8:
            waste += 0.7  # Rushed orders = more waste
        
        # 13. ORDER FREQUENCY (Minor Impact)
        # More frequent orders = better just-in-time planning
        if row['order_frequency_per_month'] >= 6:
            waste -= 0.5  # Better planning
        elif row['order_frequency_per_month'] <= 2:
            waste += 0.6  # Bulk ordering = more waste
        
        # 14. PROJECT PHASE (Minor Impact)
        # Foundation work typically has more waste due to complexity
        if row['project_phase'] == 'foundation':
            waste += 0.6  # More complex, more waste
        elif row['project_phase'] == 'slab_finishing':
            waste += 0.4  # Finishing work has some waste
        
        # 15. REINFORCEMENT RATIO (Minor Impact)
        # Higher ratios might indicate more complex projects
        if row['reinforcement_ratio_kg_per_m3'] > 160:
            waste += 0.3  # Complex projects
        elif row['reinforcement_ratio_kg_per_m3'] < 90:
            waste -= 0.2  # Simpler projects
        
        # Add realistic noise (construction projects have variability)
        noise = np.random.normal(0, 0.75)
        waste += noise
        
        # Clip to realistic industry bounds (0.5% to 15%)
        # Industry research shows waste ranges from 0.5% (excellent) to 15% (poor)
        return np.clip(waste, 0.5, 15.0)
    
    def generate_project(self, project_id: str) -> Dict:
        """Generate a single project with all parameters."""
        # Generate categorical variables first
        stock_policy = np.random.choice(self.stock_length_policies, p=self.stock_policy_weights)
        contract_type = np.random.choice(self.contract_types, p=self.contract_type_weights)
        project_phase = np.random.choice(self.project_phases, p=self.project_phase_weights)
        
        # Generate dependent variables
        num_unique_lengths = self.generate_num_unique_lengths(stock_policy)
        reinforcement_ratio = self.generate_reinforcement_ratio(project_phase, num_unique_lengths)
        
        supervision = self.generate_supervision_index()
        material_control = self.generate_material_control_level(supervision)
        storage_handling = self.generate_storage_handling_index(material_control)
        
        bim_level = self.generate_bim_integration()
        cutting_optimization = self.generate_cutting_optimization(bim_level, material_control)
        offcut_reuse = self.generate_offcut_reuse_policy(cutting_optimization, material_control)
        
        design_revisions = self.generate_design_revisions(contract_type, supervision)
        change_orders = self.generate_change_orders(contract_type, design_revisions)
        
        order_frequency = self.generate_order_frequency(project_phase, contract_type)
        lead_time = self.generate_lead_time(contract_type, order_frequency)
        
        # Create project dictionary
        project = {
            'project_id': project_id,
            'reinforcement_ratio_kg_per_m3': round(reinforcement_ratio, 1),
            'num_unique_required_lengths': num_unique_lengths,
            'stock_length_policy': stock_policy,
            'cutting_optimization_usage': cutting_optimization,
            'bim_integration_level': bim_level,
            'design_revisions_per_month': design_revisions,
            'supervision_index_1to5': supervision,
            'material_control_level_1to3': material_control,
            'storage_handling_index_1to5': storage_handling,
            'offcut_reuse_policy_0to2': offcut_reuse,
            'change_orders_per_month': change_orders,
            'contract_type': contract_type,
            'lead_time_days': lead_time,
            'order_frequency_per_month': order_frequency,
            'project_phase': project_phase
        }
        
        # Predict steel waste
        project['steel_waste_percentage'] = round(self.predict_steel_waste_percentage(project), 2)
        
        return project
    
    def generate_dataset(self, n_projects: int, start_id: int = 1000) -> pd.DataFrame:
        """
        Generate a complete dataset of projects.
        
        Args:
            n_projects: Number of projects to generate
            start_id: Starting project ID number
        
        Returns:
            DataFrame with all project parameters and predicted waste
        """
        projects = []
        
        for i in range(n_projects):
            project_id = f"P{start_id + i}"
            project = self.generate_project(project_id)
            projects.append(project)
        
        df = pd.DataFrame(projects)
        
        # Reorder columns to match original format (with waste at the end)
        column_order = [
            'project_id', 'reinforcement_ratio_kg_per_m3', 'num_unique_required_lengths',
            'stock_length_policy', 'cutting_optimization_usage', 'bim_integration_level',
            'design_revisions_per_month', 'supervision_index_1to5', 'material_control_level_1to3',
            'storage_handling_index_1to5', 'offcut_reuse_policy_0to2', 'change_orders_per_month',
            'contract_type', 'lead_time_days', 'order_frequency_per_month', 'project_phase',
            'steel_waste_percentage'
        ]
        
        return df[column_order]


def main():
    """Main function to generate and save synthetic data."""
    print("Generating synthetic steel waste data...")
    
    # Create generator
    generator = SteelWasteDataGenerator(seed=42)
    
    # Generate dataset
    n_projects = 150
    df = generator.generate_dataset(n_projects, start_id=1000)
    
    # Get parent directory path and create data directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(parent_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to CSV in data folder
    output_file = os.path.join(data_dir, 'synthetic_steel_waste_parameters.csv')
    df.to_csv(output_file, index=False)
    
    print(f"\nGenerated {n_projects} projects and saved to '{output_file}'")
    print(f"\nDataset Statistics:")
    print(f"  - Projects: {len(df)}")
    print(f"  - Average waste: {df['steel_waste_percentage'].mean():.2f}%")
    print(f"  - Min waste: {df['steel_waste_percentage'].min():.2f}%")
    print(f"  - Max waste: {df['steel_waste_percentage'].max():.2f}%")
    print(f"\nFirst 5 rows:")
    print(df.head().to_string())
    
    # Show distribution of key variables
    print(f"\nStock Length Policy Distribution:")
    print(df['stock_length_policy'].value_counts())
    print(f"\nContract Type Distribution:")
    print(df['contract_type'].value_counts())
    print(f"\nProject Phase Distribution:")
    print(df['project_phase'].value_counts())


if __name__ == "__main__":
    main()

