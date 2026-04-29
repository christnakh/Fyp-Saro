# Steel Waste Prediction System

<div align="center">

**Advanced Machine Learning System for Predicting Steel Waste in Construction Projects**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Academic-blue.svg)](LICENSE)

*Final Year Project - Civil Engineering Department*

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Model Training](#model-training)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)

---

## 🎯 Overview

The **Steel Waste Prediction System** is an intelligent web application that uses machine learning to predict steel waste percentage in construction projects. The system helps engineers, estimators, and project managers:

- **Predict** steel waste before construction begins
- **Understand** which factors drive waste (explainability)
- **Assess** prediction reliability
- **Quantify** financial and environmental impact
- **Make data-driven decisions** to reduce waste

### Problem Statement

Construction projects typically experience 5-15% steel waste, leading to:
- **Financial losses**: Wasted material costs
- **Environmental impact**: Unnecessary CO₂ emissions
- **Project delays**: Material shortages and rework

This system addresses these challenges by providing accurate, actionable predictions.

---

## ✨ Features

### 1. **Machine Learning Predictions**
- Trained on 10 different ML algorithms
- Best model: Gradient Boosting (MAE: 0.73%, R²: 0.93)
- 16 input parameters covering project characteristics

### 2. **Model Explainability** (Section 3.2)
- **SHAP-based explanations**: Shows which features drive predictions
- **Feature importance**: Identifies top waste-driving factors
- **Impact direction**: Indicates whether features increase or decrease waste

### 3. **Prediction Reliability Indicator** (Section 3.5)
- **High/Medium/Low** confidence levels
- Based on similarity to training data (k-NN approach)
- Helps engineers assess prediction trustworthiness

### 4. **Cost and CO₂ Impact Estimation** (Section 3.4)
- **Financial impact**: Calculates waste cost in USD
- **Environmental impact**: Estimates CO₂ emissions
- **Potential savings**: Shows achievable reductions

### 5. **Professional Web Interface** (Section 3.6)
- Modern, responsive design
- Intuitive form with 16 project parameters
- Real-time predictions
- Comprehensive results display

### 6. **Online Deployment** (Section 3.1)
- Cloud-ready Flask application
- Public URL access (when deployed)
- No local setup required for end users

---

## 🛠 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0.0**: Web framework
- **scikit-learn 1.3.2**: Machine learning library
- **XGBoost 2.0.3**: Gradient boosting algorithm
- **pandas 2.1.3**: Data manipulation
- **numpy 1.24.3**: Numerical operations
- **SHAP 0.43.0**: Model explainability
- **joblib 1.3.2**: Model serialization

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling (custom design system)
- **JavaScript (ES6+)**: Client-side interactivity
- **Bootstrap 5.3.0**: Responsive UI framework
- **Bootstrap Icons**: Icon library

### Data & Models
- **Synthetic Data Generation**: Research-based dataset creation
- **10 ML Models**: Comprehensive model comparison
- **Cross-Validation**: 10-fold K-Fold CV
- **Model Persistence**: Saved as `.pkl` files

---

## 📦 Installation

### Prerequisites

- Python 3.11 (recommended for deployment compatibility)
- pip (Python package manager)
- Git (optional, for cloning)

> Deployment note: this project includes `runtime.txt` and `.python-version` set to `3.11.11`.  
> If your host defaults to Python 3.14, force Python 3.11 in the hosting settings to avoid pandas build failures.

### Step 1: Clone or Download

```bash
# If using Git
git clone <repository-url>
cd CE_FYP_Revised_Proposal_Appendix_Folder_G09

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask and web dependencies
- Machine learning libraries
- Data processing tools
- SHAP for explainability

### Step 4: Verify Installation

```bash
python -c "import flask, pandas, sklearn, xgboost, shap; print('All packages installed successfully!')"
```

---

## 🚀 Quick Start

### Option 1: Use Pre-trained Model (Fastest)

If the model is already trained (`models/best_steel_waste_model.pkl` exists):

```bash
python app.py
```

Then open your browser to: **http://localhost:5005**

### Option 2: Train Model First (Complete Setup)

```bash
# Step 1: Generate training data
python data_generation/generate_train_test_data.py

# Step 2: Train and compare models
python model.py

# Step 3: Start web application
python app.py
```

---

## 📁 Project Structure

```
CE_FYP_Revised_Proposal_Appendix_Folder_G09/
│
├── app.py                          # Flask web application (main entry point)
├── model.py                        # ML model comparison and training
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/                           # Data files
│   ├── train_data.csv              # Training dataset
│   ├── test_data.csv               # Test dataset
│   ├── full_dataset.csv            # Complete dataset
│   ├── synthetic_steel_waste_parameters.csv  # Raw synthetic data
│   └── model_comparison_results.csv # Model evaluation results
│
├── data_generation/                # Data generation scripts
│   ├── synthetic_data_generator.py # Synthetic data creation
│   └── generate_train_test_data.py # Dataset splitting
│
├── models/                         # Trained models
│   └── best_steel_waste_model.pkl # Best performing model
│
├── static/                         # Static web assets
│   ├── css/
│   │   └── style.css              # Custom stylesheet
│   ├── js/
│   │   └── main.js                # JavaScript functionality
│   └── images/
│       └── placeholder.svg        # Placeholder images
│
└── templates/                      # HTML templates (Jinja2)
    ├── base.html                   # Base template
    ├── index.html                  # Landing page
    ├── predict.html                # Prediction page
    ├── about.html                  # About page
    └── features.html               # Features page
```

---

## 📖 Usage Guide

### Web Interface

1. **Navigate to Home**: http://localhost:5005
2. **Click "Predict"** in navigation or "Get Started" button
3. **Fill in Project Parameters**:
   - Project Information (ID, Phase)
   - Material Parameters (Reinforcement ratio, lengths, stock policy)
   - Management & Control (Supervision, material control, storage)
   - Design & Planning (BIM level, design revisions, change orders)
   - Procurement (Contract type, lead time, order frequency)
   - Offcut Reuse Policy
   - Total Steel Quantity (for cost/CO₂ calculations)
4. **Click "Predict Steel Waste"**
5. **View Results**:
   - Predicted waste percentage
   - Waste category (Excellent/Good/Average/Poor/Very Poor)
   - Top 5 influential features
   - Reliability indicator
   - Cost and CO₂ impact

### Input Parameters

| Parameter | Description | Range/Options |
|-----------|-------------|---------------|
| **Reinforcement Ratio** | Steel quantity per m³ of concrete | 60-180 kg/m³ |
| **Number of Unique Lengths** | Different rebar lengths required | 5-40 |
| **Stock Length Policy** | Rebar stock management approach | Standard 12m / Mixed / Custom |
| **Cutting Optimization** | Level of cutting optimization | None (0) / Basic (1) / Advanced (2) |
| **BIM Integration Level** | Building Information Modeling usage | 0-3 |
| **Design Revisions** | Monthly design change frequency | 0-10 |
| **Supervision Index** | Quality of site supervision | 1-5 |
| **Material Control Level** | Material management quality | 1-3 |
| **Storage Handling Index** | Storage and handling quality | 1-5 |
| **Offcut Reuse Policy** | Offcut material reuse strategy | None (0) / Limited (1) / Systematic (2) |
| **Change Orders** | Monthly change order frequency | 0-8 |
| **Contract Type** | Project contract structure | Lump Sum / Design Build / Remeasurement |
| **Lead Time** | Material procurement lead time | 3-30 days |
| **Order Frequency** | Material ordering frequency | 1-8 per month |
| **Project Phase** | Current construction phase | Foundation / Frame / Slab Finishing |

---

## 🤖 Model Training

### Generate Training Data

```bash
python data_generation/generate_train_test_data.py
```

**What it does:**
- Generates 3,000 synthetic projects
- Splits into 80% training (2,400) and 20% test (600)
- Saves to `data/train_data.csv` and `data/test_data.csv`

**Customization:**
Edit the script to change:
- Number of projects (`n_projects`)
- Test size (`test_size`)
- Random seed (`seed`)

### Train and Compare Models

```bash
python model.py
```

**What it does:**
1. Loads training and test datasets
2. Tests 10 different ML algorithms:
   - Gradient Boosting
   - XGBoost
   - Random Forest
   - Extra Trees
   - AdaBoost
   - Decision Tree
   - Linear Regression
   - Ridge Regression
   - Lasso Regression
   - Elastic Net
3. Evaluates with cross-validation (10-fold)
4. Calculates metrics: MAE, RMSE, R², MAPE
5. Selects best model (lowest MAE)
6. Saves to `models/best_steel_waste_model.pkl`
7. Generates feature importance analysis

**Expected Output:**
```
PROFESSIONAL MODEL COMPARISON SYSTEM
================================================================================
[1/4] Preparing data...
  ✓ Training set: 2,400 samples, 16 features
  ✓ Test set: 600 samples, 16 features

[2/4] Testing 10 models with 10-fold cross-validation...

🏆 BEST MODEL: Gradient Boosting
  Test MAE:        0.7300%
  Test RMSE:       0.9200%
  Test R²:         0.9300
  CV MAE:          0.7700% (±0.0500)
```

### Model Performance

| Model | Test MAE (%) | Test RMSE (%) | Test R² | CV MAE (%) |
|-------|--------------|---------------|---------|------------|
| **Gradient Boosting** | **0.73** | **0.92** | **0.93** | **0.77** |
| XGBoost | 0.75 | 0.94 | 0.92 | 0.79 |
| Random Forest | 1.01 | 1.25 | 0.87 | 1.08 |
| Linear Regression | 0.76 | 0.97 | 0.92 | 0.78 |

---

## 🔌 API Documentation

### Endpoint: `/api/predict`

**Method:** `POST`

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "reinforcement_ratio_kg_per_m3": 120.0,
  "num_unique_required_lengths": 20,
  "stock_length_policy": "standard_12m",
  "cutting_optimization_usage": 0,
  "bim_integration_level": 0,
  "design_revisions_per_month": 2,
  "supervision_index_1to5": 3,
  "material_control_level_1to3": 2,
  "storage_handling_index_1to5": 3,
  "offcut_reuse_policy_0to2": 0,
  "change_orders_per_month": 1,
  "contract_type": "lump_sum",
  "lead_time_days": 15,
  "order_frequency_per_month": 4,
  "project_phase": "frame",
  "total_steel_kg": 100000
}
```

**Response (Success):**
```json
{
  "success": true,
  "predicted_waste_percentage": 6.52,
  "waste_category": "Good",
  "reliability": {
    "reliability_score": 0.75,
    "reliability_level": "high",
    "message": "Input data is very similar to training data. High confidence in prediction."
  },
  "explainability": {
    "method": "SHAP",
    "top_features": [
      {
        "feature": "offcut_reuse_policy_0to2",
        "contribution": -0.0234,
        "impact": "negative"
      }
    ]
  },
  "cost_co2_impact": {
    "waste_kg": 6520.0,
    "waste_cost_usd": 5216.0,
    "waste_co2_kg": 16300.0,
    "potential_cost_savings_usd": 2608.0,
    "potential_co2_reduction_kg": 8150.0
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message here"
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid data or error)

### Example: Python API Call

```python
import requests
import json

url = "http://localhost:5005/api/predict"
data = {
    "reinforcement_ratio_kg_per_m3": 120.0,
    "num_unique_required_lengths": 20,
    "stock_length_policy": "standard_12m",
    # ... (all other parameters)
    "total_steel_kg": 100000
}

response = requests.post(url, json=data)
result = response.json()

print(f"Predicted Waste: {result['predicted_waste_percentage']}%")
print(f"Category: {result['waste_category']}")
print(f"Cost Impact: ${result['cost_co2_impact']['waste_cost_usd']:,.0f}")
```

---

## 📸 Screenshots

### Landing Page
- Hero section with project description
- Feature showcase
- How it works section
- Statistics and call-to-action

### Prediction Page
- Comprehensive input form
- Real-time prediction results
- Explainability features display
- Reliability indicators
- Cost and CO₂ impact cards

### Results Display
- Waste percentage with category badge
- Top 5 influential features
- Reliability score and level
- Financial and environmental impact
- Potential savings calculations

---

## 🔧 Configuration

### Port Configuration

To change the server port, edit `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5005)  # Change 5005 to desired port
```

### Model Path

Default model path: `models/best_steel_waste_model.pkl`

To change, edit `app.py`:

```python
model_path = 'models/best_steel_waste_model.pkl'  # Update path here
```

### Cost and CO₂ Parameters

Default values in `model.py`:

```python
steel_cost_per_kg: float = 0.8      # USD per kg
co2_per_kg_steel: float = 2.5       # kg CO₂ per kg steel
```

Update these based on your market rates.

---

## 🐛 Troubleshooting

### Issue: Model not found

**Error:** `FileNotFoundError: Model not found at models/best_steel_waste_model.pkl`

**Solution:**
```bash
# Train the model first
python model.py
```

### Issue: Port already in use

**Error:** `Address already in use`

**Solution:**
- Change port in `app.py` (see Configuration section)
- Or stop the process using port 5005

### Issue: SHAP not available

**Warning:** `SHAP not available. Install with 'pip install shap'`

**Solution:**
```bash
pip install shap
```

### Issue: Import errors

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Data generation fails

**Error:** Issues generating synthetic data

**Solution:**
- Check Python version (3.8+ required)
- Verify all dependencies installed
- Check file permissions in `data/` folder

---

## 📊 Data Generation

### Synthetic Data Overview

The system uses research-based synthetic data generation when real project data is limited. The generator:

- **Creates realistic projects** based on industry distributions
- **Maintains correlations** between parameters
- **Calculates waste** using research-derived formulas
- **Validates outputs** with quality control checks

### Data Dictionary

See `data/data_dictionary.xlsx` for complete parameter documentation including:
- Variable definitions
- Units and ranges
- Statistical distributions
- Quality control checks

### Generating Custom Data

Edit `data_generation/synthetic_data_generator.py` to:
- Adjust parameter distributions
- Modify waste calculation formula
- Add new parameters
- Change dataset size

---

## 🧪 Testing

### Manual Testing

1. **Test Prediction Form:**
   - Fill all required fields
   - Submit and verify results display
   - Check explainability features
   - Verify reliability indicator

2. **Test API:**
   ```bash
   curl -X POST http://localhost:5005/api/predict \
     -H "Content-Type: application/json" \
     -d @test_request.json
   ```

3. **Test Model:**
   ```python
   from model import ModelComparison
   import pandas as pd
   
   comparator = ModelComparison()
   comparator.load_model('models/best_steel_waste_model.pkl')
   
   test_data = pd.read_csv('data/test_data.csv')
   predictions = comparator.predict(test_data.head(10))
   print(predictions)
   ```

---

## 🤝 Contributing

This is a Final Year Project. For suggestions or improvements:

1. Document the issue or enhancement
2. Provide detailed description
3. Include code examples if applicable

---

## 👥 Team

**Final Year Project - Group G09**

**Advisors:**
- Dr. Mohamed-Asem Abdul Malak
- Dr. Farah Demachkieh

**Students:**
- Lucas Chebly (202305338)
- Saro Meghdessian (202309358)
- Shahan Nadjarian (202304615)
- Jad Raad (202309924)

**Institution:**
American University of Beirut (AUB)
Department of Civil and Environmental Engineering

---

## 🙏 Acknowledgments

- **A.R. Hourie Enterprises** for providing construction project data
- **Ms. Karen El Zind** for expert guidance and industry insights
- **Dr. Alissar Yehya** and **Dr. Dima Al Hassanieh** for weekly guidance
- **AUB Computer Labs** for computational resources

---

## 📄 License

This project is developed for academic purposes as part of the Final Year Project requirement at the American University of Beirut.

**Academic Use Only** - Not for commercial distribution.

---

## 📚 References

- Research papers on construction waste drivers
- Industry standards for steel waste in construction
- Machine learning best practices
- SHAP documentation for model explainability

For complete references, see the project proposal document.

---

## 🔗 Related Documents

- **Technical appendix (full — report / examiner handover):** [`TECHNICAL_APPENDIX_FULL.md`](TECHNICAL_APPENDIX_FULL.md) — repository tree, `requirements.txt`, data pipeline, all model features, Flask routes, `/api/predict` JSON, `curl` example, saved-model bundle, reliability/SHAP/cost formulas at code level.
- **Second-semester narrative:** [`SECOND_SEMESTER_ADDENDUM.md`](SECOND_SEMESTER_ADDENDUM.md) — proposal vs. implementation table and where to paste it in the written report.
- **Project Proposal**: `CE_FYP_Revised_Proposal_G09.pdf` (if supplied)
- **Data Dictionary**: `data/data_dictionary.xlsx`
- **Model Results**: `data/model_comparison_results.csv`
- **Code Documentation**: Inline comments in `app.py`, `model.py`, and `data_generation/`

---

## 📞 Contact

For questions or support:
- Check inline code documentation
- Review project proposal
- Contact project advisors

---

## 🎓 Project Status

**Current Status:** ✅ Complete

**Completed Features:**
- ✅ Synthetic data generation
- ✅ Model training and comparison
- ✅ Web application interface
- ✅ Model explainability (SHAP)
- ✅ Prediction reliability indicators
- ✅ Cost and CO₂ impact estimation
- ✅ Professional documentation

**Future Enhancements:**
- Integration with real project data
- Additional material types (concrete, etc.)
- Mobile application
- Advanced visualization dashboards

---

<div align="center">

**Built with ❤️ by FYP Team G09**

*American University of Beirut - 2026*

</div>
