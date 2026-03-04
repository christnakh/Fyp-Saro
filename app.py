"""
Flask Web Application for Steel Waste Prediction
================================================
Professional website with templates and static files for predicting steel waste
in construction projects using machine learning.

This application provides:
- Web interface for inputting project parameters
- Real-time steel waste predictions
- Model explainability (SHAP/Feature Importance)
- Prediction reliability indicators
- Cost and CO2 impact calculations

Author: FYP Team G09
Date: 2026
"""

# ============================================================================
# IMPORTS
# ============================================================================
from flask import Flask, request, jsonify, render_template  # Flask web framework components
import pandas as pd  # Data manipulation and DataFrame operations
import numpy as np  # Numerical operations and random number generation
import os  # File system operations
from model import ModelComparison  # Custom ML model comparison class
import warnings  # Suppress warnings for cleaner output
warnings.filterwarnings('ignore')  # Ignore all warnings (e.g., deprecation warnings)

# ============================================================================
# FLASK APPLICATION INITIALIZATION
# ============================================================================
# Create Flask application instance
app = Flask(__name__)

# Configure Flask to not cache static files (useful during development)
# This ensures changes to CSS/JS are immediately visible
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# ============================================================================
# GLOBAL VARIABLES
# ============================================================================
# Global model loader - stores the loaded ML model to avoid reloading on every request
# This improves performance by loading the model once and reusing it
model_comparator = None

def load_model():
    """
    Load the trained machine learning model.
    
    This function implements a singleton pattern to ensure the model is only loaded once.
    Subsequent calls will return the cached model, improving performance.
    
    Returns:
        ModelComparison: The loaded model comparator object with trained model
        
    Raises:
        FileNotFoundError: If the model file doesn't exist at the expected path
    """
    global model_comparator  # Access global variable
    
    # Only load model if it hasn't been loaded yet (singleton pattern)
    if model_comparator is None:
        # Define path to saved model file
        model_path = 'models/best_steel_waste_model.pkl'
        
        # Check if model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. Please train the model first."
            )
        
        # Create ModelComparison instance and load the saved model
        model_comparator = ModelComparison()
        model_comparator.load_model(model_path)  # Load model, scalers, encoders, etc.
    
    return model_comparator  # Return the loaded model

def get_waste_category(waste_percentage):
    """
    Categorize waste percentage into qualitative categories.
    
    This function converts numerical waste percentages into human-readable
    categories with corresponding Bootstrap color classes for UI display.
    
    Categories based on industry standards:
    - Excellent: < 3% (best practice, minimal waste)
    - Good: 3-5% (acceptable, industry average)
    - Average: 5-8% (moderate waste, room for improvement)
    - Poor: 8-12% (high waste, needs attention)
    - Very Poor: > 12% (excessive waste, critical issue)
    
    Args:
        waste_percentage (float): The predicted waste percentage value
        
    Returns:
        tuple: (category_name, bootstrap_color_class)
            - category_name (str): Human-readable category name
            - bootstrap_color_class (str): Bootstrap CSS class for styling
    """
    # Excellent performance - minimal waste
    if waste_percentage < 3:
        return "Excellent", "success"  # Green badge
    # Good performance - acceptable waste levels
    elif waste_percentage < 5:
        return "Good", "info"  # Blue badge
    # Average performance - moderate waste
    elif waste_percentage < 8:
        return "Average", "warning"  # Yellow badge
    # Poor performance - high waste
    elif waste_percentage < 12:
        return "Poor", "warning"  # Yellow badge
    # Very poor performance - excessive waste
    else:
        return "Very Poor", "danger"  # Red badge

def format_explainability_features(explanation):
    """
    Format explainability features into HTML for display in the template.
    
    This function takes the raw explainability data (from SHAP or feature importance)
    and converts it into formatted HTML that can be displayed in the web interface.
    It maps technical feature names to human-readable names and determines whether
    each feature increases or decreases waste.
    
    Args:
        explanation (dict): Dictionary containing explainability data with structure:
            - 'top_features': List of dicts with 'feature', 'contribution', 'impact'
            - 'method': 'SHAP' or 'Feature Importance'
        
    Returns:
        str: HTML string containing formatted feature list with Bootstrap styling
    """
    # Map technical feature names to human-readable display names
    # This makes the output more understandable for end users
    feature_name_map = {
        'offcut_reuse_policy_0to2': 'Offcut Reuse Policy',
        'cutting_optimization_usage': 'Cutting Optimization Usage',
        'change_orders_per_month': 'Change Orders Per Month',
        'stock_length_policy': 'Stock Length Policy',
        'design_revisions_per_month': 'Design Revisions Per Month',
        'bim_integration_level': 'BIM Integration Level',
        'supervision_index_1to5': 'Supervision Index',
        'material_control_level_1to3': 'Material Control Level',
        'storage_handling_index_1to5': 'Storage Handling Index',
        'reinforcement_ratio_kg_per_m3': 'Reinforcement Ratio',
        'num_unique_required_lengths': 'Number of Unique Lengths',
        'lead_time_days': 'Lead Time',
        'order_frequency_per_month': 'Order Frequency',
        'contract_type': 'Contract Type',
        'project_phase': 'Project Phase'
    }
    
    # Start building HTML list group (Bootstrap component)
    explainability_html = '<div class="list-group">'
    
    # Iterate through top features (typically top 5 most influential)
    for i, feat in enumerate(explanation['top_features'], 1):
        # Get feature key (technical name) and convert to display name
        feature_key = feat['feature']
        # Use mapped name if available, otherwise format technical name
        feature_name = feature_name_map.get(
            feature_key, 
            feature_key.replace('_', ' ').title()  # Convert snake_case to Title Case
        )
        
        # Extract contribution value (SHAP uses 'contribution', feature importance uses 'importance')
        contribution = feat.get('contribution')
        if contribution is None:
            contribution = feat.get('importance', 0)  # Fallback to importance if no contribution
        
        # Ensure contribution is a valid float
        try:
            contribution = float(contribution)
        except (ValueError, TypeError):
            contribution = 0.0  # Default to 0 if conversion fails
        
        # Determine impact direction and styling
        # Positive contribution = increases waste (bad)
        # Negative contribution = decreases waste (good)
        if contribution > 0:
            impact_text = "Increases waste"
            badge_color = "danger"  # Red badge for negative impact
        elif contribution < 0:
            impact_text = "Decreases waste"
            badge_color = "success"  # Green badge for positive impact
        else:
            impact_text = "Neutral impact"
            badge_color = "secondary"  # Gray badge for neutral
        
        # Build HTML for this feature item
        # Uses Bootstrap list-group-item with flexbox layout
        explainability_html += f'''
        <div class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <strong>{i}. {feature_name}</strong>
                <small class="d-block text-muted">{impact_text}</small>
                    </div>
            <span class="badge bg-{badge_color} rounded-pill">
                {abs(contribution):.4f}
            </span>
        </div>'''
    
    # Close the list group div
    explainability_html += '</div>'
    return explainability_html

# ============================================================================
# FLASK ROUTES - WEB PAGES
# ============================================================================

@app.route('/')
def index():
    """
    Render the landing/home page.
    
    This is the main entry point of the website, displaying:
    - Hero section with project description
    - Key features overview
    - How it works section
    - Call-to-action buttons
    
    Returns:
        str: Rendered HTML template for the landing page
    """
    return render_template('index.html')

@app.route('/predict')
def predict_page():
    """
    Render the prediction form page (GET request).
    
    This route displays the initial prediction form before any submission.
    It provides default/empty values for all form fields and results.
    
    Returns:
        str: Rendered HTML template with empty prediction form
    """
    return render_template('predict.html', 
                         project_id=str(np.random.randint(1000, 9999)),
                         predicted_waste='',
                         category='',
                         category_color='secondary',
                         interpretation='Enter project parameters and click "Predict Steel Waste" to get started.',
                         reliability_level='',
                         reliability_color='secondary',
                         reliability_message='',
                         reliability_score='',
                         waste_cost='$0',
                         waste_co2='0',
                         potential_savings_cost='$0',
                         potential_co2_reduction='0',
                         total_steel_kg='100,000',
                         waste_kg='0',
                         explainability_features='<p class="text-muted">Make a prediction to see feature contributions.</p>',
                         explainability_method='Feature Importance')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction form submission (POST request).
    
    This is the main prediction endpoint that:
    1. Loads the trained ML model
    2. Extracts and validates form data
    3. Makes waste percentage prediction
    4. Calculates explainability (SHAP/Feature Importance)
    5. Calculates prediction reliability
    6. Calculates cost and CO2 impact
    7. Formats results for display
    
    Returns:
        str: Rendered HTML template with prediction results
        
    Note:
        If an error occurs, returns the form with error message displayed
    """
    try:
        # Load the trained model (singleton pattern - cached after first load)
        comparator = load_model()
        
        # ====================================================================
        # EXTRACT FORM DATA
        # ====================================================================
        # Collect all form parameters and convert to appropriate data types
        # Default values are provided for optional fields
        data = {
            'project_id': request.form.get('project_id', 'P' + str(np.random.randint(1000, 9999))),
            'reinforcement_ratio_kg_per_m3': float(request.form.get('reinforcement_ratio', 120)),
            'num_unique_required_lengths': int(request.form.get('num_unique_lengths', 20)),
            'stock_length_policy': request.form.get('stock_length_policy', 'standard_12m'),
            'cutting_optimization_usage': int(request.form.get('cutting_optimization', 0)),
            'bim_integration_level': int(request.form.get('bim_integration', 0)),
            'design_revisions_per_month': int(request.form.get('design_revisions', 2)),
            'supervision_index_1to5': int(request.form.get('supervision_index', 3)),
            'material_control_level_1to3': int(request.form.get('material_control', 2)),
            'storage_handling_index_1to5': int(request.form.get('storage_handling', 3)),
            'offcut_reuse_policy_0to2': int(request.form.get('offcut_reuse', 0)),
            'change_orders_per_month': int(request.form.get('change_orders', 1)),
            'contract_type': request.form.get('contract_type', 'lump_sum'),
            'lead_time_days': int(request.form.get('lead_time', 15)),
            'order_frequency_per_month': int(request.form.get('order_frequency', 4)),
            'project_phase': request.form.get('project_phase', 'frame')  # Default: frame
        }
        
        # ====================================================================
        # MAKE PREDICTION
        # ====================================================================
        # Convert form data to DataFrame (required format for model)
        df = pd.DataFrame([data])
        
        # Get waste percentage prediction (returns array, take first element)
        prediction = comparator.predict(df)[0]
        
        # ====================================================================
        # CALCULATE EXPLAINABILITY
        # ====================================================================
        # Get top 5 most influential features using SHAP or feature importance
        explanation = comparator.explain_prediction(df, top_n=5)
        
        # ====================================================================
        # CALCULATE RELIABILITY
        # ====================================================================
        # Determine how reliable the prediction is based on similarity to training data
        reliability = comparator.calculate_reliability(df)
        
        # ====================================================================
        # CALCULATE COST AND CO2 IMPACT
        # ====================================================================
        # Get total steel quantity from form (default: 100,000 kg)
        total_steel_kg = float(request.form.get('total_steel_kg', 100000))
        
        # Calculate financial and environmental impact
        cost_co2 = comparator.calculate_cost_co2_impact(
            prediction, 
            total_steel_kg=total_steel_kg
        )
        
        # ====================================================================
        # CATEGORIZE WASTE LEVEL
        # ====================================================================
        # Convert numerical prediction to qualitative category
        category, category_color = get_waste_category(prediction)
        
        # ====================================================================
        # PREPARE DISPLAY DATA
        # ====================================================================
        # Human-readable interpretations for each waste category
        interpretations = {
            'Excellent': 'Excellent waste management! This project demonstrates best practices with minimal material waste.',
            'Good': 'Good waste management. The project is performing well with acceptable waste levels.',
            'Average': 'Average waste levels. Consider implementing optimization strategies to improve efficiency.',
            'Poor': 'Poor waste management. Immediate action needed to reduce waste and improve material control.',
            'Very Poor': 'Very poor waste management. Critical review of processes required to address excessive waste.'
        }
        
        # Map reliability levels to Bootstrap badge colors
        reliability_badge_color = {
            'high': 'success',    # Green - high confidence
            'medium': 'warning',  # Yellow - medium confidence
            'low': 'danger'       # Red - low confidence
        }[reliability['reliability_level']]
        
        # ====================================================================
        # RENDER RESULTS TEMPLATE
        # ====================================================================
        # Pass all calculated data to template for display
        return render_template('predict.html',
                             project_id=data['project_id'],
                             predicted_waste=f'{prediction:.2f}',
                             category=category,
                             category_color=category_color,
                             interpretation=interpretations[category],
                             reliability_level=reliability['reliability_level'].upper(),
                             reliability_color=reliability_badge_color,
                             reliability_message=reliability['message'],
                             reliability_score=f"{reliability['reliability_score']:.0%}",
                             waste_cost=f"${cost_co2['waste_cost_usd']:,.0f}",
                             waste_co2=f"{cost_co2['waste_co2_kg']:,.0f}",
                             potential_savings_cost=f"${cost_co2['potential_cost_savings_usd']:,.0f}",
                             potential_co2_reduction=f"{cost_co2['potential_co2_reduction_kg']:,.0f}",
                             total_steel_kg=f"{cost_co2['total_steel_kg']:,.0f}",
                             waste_kg=f"{cost_co2['waste_kg']:,.0f}",
                             explainability_features=format_explainability_features(explanation),
                             explainability_method=explanation['method'],
                             form_data=data)
        
    except Exception as e:
        # ====================================================================
        # ERROR HANDLING
        # ====================================================================
        # If any error occurs during prediction, display error message
        # while keeping the form accessible for retry
        return render_template('predict.html',
                             project_id=str(np.random.randint(1000, 9999)),  # Random project ID
                             predicted_waste='',  # No prediction value
                             category='',
                             category_color='danger',  # Red to indicate error
                             interpretation=f'Error: {str(e)}',  # Error message
                             reliability_level='',
                             reliability_color='secondary',
                             reliability_message='',
                             reliability_score='',
                             waste_cost='$0',
                             waste_co2='0',
                             potential_savings_cost='$0',
                             potential_co2_reduction='0',
                             total_steel_kg='100,000',
                             waste_kg='0',
                             explainability_features=f'<div class="alert alert-danger">Error: {str(e)}</div>',
                             explainability_method='N/A')

@app.route('/about')
def about():
    """
    Render the About page.
    
    Displays information about:
    - The project and its objectives
    - The technology stack used
    - The team and methodology
    
    Returns:
        str: Rendered HTML template for the About page
    """
    return render_template('about.html')

@app.route('/features')
def features():
    """
    Render the Features page.
    
    Displays detailed information about system features:
    - Model explainability
    - Cost and CO2 impact estimation
    - Prediction reliability indicators
    - Web application interface
    
    Returns:
        str: Rendered HTML template for the Features page
    """
    return render_template('features.html')

# ============================================================================
# API ENDPOINTS - JSON RESPONSES
# ============================================================================

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for programmatic predictions (returns JSON).
    
    This endpoint allows external applications to make predictions via API calls.
    It accepts JSON data and returns structured JSON response with all prediction
    details including explainability, reliability, and cost/CO2 impact.
    
    Request Body (JSON):
        {
            "reinforcement_ratio_kg_per_m3": 120.0,
            "num_unique_required_lengths": 20,
            "stock_length_policy": "standard_12m",
            ... (all other project parameters)
            "total_steel_kg": 100000
        }
    
    Returns:
        JSON response with:
        - success: Boolean indicating if prediction was successful
        - predicted_waste_percentage: Predicted waste percentage
        - waste_category: Qualitative category (Excellent/Good/Average/Poor/Very Poor)
        - reliability: Reliability score and level
        - explainability: Top features and their contributions
        - cost_co2_impact: Financial and environmental impact calculations
        
    Status Codes:
        200: Success
        400: Bad Request (invalid data or error occurred)
    """
    try:
        # Load model
        comparator = load_model()
        
        # Get JSON data from request body
        data = request.get_json()
        
        # Convert to DataFrame for model prediction
        df = pd.DataFrame([data])
        
        # Make prediction
        prediction = comparator.predict(df)[0]
        
        # Get category (ignore color for API response)
        category, _ = get_waste_category(prediction)
        
        # Calculate all additional features
        explanation = comparator.explain_prediction(df, top_n=5)
        reliability = comparator.calculate_reliability(df)
        total_steel_kg = float(data.get('total_steel_kg', 100000))
        cost_co2 = comparator.calculate_cost_co2_impact(prediction, total_steel_kg=total_steel_kg)
        
        # Return structured JSON response
        return jsonify({
            'success': True,
            'predicted_waste_percentage': round(prediction, 2),
            'waste_category': category,
            'reliability': reliability,
            'explainability': explanation,
            'cost_co2_impact': cost_co2
        })
    except Exception as e:
        # Return error response
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400  # HTTP 400 Bad Request

@app.route('/debug/explain', methods=['GET'])
def debug_explain():
    """
    Debug endpoint to inspect raw explanation data.
    
    This endpoint is useful for development and debugging. It returns
    the raw explainability data for a sample project, allowing developers
    to inspect the structure and values of SHAP/feature importance outputs.
    
    Returns:
        JSON response with raw explanation data
        
    Note:
        This endpoint should be removed or secured in production
    """
    try:
        # Load model
        comparator = load_model()
        
        # Create sample project data for testing
        sample_data = {
            'project_id': 'P3556',
            'reinforcement_ratio_kg_per_m3': 120.0,
            'num_unique_required_lengths': 20,
            'stock_length_policy': 'standard_12m',
            'cutting_optimization_usage': 0,
            'bim_integration_level': 0,
            'design_revisions_per_month': 2,
            'supervision_index_1to5': 3,
            'material_control_level_1to3': 2,
            'storage_handling_index_1to5': 3,
            'offcut_reuse_policy_0to2': 0,
            'change_orders_per_month': 1,
            'contract_type': 'lump_sum',
            'lead_time_days': 15,
            'order_frequency_per_month': 4,
            'project_phase': 'frame'
        }
        # Convert to DataFrame and get explanation
        df = pd.DataFrame([sample_data])
        explanation = comparator.explain_prediction(df, top_n=5)
        
        # Return raw explanation data for inspection
        return jsonify({
            'explanation': explanation,
            'top_features_raw': explanation['top_features']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    """
    Main entry point for running the Flask application.
    
    This block only executes when the script is run directly (not imported).
    It starts the Flask development server on localhost:5005.
    """
    # Print startup banner
    print("=" * 60)
    print("Steel Waste Prediction Web Application")
    print("=" * 60)
    print("Starting server on http://localhost:5005")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Check if model exists before starting server
    model_path = 'models/best_steel_waste_model.pkl'
    if not os.path.exists(model_path):
        print(f"\n⚠️  Warning: Model not found at {model_path}")
        print("Please run 'python model.py' first to train the model.\n")
    
    # Start Flask development server
    # debug=True: Enables auto-reload on code changes and detailed error pages
    # host='0.0.0.0': Makes server accessible from any network interface
    # port=5005: Custom port (default Flask port is 5000)
    # use_reloader=False: Disables auto-reloader (prevents double-loading of model)
    app.run(debug=True, host='0.0.0.0', port=5005, use_reloader=False)
