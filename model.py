"""
Professional Model Comparison System
Tests 10 different machine learning models with comprehensive evaluation
Includes cross-validation, multiple metrics, feature importance, and detailed reporting
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import (
    cross_val_score, 
    KFold, 
    cross_validate,
    learning_curve
)
from sklearn.metrics import (
    mean_absolute_error, 
    mean_squared_error, 
    r2_score,
    make_scorer
)
from sklearn.neighbors import NearestNeighbors
import joblib
import os
import time
import warnings
from datetime import datetime
from typing import Dict, List, Tuple, Optional
warnings.filterwarnings('ignore')

# Try to import SHAP, but make it optional
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("Warning: SHAP not available. Install with 'pip install shap' for explainability features.")

# Import 10 different models
from sklearn.ensemble import (
    RandomForestRegressor, 
    GradientBoostingRegressor, 
    AdaBoostRegressor,
    ExtraTreesRegressor
)
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor


class ModelComparison:
    """
    Professional model comparison system with comprehensive evaluation.
    
    Features:
    - 10 different ML models
    - K-Fold cross-validation (default: 10 folds)
    - Multiple evaluation metrics (MAE, RMSE, R², MAPE)
    - Feature importance analysis
    - Overfitting detection
    - Training time tracking
    - Detailed reporting
    """
    
    def __init__(self, cv_folds: int = 10, random_state: int = 42):
        """
        Initialize the model comparison system.
        
        This constructor sets up all necessary components for model training,
        evaluation, and prediction. It initializes data preprocessing tools,
        cross-validation strategy, and storage for model results.
        
        Args:
            cv_folds: Number of folds for cross-validation (default: 10)
                - Higher folds = more robust evaluation but slower
                - 10-fold CV is standard practice in ML
            random_state: Random seed for reproducibility (default: 42)
                - Ensures consistent results across runs
                - Critical for scientific reproducibility
        """
        # Cross-validation configuration
        self.cv_folds = cv_folds  # Number of CV folds
        self.random_state = random_state  # Random seed for reproducibility
        
        # Data preprocessing components
        self.label_encoders = {}  # Dictionary to store LabelEncoders for categorical variables
                                  # Format: {'column_name': LabelEncoder()}
        self.scaler = StandardScaler()  # StandardScaler for feature normalization
                                       # Converts features to mean=0, std=1
        self.feature_columns = None  # List of feature column names (set during training)
        
        # Model storage
        self.best_model = None  # The trained best-performing model object
        self.best_model_name = None  # Name of the best model (e.g., 'Gradient Boosting')
        self.results = []  # List to store evaluation results for all models
        
        # Cross-validation strategy
        # KFold splits data into k folds, shuffles, and uses each fold as test set once
        self.cv = KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        
        # Additional features for advanced functionality
        self.X_train_scaled = None  # Store scaled training data for reliability calculation
                                    # Used to compare new predictions with training data
        self.shap_explainer = None  # SHAP explainer for model explainability
                                    # Initialized after best model is selected
        
    def prepare_features(self, df: pd.DataFrame, is_training: bool = True) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Prepare features for machine learning by encoding and scaling.
        
        This method performs critical data preprocessing steps:
        1. Encodes categorical variables to numerical values
        2. Selects feature columns (excludes ID and target)
        3. Scales/normalizes numerical features
        4. Extracts target variable if present
        
        Args:
            df: Input DataFrame with project data
            is_training: Whether this is training data
                - True: Fit encoders/scalers (learn from data)
                - False: Use pre-fitted encoders/scalers (transform only)
        
        Returns:
            Tuple containing:
            - X: numpy array of features (shape: [n_samples, n_features])
            - y: numpy array of target values (shape: [n_samples]) or None if no target
        
        Raises:
            ValueError: If label encoders not found during prediction (model not trained)
        """
        # Create copy to avoid modifying original DataFrame
        df = df.copy()
        
        # ====================================================================
        # STEP 1: ENCODE CATEGORICAL VARIABLES
        # ====================================================================
        # Convert text categories (e.g., 'standard_12m', 'lump_sum') to numbers
        # This is required because ML models only work with numerical data
        categorical_cols = ['stock_length_policy', 'contract_type', 'project_phase']
        
        for col in categorical_cols:
            if is_training:
                # Training: Create and fit new encoder
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
                # fit_transform: Learns mapping (e.g., 'standard_12m' -> 0) and applies it
            else:
                # Prediction: Use existing encoder (must be trained first)
                if col not in self.label_encoders:
                    raise ValueError(
                        f"Label encoder for {col} not found. Train model first."
                    )
                df[col] = self.label_encoders[col].transform(df[col])
                # transform: Applies learned mapping to new data
        
        # ====================================================================
        # STEP 2: SELECT FEATURE COLUMNS
        # ====================================================================
        # Identify which columns are features (exclude ID and target)
        exclude_cols = ['project_id', 'steel_waste_percentage']
        
        # Store feature column names on first call (during training)
        if self.feature_columns is None:
            self.feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        # Extract feature matrix X (all columns except excluded ones)
        X = df[self.feature_columns].values  # Convert to numpy array
        
        # Extract target variable y (if present in DataFrame)
        y = df['steel_waste_percentage'].values if 'steel_waste_percentage' in df.columns else None
        
        # ====================================================================
        # STEP 3: SCALE/NORMALIZE FEATURES
        # ====================================================================
        # Standardization: Convert features to mean=0, std=1
        # This is critical because features have different scales:
        #   - reinforcement_ratio: ~100-200
        #   - bim_integration_level: 0-3
        # Without scaling, large values dominate the model
        if is_training:
            # Training: Fit scaler (learn mean and std) and transform
            X = self.scaler.fit_transform(X)
        else:
            # Prediction: Use pre-fitted scaler (apply same transformation)
            X = self.scaler.transform(X)
        
        return X, y
    
    def get_models(self) -> Dict[str, object]:
        """Define 10 different models to compare."""
        models = {
            'Random Forest': RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                n_jobs=-1,
                verbose=0
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                min_samples_split=5,
                random_state=self.random_state,
                verbose=0
            ),
            'XGBoost': XGBRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                min_child_weight=1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=self.random_state,
                n_jobs=-1,
                verbosity=0
            ),
            'Extra Trees': ExtraTreesRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                n_jobs=-1,
                verbose=0
            ),
            'AdaBoost': AdaBoostRegressor(
                n_estimators=100,
                learning_rate=0.1,
                random_state=self.random_state
            ),
            'Decision Tree': DecisionTreeRegressor(
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state
            ),
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0, random_state=self.random_state),
            'Lasso Regression': Lasso(alpha=0.1, random_state=self.random_state, max_iter=2000),
            'Elastic Net': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=self.random_state, max_iter=2000)
        }
        return models
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
        
        Returns:
            Dictionary of metrics
        """
        # Avoid division by zero in MAPE
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100 if np.any(mask) else np.inf
        
        return {
            'mae': mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred),
            'mape': mape,
            'mean_error': np.mean(y_true - y_pred),
            'std_error': np.std(y_true - y_pred)
        }
    
    def evaluate_model(self, model, X_train: np.ndarray, y_train: np.ndarray, 
                      X_test: np.ndarray, y_test: np.ndarray, model_name: str) -> Dict:
        """
        Comprehensive model evaluation with cross-validation and multiple metrics.
        
        Args:
            model: Model to evaluate
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            model_name: Name of the model
        
        Returns:
            Dictionary with all evaluation metrics
        """
        start_time = time.time()
        
        # Train model
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Calculate metrics
        train_metrics = self.calculate_metrics(y_train, y_train_pred)
        test_metrics = self.calculate_metrics(y_test, y_test_pred)
        
        # Cross-validation with multiple metrics
        cv_scoring = {
            'mae': 'neg_mean_absolute_error',
            'rmse': 'neg_root_mean_squared_error',
            'r2': 'r2'
        }
        
        cv_results = cross_validate(
            model, X_train, y_train,
            cv=self.cv,
            scoring=cv_scoring,
            n_jobs=-1,
            return_train_score=True
        )
        
        # Calculate CV statistics
        cv_mae_mean = -cv_results['test_mae'].mean()
        cv_mae_std = cv_results['test_mae'].std()
        cv_rmse_mean = -cv_results['test_rmse'].mean()
        cv_rmse_std = cv_results['test_rmse'].std()
        cv_r2_mean = cv_results['test_r2'].mean()
        cv_r2_std = cv_results['test_r2'].std()
        
        # Overfitting detection (difference between train and test R²)
        overfitting_score = train_metrics['r2'] - test_metrics['r2']
        
        # Feature importance (if available)
        feature_importance = None
        if hasattr(model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_columns, model.feature_importances_))
        elif hasattr(model, 'coef_'):
            # For linear models, use absolute coefficients
            feature_importance = dict(zip(self.feature_columns, np.abs(model.coef_)))
        
        return {
            'model_name': model_name,
            'model': model,
            'training_time': training_time,
            # Train metrics
            'train_mae': train_metrics['mae'],
            'train_rmse': train_metrics['rmse'],
            'train_r2': train_metrics['r2'],
            'train_mape': train_metrics['mape'],
            # Test metrics
            'test_mae': test_metrics['mae'],
            'test_rmse': test_metrics['rmse'],
            'test_r2': test_metrics['r2'],
            'test_mape': test_metrics['mape'],
            # Cross-validation metrics
            'cv_mae_mean': cv_mae_mean,
            'cv_mae_std': cv_mae_std,
            'cv_rmse_mean': cv_rmse_mean,
            'cv_rmse_std': cv_rmse_std,
            'cv_r2_mean': cv_r2_mean,
            'cv_r2_std': cv_r2_std,
            # Additional metrics
            'overfitting_score': overfitting_score,
            'feature_importance': feature_importance
        }
    
    def compare_models(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare all models and select the best one.
        
        Args:
            train_df: Training dataset
            test_df: Test dataset
        
        Returns:
            DataFrame with comparison results
        """
        print("=" * 80)
        print("PROFESSIONAL MODEL COMPARISON SYSTEM")
        print("=" * 80)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Cross-Validation: {self.cv_folds}-Fold K-Fold")
        print("=" * 80)
        
        # Prepare data
        print("\n[1/4] Preparing data...")
        X_train, y_train = self.prepare_features(train_df, is_training=True)
        X_test, y_test = self.prepare_features(test_df, is_training=False)
        
        # Store scaled training data for reliability calculation
        self.X_train_scaled = X_train.copy()
        
        print(f"  ✓ Training set: {X_train.shape[0]:,} samples, {X_train.shape[1]} features")
        print(f"  ✓ Test set: {X_test.shape[0]:,} samples, {X_test.shape[1]} features")
        print(f"  ✓ Target range: {y_train.min():.2f}% - {y_train.max():.2f}%")
        print(f"  ✓ Target mean: {y_train.mean():.2f}% ± {y_train.std():.2f}%")
        
        # Get models
        models = self.get_models()
        
        print(f"\n[2/4] Testing {len(models)} models with {self.cv_folds}-fold cross-validation...")
        print("-" * 80)
        
        # Evaluate each model
        total_start = time.time()
        for i, (name, model) in enumerate(models.items(), 1):
            print(f"\n[{i}/{len(models)}] {name}")
            print("  " + "-" * 76)
            
            try:
                result = self.evaluate_model(model, X_train, y_train, X_test, y_test, name)
                self.results.append(result)
                
                print(f"  Training Time: {result['training_time']:.2f}s")
                print(f"  Test MAE:  {result['test_mae']:.4f}%")
                print(f"  Test RMSE: {result['test_rmse']:.4f}%")
                print(f"  Test R²:  {result['test_r2']:.4f}")
                print(f"  Test MAPE: {result['test_mape']:.2f}%")
                print(f"  CV MAE:   {result['cv_mae_mean']:.4f}% (±{result['cv_mae_std']:.4f})")
                print(f"  CV R²:    {result['cv_r2_mean']:.4f} (±{result['cv_r2_std']:.4f})")
                print(f"  Overfitting: {result['overfitting_score']:.4f} (lower is better)")
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                continue
        
        total_time = time.time() - total_start
        print(f"\n  Total evaluation time: {total_time:.2f}s")
        
        # Create comprehensive results DataFrame
        print(f"\n[3/4] Generating comparison report...")
        results_data = []
        for r in self.results:
            results_data.append({
                'Model': r['model_name'],
                'Test MAE (%)': f"{r['test_mae']:.4f}",
                'Test RMSE (%)': f"{r['test_rmse']:.4f}",
                'Test R²': f"{r['test_r2']:.4f}",
                'Test MAPE (%)': f"{r['test_mape']:.2f}",
                'CV MAE (%)': f"{r['cv_mae_mean']:.4f}",
                'CV MAE Std': f"{r['cv_mae_std']:.4f}",
                'CV R²': f"{r['cv_r2_mean']:.4f}",
                'CV R² Std': f"{r['cv_r2_std']:.4f}",
                'Overfitting': f"{r['overfitting_score']:.4f}",
                'Train Time (s)': f"{r['training_time']:.2f}"
            })
        
        results_df = pd.DataFrame(results_data)
        
        # Sort by test MAE (lower is better)
        results_df['Test MAE (num)'] = [r['test_mae'] for r in self.results]
        results_df = results_df.sort_values('Test MAE (num)').drop('Test MAE (num)', axis=1)
        
        print("\n" + "=" * 80)
        print("COMPREHENSIVE MODEL COMPARISON RESULTS")
        print("=" * 80)
        print(results_df.to_string(index=False))
        
        # Select best model (lowest test MAE)
        if self.results:
            best_result = min(self.results, key=lambda x: x['test_mae'])
            self.best_model = best_result['model']
            self.best_model_name = best_result['model_name']
            
            # Initialize SHAP explainer if available
            if SHAP_AVAILABLE:
                try:
                    print("\n[4.5/4] Initializing SHAP explainer...")
                    # Use a sample of training data for SHAP (faster)
                    sample_size = min(100, len(X_train))
                    sample_indices = np.random.choice(len(X_train), sample_size, replace=False)
                    X_train_sample = X_train[sample_indices]
                    
                    # Create explainer based on model type
                    if 'Gradient Boosting' in self.best_model_name or 'XGBoost' in self.best_model_name:
                        self.shap_explainer = shap.TreeExplainer(self.best_model)
                    else:
                        self.shap_explainer = shap.KernelExplainer(
                            self.best_model.predict, 
                            X_train_sample
                        )
                    print("  ✓ SHAP explainer initialized")
                except Exception as e:
                    print(f"  ⚠ SHAP initialization failed: {e}")
                    self.shap_explainer = None
            
            print("\n" + "=" * 80)
            print(f"🏆 BEST MODEL: {self.best_model_name}")
            print("=" * 80)
            print(f"  Test MAE:        {best_result['test_mae']:.4f}%")
            print(f"  Test RMSE:       {best_result['test_rmse']:.4f}%")
            print(f"  Test R²:         {best_result['test_r2']:.4f}")
            print(f"  Test MAPE:       {best_result['test_mape']:.2f}%")
            print(f"  CV MAE:          {best_result['cv_mae_mean']:.4f}% (±{best_result['cv_mae_std']:.4f})")
            print(f"  CV RMSE:         {best_result['cv_rmse_mean']:.4f}% (±{best_result['cv_rmse_std']:.4f})")
            print(f"  CV R²:           {best_result['cv_r2_mean']:.4f} (±{best_result['cv_r2_std']:.4f})")
            print(f"  Overfitting:     {best_result['overfitting_score']:.4f}")
            print(f"  Training Time:   {best_result['training_time']:.2f}s")
            print("=" * 80)
        
        return results_df
    
    def get_feature_importance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get feature importance from the best model.
        
        Args:
            top_n: Number of top features to return
        
        Returns:
            DataFrame with feature importance
        """
        if self.best_model is None:
            raise ValueError("No model has been trained yet. Call compare_models() first.")
        
        best_result = next(r for r in self.results if r['model_name'] == self.best_model_name)
        
        if best_result['feature_importance'] is None:
            return pd.DataFrame({'Feature': [], 'Importance': []})
        
        importance_df = pd.DataFrame({
            'Feature': list(best_result['feature_importance'].keys()),
            'Importance': list(best_result['feature_importance'].values())
        }).sort_values('Importance', ascending=False).head(top_n)
        
        return importance_df
    
    def save_best_model(self, filepath: str = 'models/best_steel_waste_model.pkl'):
        """
        Save the best model with metadata.
        
        Args:
            filepath: Path to save the model
        """
        if self.best_model is None:
            raise ValueError("No model has been trained yet. Call compare_models() first.")
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        best_result = next(r for r in self.results if r['model_name'] == self.best_model_name)
        
        model_data = {
            'model': self.best_model,
            'model_name': self.best_model_name,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'X_train_scaled': self.X_train_scaled,  # Store for reliability calculation
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'cv_folds': self.cv_folds,
                'test_mae': best_result['test_mae'],
                'test_rmse': best_result['test_rmse'],
                'test_r2': best_result['test_r2'],
                'cv_mae_mean': best_result['cv_mae_mean'],
                'cv_mae_std': best_result['cv_mae_std'],
                'feature_importance': best_result['feature_importance']
            }
        }
        
        # Note: SHAP explainer is not saved (too large), will be recreated on load if needed
        
        joblib.dump(model_data, filepath)
        print(f"\n✓ Best model saved to: {filepath}")
        print(f"  Model: {self.best_model_name}")
        print(f"  Test MAE: {best_result['test_mae']:.4f}%")
        print(f"  Test R²: {best_result['test_r2']:.4f}")
    
    def load_model(self, filepath: str):
        """
        Load a saved model.
        
        Args:
            filepath: Path to the saved model
        """
        model_data = joblib.load(filepath)
        self.best_model = model_data['model']
        self.best_model_name = model_data['model_name']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        
        # Load training data for reliability calculation
        if 'X_train_scaled' in model_data:
            self.X_train_scaled = model_data['X_train_scaled']
        else:
            # Try to load from training data file
            try:
                train_df = pd.read_csv('data/train_data.csv')
                X_train, _ = self.prepare_features(train_df, is_training=False)
                self.X_train_scaled = X_train
            except:
                print("  ⚠ Training data not available. Reliability calculation may be limited.")
                self.X_train_scaled = None
        
        # Initialize SHAP explainer if available
        if SHAP_AVAILABLE and self.X_train_scaled is not None:
            try:
                sample_size = min(100, len(self.X_train_scaled))
                sample_indices = np.random.choice(len(self.X_train_scaled), sample_size, replace=False)
                X_train_sample = self.X_train_scaled[sample_indices]
                
                if 'Gradient Boosting' in self.best_model_name or 'XGBoost' in self.best_model_name:
                    self.shap_explainer = shap.TreeExplainer(self.best_model)
                else:
                    self.shap_explainer = shap.KernelExplainer(
                        self.best_model.predict, 
                        X_train_sample
                    )
            except Exception as e:
                print(f"  ⚠ SHAP explainer initialization failed: {e}")
                self.shap_explainer = None
        
        if 'metadata' in model_data:
            metadata = model_data['metadata']
            print(f"✓ Model loaded from: {filepath}")
            print(f"  Model: {self.best_model_name}")
            print(f"  Created: {metadata.get('created_at', 'Unknown')}")
            print(f"  Test MAE: {metadata.get('test_mae', 'Unknown'):.4f}%")
            print(f"  Test R²: {metadata.get('test_r2', 'Unknown'):.4f}")
        else:
            print(f"✓ Model loaded from: {filepath}")
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using the best model.
        
        Args:
            df: DataFrame with features
        
        Returns:
            Array of predictions
        """
        if self.best_model is None:
            raise ValueError("No model loaded. Load a model first.")
        
        X, _ = self.prepare_features(df, is_training=False)
        return self.best_model.predict(X)
    
    def explain_prediction(self, df: pd.DataFrame, top_n: int = 5) -> Dict:
        """
        Explain a prediction using SHAP values or feature importance.
        
        Model explainability is crucial for:
        - Understanding which factors drive waste predictions
        - Building trust with engineers and stakeholders
        - Identifying actionable insights for waste reduction
        
        This method attempts to use SHAP (SHapley Additive exPlanations) first,
        which provides the most accurate feature contributions. If SHAP is
        unavailable, it falls back to feature importance.
        
        Args:
            df: DataFrame with features for prediction (single or multiple rows)
            top_n: Number of top features to return (default: 5)
        
        Returns:
            Dictionary containing:
            - 'method': 'SHAP', 'Feature Importance', or 'Not Available'
            - 'top_features': List of top N features with contributions
            - 'all_features': Dictionary of all features and their contributions
        
        Raises:
            ValueError: If no model is loaded
        """
        # Validate that model is loaded
        if self.best_model is None:
            raise ValueError("No model loaded. Load a model first.")
        
        # Prepare features (encode, scale) for prediction
        X, _ = self.prepare_features(df, is_training=False)
        
        # ====================================================================
        # ATTEMPT SHAP EXPLANATION (MOST ACCURATE)
        # ====================================================================
        # SHAP provides exact feature contributions to each prediction
        # It's based on game theory and shows how each feature changes the output
        if SHAP_AVAILABLE and self.shap_explainer is not None:
            try:
                shap_values = self.shap_explainer(X)
                # Handle different SHAP return types
                if hasattr(shap_values, 'values'):
                    # SHAP Explanation object
                    contrib_values = shap_values.values[0]
                elif isinstance(shap_values, np.ndarray):
                    # Direct numpy array
                    contrib_values = shap_values[0] if len(shap_values.shape) > 1 else shap_values
                elif isinstance(shap_values, list):
                    contrib_values = shap_values[0] if len(shap_values) > 0 else np.zeros(len(self.feature_columns))
                else:
                    contrib_values = shap_values[0]
                
                # Create feature contribution dictionary (use actual values, not absolute)
                contributions = dict(zip(self.feature_columns, contrib_values))
                # Sort by absolute contribution for top features
                sorted_contributions = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
                
                # SHAP interpretation: positive = increases waste, negative = decreases waste
                # This is straightforward - SHAP shows direct contribution to prediction
                top_features_list = []
                for feat, contrib in sorted_contributions[:top_n]:
                    top_features_list.append({
                        'feature': feat,
                        'contribution': float(contrib),
                        'impact': 'positive' if contrib > 0 else 'negative'
                    })
                
                return {
                    'method': 'SHAP',
                    'top_features': top_features_list,
                    'all_features': {feat: float(contrib) for feat, contrib in contributions.items()}
                }
            except Exception as e:
                print(f"SHAP explanation failed: {e}. Falling back to feature importance.")
        
        # Fallback to feature importance
        if hasattr(self.best_model, 'feature_importances_'):
            importances = dict(zip(self.feature_columns, self.best_model.feature_importances_))
            sorted_importances = sorted(importances.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'method': 'Feature Importance',
                'top_features': [
                    {'feature': feat, 'importance': float(imp), 'impact': 'positive'}
                    for feat, imp in sorted_importances[:top_n]
                ],
                'all_features': {feat: float(imp) for feat, imp in importances.items()}
            }
        
        return {
            'method': 'Not Available',
            'top_features': [],
            'all_features': {}
        }
    
    def calculate_reliability(self, df: pd.DataFrame) -> Dict:
        """
        Calculate prediction reliability based on similarity to training data.
        
        Reliability indicates how confident we can be in a prediction. If the input
        data is very different from the training data, the model may not be reliable.
        This uses k-Nearest Neighbors (k-NN) to measure similarity.
        
        The reliability score combines two metrics:
        1. Euclidean distance to nearest training samples
        2. Feature-wise normalized distance (z-scores)
        
        Args:
            df: DataFrame with features for prediction
        
        Returns:
            Dictionary containing:
            - 'reliability_score': Float between 0-1 (higher = more reliable)
            - 'reliability_level': 'high', 'medium', or 'low'
            - 'message': Human-readable explanation
            - 'mean_distance': Average distance to nearest neighbors
            - 'normalized_distance': Normalized feature distance
        
        Raises:
            ValueError: If no model is loaded
        """
        # Validate model is loaded
        if self.best_model is None:
            raise ValueError("No model loaded. Load a model first.")
        
        # Check if training data is available (required for similarity calculation)
        if self.X_train_scaled is None:
            return {
                'reliability_score': 0.5,
                'reliability_level': 'medium',
                'message': 'Training data not available for reliability calculation'
            }
        
        # Prepare input features (same preprocessing as training)
        X, _ = self.prepare_features(df, is_training=False)
        
        # ====================================================================
        # METRIC 1: EUCLIDEAN DISTANCE TO NEAREST NEIGHBORS
        # ====================================================================
        # Use k-NN to find the k closest training samples
        # If input is close to training data, prediction is more reliable
        n_neighbors = min(10, len(self.X_train_scaled))  # Use up to 10 neighbors
        nn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
        nn.fit(self.X_train_scaled)  # Fit on training data
        
        # Find distances to nearest neighbors
        distances, _ = nn.kneighbors(X)  # Returns distances and indices
        mean_distance = np.mean(distances[0])  # Average distance to k nearest neighbors
        
        # ====================================================================
        # METRIC 2: FEATURE-WISE NORMALIZED DISTANCE
        # ====================================================================
        # Measure how many standard deviations each feature is from training mean
        # This accounts for different feature scales
        feature_distances = np.abs(X[0] - np.mean(self.X_train_scaled, axis=0))
        feature_stds = np.std(self.X_train_scaled, axis=0)
        
        # Normalize by standard deviation (z-score)
        # Values > 2 std devs indicate significant deviation
        normalized_distances = feature_distances / (feature_stds + 1e-10)  # +1e-10 prevents division by zero
        mean_normalized_distance = np.mean(normalized_distances)
        
        # ====================================================================
        # COMBINE METRICS INTO RELIABILITY SCORE
        # ====================================================================
        # Use percentile-based approach to normalize distance score
        # Calculate 95th percentile of distances in training data (expected maximum)
        max_expected_distance = np.percentile(
            [np.mean(nn.kneighbors([sample])[0][0]) 
             for sample in self.X_train_scaled[:100]],  # Sample 100 points for speed
            95
        )
        
        # Normalize distance score (0-1 scale, higher = closer = more reliable)
        if max_expected_distance > 0:
            distance_score = 1 - min(mean_distance / max_expected_distance, 1.0)
        else:
            distance_score = 0.5  # Default if calculation fails
        
        # Normalized distance score (lower normalized distance = higher reliability)
        # 2 standard deviations = threshold for low reliability
        normalized_score = 1 - min(mean_normalized_distance / 2.0, 1.0)
        
        # Combine both scores using weighted average
        # Weight distance more (60%) as it's more direct measure of similarity
        reliability_score = 0.6 * distance_score + 0.4 * normalized_score
        
        # ====================================================================
        # DETERMINE RELIABILITY LEVEL
        # ====================================================================
        # Convert numerical score to qualitative level
        if reliability_score >= 0.7:
            level = 'high'
            message = 'Input data is very similar to training data. High confidence in prediction.'
        elif reliability_score >= 0.4:
            level = 'medium'
            message = 'Input data is somewhat similar to training data. Moderate confidence in prediction.'
        else:
            level = 'low'
            message = 'Input data differs significantly from training data. Lower confidence in prediction.'
        
        return {
            'reliability_score': float(reliability_score),
            'reliability_level': level,
            'message': message,
            'mean_distance': float(mean_distance),
            'normalized_distance': float(mean_normalized_distance)
        }
    
    def calculate_cost_co2_impact(self, waste_percentage: float, 
                                   total_steel_kg: float = 100000,
                                   steel_cost_per_kg: float = 0.8,
                                   co2_per_kg_steel: float = 2.5) -> Dict:
        """
        Calculate financial and environmental impact of steel waste.
        
        This method quantifies the real-world implications of predicted waste:
        - Financial cost of wasted steel
        - CO₂ emissions from wasted steel production
        - Potential savings from waste reduction
        
        These metrics help stakeholders understand the business case for
        waste reduction and make data-driven decisions.
        
        Args:
            waste_percentage: Predicted waste percentage (e.g., 6.5 for 6.5%)
            total_steel_kg: Total steel quantity in kg (default: 100,000 kg = 100 tons)
            steel_cost_per_kg: Cost per kg of steel in USD (default: $0.8/kg)
                - Based on Middle East market rates (2024-2025)
            co2_per_kg_steel: CO₂ emissions per kg of steel in kg CO₂ (default: 2.5 kg CO₂/kg)
                - Based on industry average for rebar production
                - Includes production, transportation, and processing
        
        Returns:
            Dictionary containing:
            - 'waste_percentage': Original predicted waste percentage
            - 'total_steel_kg': Total steel quantity
            - 'waste_kg': Amount of steel wasted (in kg)
            - 'waste_cost_usd': Financial cost of waste (in USD)
            - 'waste_co2_kg': CO₂ emissions from waste (in kg CO₂)
            - 'potential_savings_kg': Potential steel savings (in kg)
            - 'potential_cost_savings_usd': Potential cost savings (in USD)
            - 'potential_co2_reduction_kg': Potential CO₂ reduction (in kg CO₂)
            - 'target_waste_percentage': Target waste percentage (50% reduction)
        """
        # ====================================================================
        # CALCULATE ACTUAL WASTE QUANTITIES
        # ====================================================================
        # Convert percentage to absolute quantity
        waste_kg = (waste_percentage / 100) * total_steel_kg
        
        # Calculate financial cost of waste
        # Example: 6.5% of 100,000 kg = 6,500 kg × $0.8/kg = $5,200
        waste_cost = waste_kg * steel_cost_per_kg
        
        # Calculate CO₂ emissions from waste
        # Steel production is carbon-intensive
        # Example: 6,500 kg × 2.5 kg CO₂/kg = 16,250 kg CO₂
        waste_co2 = waste_kg * co2_per_kg_steel
        
        # ====================================================================
        # CALCULATE POTENTIAL SAVINGS
        # ====================================================================
        # Assume 50% waste reduction is achievable with optimization
        # This is a conservative estimate based on industry best practices
        target_waste_percentage = waste_percentage * 0.5
        
        # Calculate potential savings in steel quantity
        potential_savings_kg = (waste_percentage - target_waste_percentage) / 100 * total_steel_kg
        
        # Calculate potential cost savings
        potential_cost_savings = potential_savings_kg * steel_cost_per_kg
        
        # Calculate potential CO₂ reduction
        # Reducing waste directly reduces carbon footprint
        potential_co2_reduction = potential_savings_kg * co2_per_kg_steel
        
        return {
            'waste_percentage': float(waste_percentage),
            'total_steel_kg': float(total_steel_kg),
            'waste_kg': float(waste_kg),
            'waste_cost_usd': float(waste_cost),
            'waste_co2_kg': float(waste_co2),
            'potential_savings_kg': float(potential_savings_kg),
            'potential_cost_savings_usd': float(potential_cost_savings),
            'potential_co2_reduction_kg': float(potential_co2_reduction),
            'target_waste_percentage': float(target_waste_percentage)
        }


def main():
    """Main function to compare models."""
    print("\n" + "=" * 80)
    print("STEEL WASTE PREDICTION - MODEL COMPARISON")
    print("=" * 80)
    
    # Load train and test data from data folder
    print("\n[0/4] Loading datasets...")
    try:
        train_df = pd.read_csv('data/train_data.csv')
        test_df = pd.read_csv('data/test_data.csv')
        print(f"  ✓ Loaded {len(train_df):,} training samples")
        print(f"  ✓ Loaded {len(test_df):,} test samples")
    except FileNotFoundError as e:
        print(f"  ✗ Error: {e}")
        print("  Please run 'data_generation/generate_train_test_data.py' first to create the datasets.")
        return
    
    # Create model comparison with 10-fold CV
    comparator = ModelComparison(cv_folds=10, random_state=42)
    
    # Compare models
    results_df = comparator.compare_models(train_df, test_df)
    
    # Get feature importance
    print(f"\n[4/4] Feature Importance Analysis (Top 10)...")
    try:
        importance_df = comparator.get_feature_importance(top_n=10)
        if not importance_df.empty:
            print("\n" + "-" * 80)
            print(importance_df.to_string(index=False))
            print("-" * 80)
    except Exception as e:
        print(f"  Feature importance not available: {e}")
    
    # Save best model
    comparator.save_best_model('models/best_steel_waste_model.pkl')
    
    # Save results to data folder
    os.makedirs('data', exist_ok=True)
    results_df.to_csv('data/model_comparison_results.csv', index=False)
    print(f"\n✓ Model comparison results saved to: data/model_comparison_results.csv")
    
    # Test prediction on sample test data
    print("\n" + "=" * 80)
    print("PREDICTION VALIDATION - Sample Test Data")
    print("=" * 80)
    sample_test = test_df.head(20).copy()
    predictions = comparator.predict(sample_test)
    
    comparison = pd.DataFrame({
        'Project ID': sample_test['project_id'],
        'Actual Waste (%)': sample_test['steel_waste_percentage'].round(2),
        'Predicted Waste (%)': predictions.round(2),
        'Error (%)': (sample_test['steel_waste_percentage'] - predictions).round(2),
        'Abs Error (%)': (sample_test['steel_waste_percentage'] - predictions).abs().round(2)
    })
    
    print("\nFirst 20 test samples:")
    print(comparison.to_string(index=False))
    
    print(f"\nSummary Statistics:")
    print(f"  Mean Absolute Error: {comparison['Abs Error (%)'].mean():.4f}%")
    print(f"  Max Error: {comparison['Abs Error (%)'].max():.4f}%")
    print(f"  Min Error: {comparison['Abs Error (%)'].min():.4f}%")
    print(f"  Std Error: {comparison['Error (%)'].std():.4f}%")
    
    print("\n" + "=" * 80)
    print("✓ Model comparison complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
