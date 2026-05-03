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
from config import CO2_PER_KG_STEEL, STEEL_COST_PER_KG_USD

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

def train_model_if_needed(model_path='models/best_steel_waste_model.pkl'):
    """
    Train and save the model if the model file does not exist.
    Requires data/train_data.csv and data/test_data.csv to be present.
    """
    if os.path.exists(model_path):
        return
    print(f"Model not found at {model_path}. Training model...")
    try:
        train_df = pd.read_csv('data/train_data.csv')
        test_df = pd.read_csv('data/test_data.csv')
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Training data not found. Please run 'data_generation/generate_train_test_data.py' first to create data/train_data.csv and data/test_data.csv. Original error: {e}"
        )
    comparator = ModelComparison(cv_folds=10, random_state=42)
    comparator.compare_models(train_df, test_df)
    comparator.save_best_model(model_path)
    print("Model training complete.")

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
            train_model_if_needed(model_path)
        
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

# Category blurbs (HTML + /api/predict live updates)
WASTE_CATEGORY_INTERPRETATIONS = {
    'Excellent': 'Excellent waste management! This project demonstrates best practices with minimal material waste.',
    'Good': 'Good waste management. The project is performing well with acceptable waste levels.',
    'Average': 'Average waste levels. Consider implementing optimization strategies to improve efficiency.',
    'Poor': 'Poor waste management. Immediate action needed to reduce waste and improve material control.',
    'Very Poor': 'Very poor waste management. Critical review of processes required to address excessive waste.',
}

RELIABILITY_BADGE_COLORS = {
    'high': 'success',
    'medium': 'warning',
    'low': 'danger',
}

# Feature columns required in JSON body for /api/predict (project_id optional; filled if absent)
API_PREDICT_FEATURE_KEYS = frozenset({
    'reinforcement_ratio_kg_per_m3',
    'num_unique_required_lengths',
    'stock_length_policy',
    'cutting_optimization_usage',
    'bim_integration_level',
    'design_revisions_per_month',
    'supervision_index_1to5',
    'material_control_level_1to3',
    'storage_handling_index_1to5',
    'offcut_reuse_policy_0to2',
    'change_orders_per_month',
    'contract_type',
    'lead_time_days',
    'order_frequency_per_month',
    'project_phase',
})

# Human-readable names for model feature keys (UI + API)
FEATURE_DISPLAY_NAMES = {
    'offcut_reuse_policy_0to2': 'Offcut Reuse Policy',
    'cutting_optimization_usage': 'Cutting Optimization Usage',
    'change_orders_per_month': 'Change Orders Per Month',
    'stock_length_policy': 'Stock Length Policy',
    'design_revisions_per_month': 'Design Revisions Per Month',
    'bim_integration_level': 'BIM Integration Level',
    'supervision_index_1to5': 'Supervision Index',
    'material_control_level_1to3': 'Material Control Level',
    'storage_handling_index_1to5': 'Storage Handling Index',
    'reinforcement_ratio_kg_per_m3': 'Reinforcement Ratio (kg/m³)',
    'num_unique_required_lengths': 'Number of Unique Required Lengths',
    'lead_time_days': 'Lead Time (days)',
    'order_frequency_per_month': 'Order Frequency per Month',
    'contract_type': 'Contract Type',
    'project_phase': 'Project Phase',
}

PARAMETER_HELP_FALLBACK = 'No detailed definition is configured for this parameter.'
PARAMETER_HELP = {
    'reinforcement_ratio_kg_per_m3': (
        'The amount of steel used per cubic meter of concrete.\n'
        'On the form, typical range is 60–180 kg/m³.'
    ),
    'num_unique_required_lengths': (
        'The number of different bar lengths needed in the project.\n'
        'On the form, typical range is 5–40.'
    ),
    'stock_length_policy': (
        'The type of bar lengths purchased from suppliers (for example standard 12 m, mixed lengths, or custom).'
    ),
    'cutting_optimization_usage': (
        'The level of optimization used when planning steel cutting (0–2).\n\n'
        '0 — No optimization: bars are cut on site without a planned cutting layout.\n'
        '1 — Basic: the team manually arranges cuts to reduce leftovers.\n'
        '2 — Advanced: specialized software generates cutting patterns.'
    ),
    'bim_integration_level': (
        'The extent to which BIM is used in the project (model uses 0–3).\n\n'
        '0 — None: matches the trained model’s “no BIM” bucket.\n'
        '1 — Limited: drawings coordinated mainly through 2D plans.\n'
        '2 — Moderate: BIM used for parts of coordination and planning.\n'
        '3 — Strong: 3D BIM for clash detection, rebar coordination, and detailing.'
    ),
    'design_revisions_per_month': (
        'The number of design changes made in an average month.'
    ),
    'supervision_index_1to5': (
        'A rating of site supervision quality (1–5).\n\n'
        '1 — Very weak: limited checking of cutting, placement, and material use.\n'
        '5 — Very strong: regular inspections and close monitoring of steel work and wastage.'
    ),
    'material_control_level_1to3': (
        'How well steel materials are tracked and managed (1–3).\n\n'
        '1 — Poor: little recording or inventory follow-up.\n'
        '3 — Strong: quantities logged, monitored, and checked throughout the project.'
    ),
    'storage_handling_index_1to5': (
        'How well steel is stored and handled on site (1–5).\n\n'
        '1 — Very poor: exposed, mixed randomly, or handled carelessly.\n'
        '5 — Very good: neat storage, protection, and organized movement.'
    ),
    'offcut_reuse_policy_0to2': (
        'How much leftover cut pieces are reused (0–2).\n\n'
        '0 — None: offcuts discarded after cutting.\n'
        '1 — Basic: occasional reuse when a suitable use is noticed.\n'
        '2 — Systematic: leftovers sorted, stored, and reused by a clear process.'
    ),
    'change_orders_per_month': (
        'The number of scope or drawing changes made in an average month.'
    ),
    'contract_type': (
        'The contractual arrangement used in the project (for example lump sum, design-build, or remeasurement).'
    ),
    'lead_time_days': (
        'The number of days between placing a steel order and receiving it.'
    ),
    'order_frequency_per_month': (
        'The number of steel orders placed per month.'
    ),
    'project_phase': (
        'The current stage of the project—for example foundation, frame, or slab/finishing.'
    ),
}


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


def _json_safe(obj):
    """Convert numpy scalars and nested structures for Jinja ``|tojson`` / jsonify."""
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    if isinstance(obj, (np.integer, np.int64, np.int32, np.intc)):
        return int(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def split_shap_driver_lists(explanation: dict):
    """
    Top three positive SHAP (increase waste) and top three negative (decrease waste).
    Returns (positive_features, negative_features, shap_ok).
    """
    if explanation.get('method') != 'SHAP' or not explanation.get('all_features'):
        return [], [], False
    all_f = explanation['all_features']
    pos = sorted([(k, float(v)) for k, v in all_f.items() if v > 0], key=lambda x: -x[1])[:3]
    neg = sorted([(k, float(v)) for k, v in all_f.items() if v < 0], key=lambda x: x[1])[:3]

    def _row(k, v):
        return {
            'feature': k,
            'contribution': v,
            'display': FEATURE_DISPLAY_NAMES.get(k, k.replace('_', ' ').title()),
            'help': PARAMETER_HELP.get(k, PARAMETER_HELP_FALLBACK),
        }

    return [_row(k, v) for k, v in pos], [_row(k, v) for k, v in neg], True


def _gauge_scale(pred, p10, p90, intervals_ok):
    """Linear scale endpoints and marker position (0–100%)."""
    if intervals_ok and p10 is not None and p90 is not None:
        lo = float(min(p10, pred)) - 0.5
        hi = float(max(p90, pred)) + 0.5
    else:
        lo, hi = 0.0, max(15.0, float(pred) + 2.0)
    if hi <= lo:
        hi = lo + 2.0

    def pct(val):
        return max(0.0, min(100.0, (float(val) - lo) / (hi - lo) * 100.0))

    out = {
        'gauge_lo': lo,
        'gauge_hi': hi,
        'marker_pct': pct(pred),
        'p10_pct': pct(p10) if intervals_ok and p10 is not None else None,
        'p90_pct': pct(p90) if intervals_ok and p90 is not None else None,
    }
    return out


def build_prediction_bundle(comparator: ModelComparison, row: dict, total_steel_kg: float) -> dict:
    """
    Single code path for HTML and JSON predictions.
    `row` must contain all model feature columns (no total_steel_kg).
    """
    steel_cost = STEEL_COST_PER_KG_USD
    co2_factor = CO2_PER_KG_STEEL

    df = pd.DataFrame([row])
    prediction = float(comparator.predict(df)[0])
    intervals = comparator.prediction_intervals_for_row(df)
    intervals_ok = bool(intervals.get('available'))
    p10 = intervals.get('p10')
    p90 = intervals.get('p90')

    explanation = comparator.explain_prediction(df, top_n=5)
    reliability = comparator.calculate_reliability(df)
    cost_co2 = comparator.calculate_cost_co2_impact(
        prediction,
        total_steel_kg=total_steel_kg,
        steel_cost_per_kg=steel_cost,
        co2_per_kg_steel=co2_factor,
    )
    counterfactual = comparator.calculate_counterfactual_potential(
        df, explanation, total_steel_kg, steel_cost, co2_factor
    )

    pos_feats, neg_feats, shap_split = split_shap_driver_lists(explanation)
    scenario_keys = []
    for item in pos_feats + neg_feats:
        fk = item['feature']
        if fk not in scenario_keys:
            scenario_keys.append(fk)

    bounds = {}
    if comparator.training_feature_bounds:
        for k in scenario_keys:
            if k in comparator.training_feature_bounds:
                bounds[k] = comparator.training_feature_bounds[k]

    api_row = {**row, 'total_steel_kg': float(total_steel_kg)}
    scenario_json = _json_safe({
        'apiPayloadBaseline': api_row,
        'scenarioFeatureKeys': scenario_keys,
        'bounds': bounds,
        'displayNames': {k: FEATURE_DISPLAY_NAMES.get(k, k) for k in scenario_keys},
        'helps': {k: PARAMETER_HELP.get(k, PARAMETER_HELP_FALLBACK) for k in scenario_keys},
    })

    gauge = _gauge_scale(prediction, p10, p90, intervals_ok)

    return {
        'prediction': prediction,
        'p10': p10,
        'p90': p90,
        'intervals_available': intervals_ok,
        'explanation': explanation,
        'reliability': reliability,
        'cost_co2': cost_co2,
        'counterfactual': counterfactual,
        'positive_features': pos_feats,
        'negative_features': neg_feats,
        'shap_split': shap_split,
        'scenario_json': scenario_json,
        'gauge': gauge,
        'steel_cost_per_kg': steel_cost,
        'co2_per_kg_steel': co2_factor,
    }


def _template_vars_from_bundle(bundle, form_data):
    """Flatten bundle into predict.html template variables."""
    pred = bundle['prediction']
    p10 = bundle['p10']
    p90 = bundle['p90']
    intervals_ok = bundle['intervals_available']
    reliability = bundle['reliability']
    cost = bundle['cost_co2']
    cf = bundle['counterfactual']
    explanation = bundle['explanation']
    gauge = bundle['gauge']
    category, category_color = get_waste_category(pred)

    reliability_badge_color = RELIABILITY_BADGE_COLORS[reliability['reliability_level']]

    if cf['available']:
        potential_savings_cost = f"${cf['potential_cost_savings_usd']:,.0f}"
        potential_co2_reduction = f"{cf['potential_co2_reduction_kg']:,.0f}"
        savings_subtext = (
            'If the three strongest waste-increasing factors (SHAP) matched average levels '
            'in the synthetic training database.'
        )
    else:
        potential_savings_cost = 'N/A'
        potential_co2_reduction = 'N/A'
        savings_subtext = cf.get('message', 'Not available for this prediction.')

    explainability_fallback_html = (
        format_explainability_features(explanation) if not bundle['shap_split'] else ''
    )

    return {
        'has_prediction': True,
        'predicted_waste': f'{pred:.2f}',
        'p10_display': f'{p10:.2f}' if intervals_ok and p10 is not None else '—',
        'p90_display': f'{p90:.2f}' if intervals_ok and p90 is not None else '—',
        'intervals_available': intervals_ok,
        'gauge_lo': gauge['gauge_lo'],
        'gauge_hi': gauge['gauge_hi'],
        'gauge_marker_pct': gauge['marker_pct'],
        'gauge_p10_pct': gauge['p10_pct'],
        'gauge_p90_pct': gauge['p90_pct'],
        'category': category,
        'category_color': category_color,
        'interpretation': WASTE_CATEGORY_INTERPRETATIONS[category],
        'reliability_level': reliability['reliability_level'].upper(),
        'reliability_color': reliability_badge_color,
        'reliability_message': reliability['message'],
        'reliability_score': f"{reliability['reliability_score']:.0%}",
        'waste_cost': f"${cost['waste_cost_usd']:,.0f}",
        'waste_co2': f"{cost['waste_co2_kg']:,.0f}",
        'potential_savings_cost': potential_savings_cost,
        'potential_co2_reduction': potential_co2_reduction,
        'total_steel_kg': f"{cost['total_steel_kg']:,.0f}",
        'waste_kg': f"{cost['waste_kg']:,.0f}",
        'unit_cost_label': f"${bundle['steel_cost_per_kg']:.2f}/kg steel (waste)",
        'unit_co2_label': f"{bundle['co2_per_kg_steel']:.2f} kg CO₂/kg steel waste",
        'savings_subtext': savings_subtext,
        'explainability_method': explanation['method'],
        'positive_features': bundle['positive_features'],
        'negative_features': bundle['negative_features'],
        'shap_split': bundle['shap_split'],
        'explainability_fallback_html': explainability_fallback_html,
        'scenario_json': bundle['scenario_json'],
        'form_data': form_data,
        'prediction_error': None,
    }


def _empty_predict_template_vars():
    """Defaults when no prediction has been run."""
    return {
        'has_prediction': False,
        'prediction_error': None,
        'predicted_waste': '',
        'p10_display': '—',
        'p90_display': '—',
        'intervals_available': False,
        'gauge_lo': 0.0,
        'gauge_hi': 15.0,
        'gauge_marker_pct': 0.0,
        'gauge_p10_pct': None,
        'gauge_p90_pct': None,
        'category': '',
        'category_color': 'secondary',
        'interpretation': 'Enter project parameters and click "Predict Steel Waste" to get started.',
        'reliability_level': '',
        'reliability_color': 'secondary',
        'reliability_message': '',
        'reliability_score': '',
        'waste_cost': '$0',
        'waste_co2': '0',
        'potential_savings_cost': '$0',
        'potential_co2_reduction': '0',
        'total_steel_kg': '100,000',
        'waste_kg': '0',
        'unit_cost_label': f'${STEEL_COST_PER_KG_USD:.2f}/kg steel (waste)',
        'unit_co2_label': f'{CO2_PER_KG_STEEL:.2f} kg CO₂/kg steel waste',
        'savings_subtext': '',
        'explainability_method': 'Feature Importance',
        'positive_features': [],
        'negative_features': [],
        'shap_split': False,
        'explainability_fallback_html': '<p class="text-muted">Make a prediction to see feature contributions.</p>',
        'scenario_json': None,
        'form_data': None,
    }


def _json_api_response(bundle: dict) -> dict:
    """Shape returned by /api/predict."""
    pred = bundle['prediction']
    category, _ = get_waste_category(pred)
    intervals_ok = bundle['intervals_available']
    cf = bundle['counterfactual']
    pos = bundle['positive_features']
    neg = bundle['negative_features']
    shap_ok = bundle['shap_split']

    scenario_keys = [x['feature'] for x in pos + neg]
    unique_keys = []
    for k in scenario_keys:
        if k not in unique_keys:
            unique_keys.append(k)
    param_help = {k: PARAMETER_HELP.get(k, PARAMETER_HELP_FALLBACK) for k in unique_keys}

    rel = bundle['reliability']
    rel_level = rel['reliability_level']
    return _json_safe({
        'success': True,
        'predicted_waste_percentage': round(pred, 2),
        'p10': round(bundle['p10'], 2) if intervals_ok and bundle['p10'] is not None else None,
        'p90': round(bundle['p90'], 2) if intervals_ok and bundle['p90'] is not None else None,
        'prediction_intervals_available': intervals_ok,
        'waste_category': category,
        'interpretation': WASTE_CATEGORY_INTERPRETATIONS[category],
        'reliability': rel,
        'reliability_badge_color': RELIABILITY_BADGE_COLORS.get(rel_level, 'secondary'),
        'reliability_level_display': rel_level.upper(),
        'reliability_score_display': f"{rel['reliability_score']:.0%}",
        'explainability': bundle['explanation'],
        'explainability_positive': pos,
        'explainability_negative': neg,
        'shap_directional_split': shap_ok,
        'cost_co2_impact': bundle['cost_co2'],
        'counterfactual_savings': cf,
        'gauge': bundle['gauge'],
        'parameter_help': param_help,
        'scenario_context': bundle['scenario_json'],
    })


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
    ctx = _empty_predict_template_vars()
    return render_template(
        'predict.html',
        project_id=str(np.random.randint(1000, 9999)),
        **ctx,
    )

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
        comparator = load_model()

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
            'project_phase': request.form.get('project_phase', 'frame'),
        }

        total_steel_kg = float(request.form.get('total_steel_kg', 100000))
        bundle = build_prediction_bundle(comparator, data, total_steel_kg)
        form_with_steel = dict(data)
        form_with_steel['total_steel_kg'] = total_steel_kg
        tpl = _template_vars_from_bundle(bundle, form_with_steel)

        return render_template(
            'predict.html',
            project_id=data['project_id'],
            **tpl,
        )

    except Exception as e:
        err_ctx = _empty_predict_template_vars()
        err_ctx['prediction_error'] = str(e)
        return render_template(
            'predict.html',
            project_id=str(np.random.randint(1000, 9999)),
            **err_ctx,
        )

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
        comparator = load_model()
        payload = request.get_json(silent=True) or {}
        if not isinstance(payload, dict):
            return jsonify({'success': False, 'error': 'JSON object required'}), 400

        total_steel_kg = float(payload.pop('total_steel_kg', 100000))
        row = dict(payload)
        if 'project_id' not in row or row['project_id'] is None:
            row['project_id'] = 'P' + str(np.random.randint(1000, 9999))

        missing = sorted(k for k in API_PREDICT_FEATURE_KEYS if k not in row)
        if missing:
            return jsonify({
                'success': False,
                'error': (
                    'Missing required project fields: '
                    + ', '.join(missing)
                    + '. Send all model parameters as JSON (see /api/predict docstring).'
                ),
            }), 400

        bundle = build_prediction_bundle(comparator, row, total_steel_kg)
        return jsonify(_json_api_response(bundle))
    except Exception as e:
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
    
    # Ensure model exists before starting server (train if missing)
    model_path = 'models/best_steel_waste_model.pkl'
    if not os.path.exists(model_path):
        try:
            train_model_if_needed(model_path)
        except FileNotFoundError as e:
            print(f"\n⚠️  {e}\n")
    else:
        print(f"\n✓ Model found at {model_path}\n")
    
    # Start Flask development server
    # debug=True: Enables auto-reload on code changes and detailed error pages
    # host='0.0.0.0': Makes server accessible from any network interface
    # port=5005: Custom port (default Flask port is 5000)
    # use_reloader=False: Disables auto-reloader (prevents double-loading of model)
    app.run(debug=True, host='0.0.0.0', port=5006, use_reloader=False)
