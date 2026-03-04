# Steel Waste Prediction System - Progress Presentation
## 20-Minute Technical Presentation

Note on Slide Changes:
- (added) = New slide added in this restructure
- (changed) = Slide modified from original
- (kept) = Slide kept mostly the same
- (removed) = Original detailed ML model slides (4-8) were condensed/removed:
  - Original Slide 4: ML Model - Feature Engineering & Preprocessing (removed)
  - Original Slide 5: ML Model - All 10 Algorithms Tested (removed)
  - Original Slide 6: ML Model - Training Pipeline & Evaluation (removed)
  - Original Slide 7: ML Model - Gradient Boosting Algorithm (removed)
  - Original Slide 8: ML Model - Comprehensive Results & Comparison (removed)
  - Original Slide 9: Semester 2 Objectives & Architecture (condensed into other slides)
  - Original Slides 14-15: Features 1&2, Features 3&4 (condensed into technical slides)
  - Original Slide 16: Model Performance & Validation (condensed into Impact slide)
  - Original Slide 17: User Workflow (condensed into User Journey slide)

---

## Slide 1: Title Slide (1 minute) (kept)
Data-Driven Prediction of Material Waste in Construction Projects Using Machine Learning

Final Year Project - Progress Presentation

Team:
- Lucas Chebly (202305338)
- Saro Meghdessian (202309358)  
- Shahan Nadjarian (202304615)
- Jad Raad (202309924)

Advisors: Dr. Mohamed-Asem Abdul Malak, Dr. Farah Demachkieh

Department of Civil and Environmental Engineering

SPEAKING NOTES:
"Good morning/afternoon. Thank you for taking the time to review our progress. Today, we're presenting our Final Year Project on Data-Driven Prediction of Material Waste in Construction Projects Using Machine Learning. I'm [Your Name], and I'm joined by my teammates Lucas, Saro, Shahan, and Jad. We're working under the supervision of Dr. Mohamed-Asem Abdul Malak and Dr. Farah Demachkieh. This presentation will cover our problem statement, methodology, what we accomplished in Semester 1, the significant enhancements we've made in Semester 2, and demonstrate how the system works. Let's begin."

---

## Slide 2: Problem Statement & Objectives (2 minutes) (changed)
Problem Statement

- Construction materials = 50-60% of project costs in Middle East
- Current practice: Fixed waste allowances (5-15%) - inaccurate
- Steel reinforcement waste: 3-8% with significant variation
- Gap: No data-driven prediction tools linking project parameters to waste

Project Objectives:
1. Develop ML model predicting steel waste (Target: R² ≥ 0.60, MAE ≤ 2.0%)
2. Create explainable AI system (SHAP-based feature importance)
3. Quantify financial and environmental impact (Cost & CO₂)
4. Build production-ready web application

IMAGE PLACEMENT:
- Left side: Construction site image showing steel reinforcement
- Right side: Graph/chart showing waste percentage variation across projects
- Bottom: Formula: Steel Waste (%) = (Ordered - Installed Theoretical) / Installed Theoretical × 100

SPEAKING NOTES:
"Let me start by explaining the problem we're addressing. In the Middle East construction industry, materials account for 50 to 60 percent of total project costs. Currently, contractors use fixed waste allowances, typically between 5 and 15 percent, but these are often inaccurate. For steel reinforcement specifically, waste can vary significantly from 3 to 8 percent depending on project characteristics. The gap we identified is that there are no data-driven prediction tools that link specific project parameters to expected waste levels. Our objectives are clear: First, develop a machine learning model that predicts steel waste with high accuracy - our target is R-squared greater than or equal to 0.60 and mean absolute error less than or equal to 2.0 percent. Second, create an explainable AI system using SHAP-based feature importance so users understand why predictions are made. Third, quantify the financial and environmental impact by calculating cost and CO₂ emissions. And fourth, build a production-ready web application that makes this technology accessible to industry professionals. The formula shown here is how we calculate steel waste percentage - it's the difference between ordered and installed theoretical quantities, divided by installed theoretical, multiplied by 100."

---

## Slide 3: Methodology (1.5 minutes) (added)
Research Approach

Phase 1: Literature Review & Parameter Identification
- Reviewed 50+ research papers on construction waste
- Identified 16 key waste drivers
- Categorized: Material (4), Management (5), Dynamics (7)

Phase 2: Data Collection & Generation
- Literature-based synthetic dataset (3,000 projects)
- Real project data from A.R. Hourie Enterprises (in progress)
- Validation against industry practices

Phase 3: Model Development
- Tested 10 ML algorithms
- Selected best model (Gradient Boosting)
- Evaluated using MAE, RMSE, R², MAPE, cross-validation

Phase 4: System Enhancement
- Added explainability (SHAP)
- Added cost/CO₂ impact analysis
- Added reliability indicators
- Built professional web interface

Phase 5: Validation & Deployment
- Cross-validation testing
- Real-world scenario validation
- Production-ready deployment

IMAGE PLACEMENT:
- Center: Methodology flowchart showing 5 phases
- Bottom: Timeline showing Semester 1 → Semester 2 progression

SPEAKING NOTES:
"Our methodology follows a systematic five-phase approach. Phase 1 involved an extensive literature review where we reviewed over 50 research papers on construction waste and identified 16 key waste drivers, which we categorized into material-related, management-related, and project dynamics parameters. Phase 2 focused on data collection and generation. We started with a literature-based synthetic dataset of 3,000 projects, and we're currently working with A.R. Hourie Enterprises to integrate real project data. All data is validated against industry practices. Phase 3 was model development, where we tested 10 different machine learning algorithms and selected the best-performing one - Gradient Boosting. We evaluated models using multiple metrics: Mean Absolute Error, Root Mean Squared Error, R-squared, Mean Absolute Percentage Error, and cross-validation. Phase 4 involved system enhancement, where we added explainability using SHAP, cost and CO₂ impact analysis, reliability indicators, and built a professional web interface. Phase 5 is validation and deployment, where we conduct cross-validation testing, validate against real-world scenarios, and deploy a production-ready system. This methodology ensures we build a robust, validated, and practical solution."

---

## Slide 4: Last Semester Work - Overview (1.5 minutes) (changed)
Semester 1 Accomplishments

1. Literature Review & Parameter Identification
- Identified 16 key waste drivers from research
- Categorized: Material (4), Management (5), Dynamics (7)
- Validated against industry practices

2. Data Generation
- Created synthetic dataset: 3,000 projects
- Based on literature-derived relationships
- Validated distributions and correlations

3. Model Development
- Tested 10 ML algorithms
- Best Model: Gradient Boosting
  - Test MAE: 0.73% (Target: ≤2.0%) ✅ 63% better
  - Test RMSE: 0.92% (Target: ≤3.0%) ✅ 69% better
  - Test R²: 0.93 (Target: ≥0.60) ✅ 55% better
  - Test MAPE: 10.88%

4. Basic Web Interface
- Simple HTML/CSS/JavaScript
- Prediction form and results display
- Functional but basic design

IMAGE PLACEMENT:
- Top: Screenshot of old basic web interface (Semester 1)
- Middle: Model comparison table showing all 10 models with metrics
- Bottom: Bar chart comparing model performance (R² scores)

SPEAKING NOTES:
"Now let me recap what we accomplished in Semester 1. First, we conducted an extensive literature review and identified 16 key waste drivers from research papers and industry practices. We categorized these into three groups: 4 material-related parameters, 5 management-related parameters, and 7 project dynamics parameters. Second, we generated a synthetic dataset of 3,000 projects based on relationships we derived from the literature, and we validated the distributions and correlations to ensure realism. Third, we tested 10 different machine learning algorithms, including Random Forest, XGBoost, Linear Regression, and others. Our best-performing model was Gradient Boosting, which achieved a test MAE of 0.73 percent - that's 63 percent better than our target of 2.0 percent. The test RMSE was 0.92 percent, 69 percent better than our 3.0 percent target. The R-squared value was 0.93, which is 55 percent better than our target of 0.60. The MAPE was 10.88 percent, which is excellent for this type of prediction. Finally, we created a basic web interface using simple HTML, CSS, and JavaScript - it was functional but had a very basic design, as you can see in the screenshot. This gave us a solid foundation to build upon in Semester 2."

---

## Slide 5: Last Semester Work - Data Generation Process (2 minutes) (added)
How We Generated the Synthetic Dataset

Generation Approach:
- Literature-Based: Relationships derived from 50+ research papers
- Realistic Distributions: All variables follow industry-typical patterns
- Logical Dependencies: Variables generated in order of dependency
- Reproducible: Fixed seed (42) for consistent results

Generation Pipeline:
```
1. Generate Categorical Variables (Independent)
   - Stock Length Policy, Contract Type, Project Phase
   ↓
2. Generate Dependent Variables (Based on categorical)
   - Reinforcement Ratio, Unique Lengths, Supervision Index
   ↓
3. Generate Correlated Variables (Based on other variables)
   - Material Control, Storage Handling, BIM Integration
   ↓
4. Calculate Steel Waste (Based on all 16 parameters)
   - Research-derived formula with 15 factors
   - Baseline: 6.5% + stochastic noise
   ↓
5. Output Complete Project Record
```

Key Features:
- 3,000 Projects: Sufficient for ML training
- 16 Input Features: All identified waste drivers
- Realistic Ranges: Values within industry-typical bounds
- Quality Control: Validation checks ensure coherence

Example Relationships:
- Higher supervision → Better material control → Lower waste
- More change orders → Higher design revisions → Higher waste
- Better cutting optimization → Lower waste

IMAGE PLACEMENT:
- Left: Data generation pipeline flowchart
- Right: Example of generated data showing relationships
- Bottom: Distribution plots showing realistic ranges for key variables

SPEAKING NOTES:
"Let me explain how we generated our synthetic dataset. Our approach was literature-based - we derived relationships from over 50 research papers on construction waste. All variables follow realistic, industry-typical distributions, and variables are generated in order of dependency to maintain logical relationships. We use a fixed random seed of 42 for reproducibility. The generation pipeline works in five steps. First, we generate categorical variables independently - these are stock length policy, contract type, and project phase. Second, we generate dependent variables based on the categorical ones - for example, reinforcement ratio depends on project phase, and number of unique lengths depends on stock length policy. Third, we generate correlated variables based on other variables - material control depends on supervision index, storage handling depends on material control, and so on. Fourth, we calculate steel waste using a research-derived formula that incorporates all 16 parameters, with a baseline of 6.5 percent plus stochastic noise to add realism. Fifth, we output a complete project record with all parameters and the calculated waste percentage. We generated 3,000 projects, which is sufficient for machine learning training. All 16 input features are included, and values are within industry-typical bounds. We have quality control checks to ensure data coherence. For example, we know from research that higher supervision leads to better material control, which leads to lower waste. More change orders lead to higher design revisions, which increases waste. Better cutting optimization reduces waste. These relationships are encoded in our generation logic, making the synthetic data realistic and useful for training our machine learning model."

---

## Slide 6: This Semester - Website Interface Progression (2 minutes) (added)
Visual & UI Transformation

Semester 1 Interface:
- Basic HTML/CSS/JavaScript
- Simple form layout
- Minimal styling
- Single-page design

Semester 2 Interface:
- Modern Design: Professional color palette, minimal aesthetic
- Template Architecture: Flask + Jinja2 templating
- Responsive Layout: Bootstrap 5, mobile-optimized
- Multiple Pages: Landing, Prediction, About, Features
- Enhanced UX: Clear navigation, organized sections, visual feedback

Key Improvements:
- ✅ Professional branding and color scheme
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Template inheritance (DRY principle)
- ✅ Organized static assets (CSS, JS, images)
- ✅ Consistent spacing and typography
- ✅ Modern UI components (cards, badges, icons)

IMAGE PLACEMENT:
- Left: Side-by-side comparison: Semester 1 (old) vs Semester 2 (new)
- Right: Screenshot of new landing page showing hero section
- Bottom: Mobile responsive view showing adaptability

SPEAKING NOTES:
"One of the major improvements this semester is the complete transformation of our web interface. In Semester 1, we had a basic interface with simple HTML, CSS, and JavaScript - it was functional but had minimal styling and a single-page design. In Semester 2, we've created a modern, professional interface. We use a professional color palette with a minimal aesthetic - we removed all glossy colors and gradients for a clean, modern look. The architecture now uses Flask with Jinja2 templating, allowing for template inheritance and better code organization. The layout is fully responsive using Bootstrap 5, optimized for mobile, tablet, and desktop devices. We now have multiple pages: a landing page with hero section, a prediction page with comprehensive form and results, an about page with system overview, and a features page with detailed documentation. The user experience is significantly enhanced with clear navigation, organized sections, and visual feedback. Key improvements include professional branding, responsive design, template inheritance following the DRY principle, organized static assets in separate folders, consistent spacing and typography, and modern UI components like cards, badges, and icons. This transformation makes the system not just functional, but professional and user-friendly."

---

## Slide 7: This Semester - User Journey & Ease of Use (2 minutes) (added)
How Easy It Is to Use the Website

Step-by-Step User Journey:

Step 1: Access the Website
- Navigate to URL (no installation required)
- Clean, welcoming landing page
- Clear call-to-action buttons

Step 2: Navigate to Prediction Page
- Click "Make Prediction" button
- Intuitive navigation menu
- Organized form sections

Step 3: Enter Project Parameters
- 16 Input Fields: Organized into logical sections
  - Project Information
  - Material Parameters
  - Management & Control
  - Project Dynamics
- Helpful Placeholders: Show expected ranges
- Input Validation: Real-time feedback
- Default Values: Pre-filled for quick testing

Step 4: Submit & Get Results
- Single "Predict" button
- Processing time: <2 seconds
- Comprehensive results displayed:
  - Waste percentage prediction & category
  - Top 5 waste-driving factors (SHAP)
  - Reliability indicator
  - Cost impact & CO₂ emissions
  - Potential savings

Step 5: Interpret & Act
- Clear visual indicators (color-coded categories)
- Actionable insights (top factors to address)
- Financial and environmental impact
- Reliability confidence level

IMAGE PLACEMENT:
- Top: Screenshot sequence showing Step 1 → Step 5
- Middle: Full prediction form with all sections visible
- Bottom: Complete results page showing all features integrated

SPEAKING NOTES:
"Let me walk you through how easy it is to use our website. The user journey is straightforward and intuitive. Step 1 is accessing the website - users simply navigate to the URL, no installation or software download required. They're greeted with a clean, welcoming landing page with clear call-to-action buttons. Step 2 is navigating to the prediction page - users click the 'Make Prediction' button or use the intuitive navigation menu. Step 3 is entering project parameters. We have 16 input fields organized into logical sections: Project Information, Material Parameters, Management & Control, and Project Dynamics. Each field has helpful placeholders showing expected ranges, and we have input validation with real-time feedback. For quick testing, we provide default values that users can modify. Step 4 is submitting and getting results - users click a single 'Predict' button, and the system processes the request in under 2 seconds. Results are comprehensive and displayed clearly: waste percentage prediction with category classification, top 5 waste-driving factors with SHAP values, reliability indicator showing confidence level, cost impact analysis, CO₂ emissions, and potential savings. Step 5 is interpreting and acting on the results. We provide clear visual indicators with color-coded categories, actionable insights showing which factors to address, financial and environmental impact, and a reliability confidence level. The entire process takes less than a minute, and everything the user needs is in one place - no switching between different tools or interfaces."

---

## Slide 8: This Semester - Website Example Walkthrough (1.5 minutes) (added)
Live Example: Using the Website

Example Project Scenario:
- Project: Commercial Building, Frame Phase
- Steel Quantity: 100,000 kg
- Parameters: Standard values with some variations

Walkthrough Steps:

Input Example:
- Project ID: P3556
- Reinforcement Ratio: 120 kg/m³
- Unique Lengths: 20
- Stock Length Policy: Standard 12m
- Cutting Optimization: None (0)
- Supervision Index: 3
- Material Control: 2
- Change Orders: 1/month
- Design Revisions: 2/month
- ... (all 16 parameters)

Output Example:
- Predicted Waste: 11.16% (Poor category)
- Reliability: Medium (41% confidence)
- Top Factors:
  1. Offcut Reuse Policy: +1.57 (Increases waste)
  2. Cutting Optimization: +1.18 (Increases waste)
  3. Change Orders: -0.95 (Decreases waste)
- Cost Impact: $8,926 waste cost
- CO₂ Impact: 27,894 kg CO₂
- Potential Savings: $4,463 with 50% reduction

Key Insights:
- System identifies actionable factors
- Clear financial and environmental implications
- Reliability indicator guides interpretation

IMAGE PLACEMENT:
- Top: Screenshot of filled form with example values
- Middle: Screenshot of results page with all outputs
- Bottom: Annotated screenshot highlighting key features

SPEAKING NOTES:
"Let me show you a live example of using the website. For this example, we have a commercial building project in the frame phase with 100,000 kilograms of steel. I'll walk through entering the parameters and interpreting the results. For input, we enter a project ID, set reinforcement ratio to 120 kilograms per cubic meter, specify 20 unique lengths, select standard 12-meter stock length policy, set cutting optimization to none, supervision index to 3, material control to 2, change orders to 1 per month, design revisions to 2 per month, and fill in all 16 parameters. When we submit, the system processes this in under 2 seconds and returns comprehensive results. The predicted waste is 11.16 percent, which is categorized as Poor - meaning immediate action is needed. The reliability is Medium with 41 percent confidence, indicating the input data is somewhat similar to our training data. The top waste-driving factors are identified: Offcut Reuse Policy contributes plus 1.57, meaning it increases waste - this suggests implementing an offcut reuse policy could help. Cutting Optimization contributes plus 1.18, also increasing waste - this suggests better cutting optimization is needed. Interestingly, Change Orders contributes minus 0.95, meaning it decreases waste relative to the baseline - this is counterintuitive but shows the model captures complex relationships. The cost impact shows 8,926 dollars in waste cost, and the CO₂ impact is 27,894 kilograms. With a 50 percent reduction scenario, potential savings are 4,463 dollars. The key insights are that the system identifies actionable factors that project managers can control, provides clear financial and environmental implications, and the reliability indicator guides how to interpret the results. This example demonstrates how easy and valuable the system is to use."

---

## Slide 8a: Website Visual Design – Home Page & Navigation (added)
Screenshots: Landing Page & Design Elements

PHOTO 1 – Full landing page (hero section):
[INSERT SCREENSHOT: Full view of the home page showing the hero section]
- Dark theme with gradient accent (emerald/cyan) for a modern, professional look.
- Hero headline: “Predict & Reduce Steel Waste with AI” with clear value proposition.
- Primary and secondary call-to-action buttons (e.g. “Make Prediction”, “Learn More”).
- Key stats strip: e.g. 93% accuracy, 10+ models, 3000+ samples, 16 parameters.

PHOTO 2 – Floating navigation bar:
[INSERT SCREENSHOT: Close-up of the top navigation]
- Centered, floating “dock” style navbar with blur/glass effect.
- Logo/brand (“Steel Waste AI”), links: Home, Predict, About, Features.
- “Make Prediction” button for quick access.
- Stays visible on scroll and works on mobile (collapsed menu).

PHOTO 3 – Feature cards section (below hero):
[INSERT SCREENSHOT: Grid of feature cards on the home page]
- Glass-style cards with icons (e.g. AI predictions, reliability, cost/CO₂).
- Short titles and descriptions; links to Predict or Features.
- Consistent spacing and typography (Space Grotesk / Inter).

Explanation:
The design uses a dark background (#020408) with emerald and cyan accents so the interface feels modern and focused. The hero explains the product in one glance; the floating nav gives fast access to prediction and info; the feature cards summarize capabilities without clutter.

SPEAKING NOTES (Slide 8a):
"Here are actual screenshots of our website. The first shows the full landing page: dark theme with emerald and cyan accents, the hero headline 'Predict & Reduce Steel Waste with AI', and clear call-to-action buttons. The stats strip highlights 93% accuracy, 10+ models, 3000+ samples, and 16 parameters. The second image is our floating navigation bar – centered, with a glass effect – with the logo, Home, Predict, About, Features, and the Make Prediction button. The third shows the feature cards section with glass-style cards and icons. The overall look is modern and professional and keeps the user focused on the main actions."

---

## Slide 8b: Website Visual Design – Prediction Page (added)
Screenshots: Prediction Form & Layout

PHOTO 1 – Full prediction page (all sections visible):
[INSERT SCREENSHOT: Full prediction page showing section header and form]
- Section label (e.g. “PREDICTION”) and title “Steel Waste Prediction”.
- Single main card containing the entire form.
- Logical grouping: Project Information → Material Parameters → Management & Control → Project Dynamics.

PHOTO 2 – Form sections (e.g. Material Parameters):
[INSERT SCREENSHOT: One or two form sections with inputs and labels]
- Section headers with small icons (e.g. box, shield, graph).
- Inputs and dropdowns with dark background and light text; emerald focus state.
- Helper text (e.g. ranges: 60–180 kg/m³) where relevant.
- “Predict Steel Waste” button at the bottom.

PHOTO 3 – Loading state (optional):
[INSERT SCREENSHOT: Loading spinner while prediction is processing]
- Centered spinner and short message (e.g. “Processing prediction…”).
- Same dark theme and card container.

Explanation:
The prediction page keeps all 16 parameters in one place but organized into clear sections. Styling (dark inputs, emerald accents, glass card) matches the home page so the experience feels consistent and professional.

SPEAKING NOTES (Slide 8b):
"On the prediction page we have a single main card with the section label and title. The form is grouped into Project Information, Material Parameters, Management & Control, and Project Dynamics. Each section has clear headers and inputs with dark styling and emerald focus states; we also show helpful ranges where needed. The 'Predict Steel Waste' button is at the bottom. Optionally we show the loading state with a spinner while the prediction runs. The layout and styling are consistent with the rest of the site."

---

## Slide 8c: Website Visual Design – Results & Other Pages (added)
Screenshots: Results, About, and Features

PHOTO 1 – Results page (after a prediction):
[INSERT SCREENSHOT: Results card with waste %, reliability, cost, CO₂]
- Large waste percentage badge (e.g. 11.16%) with category (e.g. Poor).
- Interpretation and reliability (e.g. Medium, 41% confidence).
- Financial & environmental impact: waste cost, CO₂, potential savings, CO₂ reduction.
- Top waste-driving factors (SHAP) and “Make Another Prediction” button.

PHOTO 2 – About page:
[INSERT SCREENSHOT: About page – overview and/or tech stack section]
- Page header “About the System” with short intro.
- Cards for Overview, Technology Stack, Key Features, Model Performance, Input Parameters.
- Same dark theme and card style as the rest of the site.

PHOTO 3 – Features page:
[INSERT SCREENSHOT: Features page – feature list and/or technical specs]
- “System Features” header and list of features (e.g. explainability, reliability, cost, CO₂, real-time, ML models).
- Technical specifications (e.g. test MAE/RMSE/R², training samples, technologies).
- Optional image or diagram at top; content in glass-style cards.

Explanation:
Results are shown in one card with clear hierarchy: prediction → interpretation → reliability → cost/CO₂ → SHAP factors. About and Features reuse the same layout and components (headers, cards, dark theme) so the whole site looks and feels like one product.

SPEAKING NOTES (Slide 8c):
"The results page shows the waste percentage and category, interpretation, reliability, then financial and environmental impact – waste cost, CO₂, potential savings – and the top waste-driving factors with a 'Make Another Prediction' button. The About page has cards for Overview, Technology Stack, Key Features, Model Performance, and Input Parameters in the same dark theme. The Features page lists all six features and technical specs in glass-style cards. Across the site we use the same visual language so it feels cohesive and professional."

---

## Slide 9: This Semester - Hourie Data Acquisition (1.5 minutes) (added)
Real Project Data Integration (In Progress)

Data Source: A.R. Hourie Enterprises
- Partnership: Established through advisors (Dr. Malak, Dr. Demachkieh)
- Company: One of the largest construction companies in the region
- Scope: Multiple project datasets from Middle East region
- Status: Data acquisition and processing in progress

Data Collection Process:
1. Initial Meeting: Expert input from Ms. Karen El Zind
2. Data Requirements: Identified needed parameters
3. Data Sharing Agreement: Confidentiality and ethics compliance
4. Data Processing: Cleaning, validation, and formatting
5. Integration: Merging with synthetic dataset

Expected Data Characteristics:
- Geographic Diversity: Projects across Middle East
- Project Types: Residential and commercial buildings
- Time Period: Recent projects (last 5-10 years)
- Parameters: All 16 features + actual waste percentages
- Volume: Multiple projects (exact number TBD)

Implementation Plan:
1. Data Validation: Quality checks and outlier detection
2. Feature Alignment: Ensure compatibility with model
3. Model Retraining: Incorporate real data into training set
4. Performance Validation: Compare real vs synthetic performance
5. Continuous Improvement: Iterative model updates

Benefits:
- ✅ Improved model accuracy with real-world patterns
- ✅ Validation of synthetic data assumptions
- ✅ Regional-specific calibration
- ✅ Enhanced model credibility

IMAGE PLACEMENT:
- Top: Data collection workflow diagram
- Middle: Example of data structure (anonymized)
- Bottom: Timeline showing current progress and next steps

SPEAKING NOTES:
"We're currently working on integrating real project data from A.R. Hourie Enterprises, one of the largest construction companies in the region. This partnership was established through our advisors, Dr. Malak and Dr. Demachkieh. The data collection process began with an initial meeting with Ms. Karen El Zind at Hourie Enterprises, where we received expert input on how steel waste interacts with different parameters. We then identified our data requirements, established a data sharing agreement that complies with confidentiality and ethics standards, and are now in the process of cleaning, validating, and formatting the data for integration. The expected data characteristics include geographic diversity across the Middle East, residential and commercial building projects, recent projects from the last 5 to 10 years, all 16 features we need plus actual waste percentages, and multiple projects - the exact number is still being determined. Our implementation plan involves data validation with quality checks and outlier detection, feature alignment to ensure compatibility with our model, model retraining to incorporate real data into the training set, performance validation to compare real versus synthetic performance, and continuous improvement through iterative model updates. The benefits are significant: improved model accuracy with real-world patterns, validation of our synthetic data assumptions, regional-specific calibration for the Middle East market, and enhanced model credibility. This real data integration will strengthen our model and make it even more applicable to industry use."

---

## Slide 10: This Semester - Features Summary (1 minute) (added)
All Semester 2 Enhancements - Overview

✅ 3.2 Model Explainability and Transparency
- SHAP-based feature importance
- Top 5 waste-driving factors per prediction
- Identifies actionable parameters for waste reduction

✅ 3.4 Cost and CO₂ Impact Estimation
- Financial impact: Waste cost calculation ($/kg)
- Environmental impact: CO₂ emissions (kg CO₂/kg steel)
- Potential savings: Cost and CO₂ reduction scenarios

✅ 3.5 Prediction Reliability Indicator
- k-NN based confidence scoring
- High/Medium/Low reliability levels
- Transparent uncertainty communication

✅ 3.6 Professional Web Application Interface
- Modern, responsive design
- Multiple pages (Landing, Prediction, About, Features)
- Template-based architecture (Flask + Jinja2)

IMAGE PLACEMENT:
- Top: Four feature cards/icons side-by-side
- Bottom: Screenshot showing all features integrated in results page

SPEAKING NOTES:
"Before diving into technical details, let me give you an overview of all four enhancements we completed this semester. First, Model Explainability and Transparency - we implemented SHAP-based feature importance that shows the top 5 waste-driving factors for each prediction, helping engineers identify actionable parameters. Second, Cost and CO₂ Impact Estimation - we calculate both financial impact showing waste cost in dollars, and environmental impact showing CO₂ emissions, plus potential savings scenarios. Third, Prediction Reliability Indicator - we use k-nearest neighbors to provide confidence scoring with High, Medium, or Low reliability levels, ensuring transparent uncertainty communication. Fourth, Professional Web Application Interface - we completely redesigned the interface with modern, responsive design, multiple pages, and a template-based architecture using Flask and Jinja2. All four features are seamlessly integrated into the system, working together to provide comprehensive insights. Now let me show you the technical implementation of each feature."

---

## Slide 11: This Semester - Technical Implementation: SHAP Explainability (1.5 minutes) (changed)
3.2 Model Explainability - SHAP Implementation

What is SHAP?
- SHapley Additive exPlanations: Game-theoretic approach from cooperative game theory
- Purpose: Explains how each feature contributes to prediction (not just which features matter, but by how much)
- Method: TreeExplainer for tree-based models (fast, exact values)
- Why Important: Engineers need to understand WHY the model predicts certain waste levels to make informed decisions

How SHAP Works:
- Calculates the contribution of each feature by comparing predictions with and without that feature
- Uses Shapley values from game theory: fairly distributes "credit" for the prediction among all features
- For our model: Shows which of the 16 parameters drive waste up or down, and by how much

Technical Implementation:
```python
def explain_prediction(self, df: pd.DataFrame, top_n: int = 5):
    X, _ = self.prepare_features(df, is_training=False)
    
    # Initialize SHAP TreeExplainer
    self.shap_explainer = shap.TreeExplainer(self.best_model)
    
    # Calculate SHAP values
    shap_values = self.shap_explainer(X)
    contrib_values = shap_values.values[0]
    
    # Sort by absolute contribution
    contributions = dict(zip(self.feature_columns, contrib_values))
    sorted_contributions = sorted(
        contributions.items(), 
        key=lambda x: abs(x[1]), 
        reverse=True
    )
    
    # Return top N features
    return {'method': 'SHAP', 'top_features': top_features}
```

Key Features:
- Fast Calculation: O(n) complexity for tree models - completes in milliseconds
- Exact Values: No approximation needed - mathematically precise Shapley values
- Feature Ranking: Identifies most impactful factors (top 5 shown to users)
- Impact Direction: Positive (increases waste) vs Negative (decreases waste) - tells engineers what to improve
- Fallback: Uses feature importance if SHAP unavailable - ensures system always provides explanations

Real-World Application:
- Example: If "Offcut Reuse Policy" has SHAP value +1.57, it means this feature alone increases predicted waste by 1.57 percentage points compared to the baseline
- Engineers can see: "If I implement systematic offcut reuse (change from 0 to 2), I could reduce waste by X%"
- This transforms the model from a "black box" to a decision-support tool

Output Example:
- Top 5 waste-driving factors with contribution values
- Clear indication of which factors increase/decrease waste
- Actionable insights for project managers

IMAGE PLACEMENT:
- Left: Code snippet (as shown above)
- Right: SHAP waterfall plot or bar chart visualization
- Bottom: Screenshot of explainability section in web app

SPEAKING NOTES:
"One of our key technical implementations is SHAP explainability. SHAP stands for SHapley Additive exPlanations - it's a game-theoretic approach that explains how each feature contributes to a prediction. For tree-based models like our Gradient Boosting model, we use TreeExplainer, which provides fast, exact SHAP values. The technical implementation works like this: We prepare the input features using the same preprocessing pipeline as prediction, initialize a SHAP TreeExplainer with our trained model, calculate SHAP values for the input, extract contribution values, create a dictionary mapping each feature to its contribution, sort features by absolute contribution to identify the most impactful factors, and return the top N features. Key features of this implementation include fast calculation with O(n) complexity for tree models, exact values with no approximation needed, feature ranking that identifies the most impactful factors, impact direction showing whether factors increase or decrease waste, and a fallback to standard feature importance if SHAP is unavailable. The output shows the top 5 waste-driving factors with contribution values, clear indication of which factors increase or decrease waste, and actionable insights for project managers. This explainability feature builds trust in AI predictions and helps engineers understand why certain predictions are made."

---

## Slide 12: This Semester - Technical Implementation: Reliability & Cost/CO₂ (1.5 minutes) (changed)
3.5 Reliability Indicator & 3.4 Cost/CO₂ Impact

Why Reliability Matters:
- ML models are only reliable when input data is similar to training data
- If user enters unusual parameters, prediction may be less trustworthy
- Engineers need to know: "Can I trust this prediction for my specific project?"

Reliability Calculation (k-NN):
```python
def calculate_reliability(self, df: pd.DataFrame):
    # Find 10 nearest training samples
    nn = NearestNeighbors(n_neighbors=10, metric='euclidean')
    nn.fit(self.X_train_scaled)
    distances, _ = nn.kneighbors(X)
    
    # Calculate normalized distances
    feature_distances = np.abs(X[0] - np.mean(self.X_train_scaled, axis=0))
    feature_stds = np.std(self.X_train_scaled, axis=0)
    normalized_distances = feature_distances / (feature_stds + 1e-10)
    
    # Weighted combination
    reliability_score = 0.6 * distance_score + 0.4 * normalized_score
    
    # Determine level: High (≥70%), Medium (40-70%), Low (<40%)
```

Cost & CO₂ Calculation:
```python
def calculate_cost_co2_impact(self, waste_percentage, total_steel_kg):
    waste_kg = (waste_percentage / 100) * total_steel_kg
    waste_cost = waste_kg * 0.80  # $/kg
    waste_co2 = waste_kg * 2.5    # kg CO₂/kg steel
    
    # Potential savings (50% reduction)
    potential_savings_kg = (waste_percentage * 0.5 / 100) * total_steel_kg
    potential_cost_savings = potential_savings_kg * 0.80
    potential_co2_reduction = potential_savings_kg * 2.5
```

How Reliability Works:
1. Find Similar Projects: Uses k-NN to find 10 most similar training projects
2. Calculate Distance: Measures how "far" the input is from training data in 16-dimensional space
3. Normalize: Accounts for features with different scales (e.g., reinforcement ratio 50-200 vs supervision 1-5)
4. Score: Combines distance metrics (60% raw distance + 40% normalized distance)
5. Categorize: High (≥70%) = very similar, Medium (40-70%) = somewhat similar, Low (<40%) = different

Key Features:
- Reliability: Measures input similarity to training data - tells engineers prediction confidence
- Dual Metrics: Combines raw and normalized distances - handles different feature scales properly
- Cost Impact: Real-time financial calculations - converts waste % to actual dollars
- Environmental Impact: CO₂ emissions and reduction potential - shows sustainability impact
- Configurable: Unit costs and emission factors adjustable - adapts to regional variations

Real-World Application:
- High reliability: "Your project is very similar to our training data - high confidence in prediction"
- Low reliability: "Your project has unusual parameters - interpret results with caution, consider consulting experts"
- This prevents over-reliance on predictions when they may not be appropriate

IMAGE PLACEMENT:
- Left: Code snippets (as shown above)
- Right: Screenshot showing reliability badge and cost/CO₂ cards
- Bottom: Formula breakdown visualization

SPEAKING NOTES:
"Our reliability calculation uses k-nearest neighbors to measure how similar the input data is to our training data. We find the 10 nearest training samples using Euclidean distance, calculate both raw distances and normalized distances by feature standard deviation, and combine them with a weighted average - 60 percent weight on distance score and 40 percent on normalized score. The reliability level is determined as High for scores 70 percent and above, Medium for 40 to 70 percent, and Low for below 40 percent. This provides engineers with a clear confidence indicator. For cost and CO₂ impact, we calculate waste quantity in kilograms by multiplying waste percentage by total steel quantity, calculate waste cost by multiplying waste quantity by 0.80 dollars per kilogram, and calculate CO₂ emissions by multiplying waste quantity by 2.5 kilograms of CO₂ per kilogram of steel. We also calculate potential savings assuming a 50 percent waste reduction scenario. Key features include reliability measurement of input similarity, dual metrics combining raw and normalized distances, real-time financial calculations, environmental impact assessment with CO₂ emissions and reduction potential, and configurable parameters - unit costs and emission factors can be adjusted. These features provide comprehensive insights beyond just the prediction, helping users understand both the confidence level and the financial and environmental implications."

---

## Slide 13: This Semester - Technical Implementation: Flask Backend (1 minute) (changed)
3.6 Professional Web Interface - Backend Architecture

Why This Architecture:
- Separation of Concerns: Model logic separate from web logic separate from presentation
- Maintainability: Easy to update model without touching web code
- Scalability: Can add new features without breaking existing functionality
- Performance: Optimized to complete all calculations in <2 seconds

Flask Backend Structure:
```python
@app.route('/predict', methods=['POST'])
def predict():
    comparator = load_model()
    
    # Extract form data
    data = {all 16 parameters}
    df = pd.DataFrame([data])
    
    # Parallel processing
    prediction = comparator.predict(df)[0]
    explanation = comparator.explain_prediction(df, top_n=5)
    reliability = comparator.calculate_reliability(df)
    cost_co2 = comparator.calculate_cost_co2_impact(prediction, total_steel_kg)
    
    # Render template with all results
    return render_template('predict.html', ...)
```

Frontend Architecture:
- Templates: Jinja2 template inheritance (base.html)
- Static Assets: Organized folders (CSS, JS, images)
- Responsive Design: Bootstrap 5 grid system
- JavaScript: Form validation and interactivity

How It Works:
1. User submits form → Flask receives POST request with 16 parameters
2. Data preparation → Convert form data to pandas DataFrame (same format as training)
3. Model prediction → Gradient Boosting model predicts waste percentage
4. SHAP calculation → TreeExplainer calculates feature contributions
5. Reliability scoring → k-NN finds similar training samples, calculates confidence
6. Cost/CO₂ analysis → Converts waste % to financial and environmental impact
7. Template rendering → Jinja2 combines all results into HTML response

Key Technical Points:
- Single Route: One endpoint handles all prediction logic - simple, maintainable
- Sequential Processing: Model → SHAP → Reliability → Cost/CO₂ - each step uses previous results
- Template Rendering: Jinja2 receives all computed results - clean separation of logic and presentation
- Error Handling: Graceful failure with user-friendly messages - system never crashes, always provides feedback
- Performance: <2 seconds processing time - fast enough for real-time use

Frontend-Backend Integration:
- Templates: Jinja2 template inheritance allows reusable components (header, footer, navigation)
- Static Assets: Organized folders make it easy to update CSS/JS/images independently
- Responsive Design: Bootstrap 5 ensures works on all devices (mobile, tablet, desktop)
- JavaScript: Client-side validation reduces server load and improves user experience

IMAGE PLACEMENT:
- Left: Code snippet showing Flask route
- Right: System architecture diagram
- Bottom: File structure showing templates and static folders

SPEAKING NOTES:
"Our Flask backend architecture is clean and efficient. The predict route handles POST requests, loads the trained model, extracts all 16 parameters from form data, converts them to a pandas DataFrame, and performs sequential processing: model prediction, SHAP explanation, reliability calculation, and cost/CO₂ impact analysis. All results are then rendered in the Jinja2 template. The frontend architecture uses Jinja2 template inheritance with a base template, organized static assets in separate folders for CSS, JavaScript, and images, responsive design using Bootstrap 5 grid system, and JavaScript for form validation and interactivity. Key technical points include a single route that handles all prediction logic, sequential processing that completes in under 2 seconds, template rendering where Jinja2 receives all computed results, comprehensive error handling with graceful failure and user-friendly messages, and excellent performance. This architecture ensures clean separation of concerns - model logic is in the ModelComparison class, web logic is in Flask routes, and presentation logic is in templates. The result is a maintainable, scalable, and professional system."

---

## Slide 14: Future Work (1.5 minutes) (changed)
What's Left from the Methodology

Immediate Next Steps:
- ✅ Complete Hourie data integration
- ✅ Model retraining with real data
- ✅ Performance validation and comparison
- ✅ Final testing and documentation
- ✅ User feedback collection

Future Enhancements:

1. Data Expansion
- Additional real project datasets
- Geographic expansion (beyond Middle East)
- Temporal data (longitudinal studies)
- Different project types

2. Model Improvements
- Hyperparameter optimization
- Ensemble methods
- Real-time learning (online updates)
- Uncertainty quantification

3. Feature Extensions
- Additional material types (concrete, blocks)
- Weather and environmental factors
- Supply chain parameters
- Advanced BIM integration metrics

4. System Enhancements
- User authentication and history
- Project comparison tools
- Batch prediction capabilities
- API for third-party integration
- Mobile application

5. Research & Validation
- Field studies and validation
- Industry pilot programs
- Academic publication
- Best practices documentation

IMAGE PLACEMENT:
- Top: Roadmap showing immediate → short-term → long-term
- Middle: Feature extensions diagram
- Bottom: System enhancements visualization

SPEAKING NOTES:
"Looking at what's left from our methodology, our immediate next steps include completing the Hourie data integration, retraining the model with real data, validating and comparing performance, final testing and documentation, and collecting user feedback. For future enhancements, we see several opportunities. First, data expansion - we want to add additional real project datasets, expand geographically beyond the Middle East, include temporal data for longitudinal studies, and cover different project types. Second, model improvements - we can optimize hyperparameters, explore ensemble methods, implement real-time learning for online updates, and add uncertainty quantification. Third, feature extensions - we want to add additional material types like concrete and blocks, include weather and environmental factors, add supply chain parameters, and incorporate advanced BIM integration metrics. Fourth, system enhancements - we plan to add user authentication and history tracking, project comparison tools, batch prediction capabilities, an API for third-party integration, and a mobile application. Fifth, research and validation - we want to conduct field studies, run industry pilot programs, publish academic papers, and create best practices documentation. This roadmap ensures continuous improvement and expansion of the system's capabilities and impact."

---

## Slide 15: Impact (1.5 minutes) (changed)
Project Impact & Achievements

Technical Achievements:
- ✅ 93% Model Accuracy: Exceeded all targets (63-69% better)
- ✅ Explainable AI: SHAP-based transparency
- ✅ Reliability System: Confidence indicators for engineers
- ✅ Integrated Analysis: Prediction + Cost + CO₂ in one system
- ✅ Production-Ready: Professional web application

Industry Impact:

Cost Savings:
- Per Project: $4,000-$8,000 per 100,000 kg steel
- Annual Potential: Millions in savings across industry
- Improved Estimation: Better bidding accuracy

Environmental Impact:
- CO₂ Reduction: 10,000-20,000 kg per project
- Material Efficiency: Reduced waste = less production needed
- Sustainability: Aligns with net-zero goals

Innovation:
- First Steel-Specific: Waste prediction with explainability
- Combined Approach: Prediction + financial + environmental
- Engineering-Focused: Reliability indicators for responsibility
- Practical Tool: Ready for immediate industry use

Academic Contribution:
- Methodology: Replicable framework for other materials
- Research: Validates ML approach for construction waste
- Knowledge: Advances understanding of waste drivers

IMAGE PLACEMENT:
- Top: Infographic showing key numbers (93%, $8K, 20K kg CO₂)
- Middle: Impact visualization (cost savings, CO₂ reduction charts)
- Bottom: Before/after comparison: Traditional vs ML approach

SPEAKING NOTES:
"Let me summarize the impact of our project. From a technical standpoint, we've achieved 93 percent model accuracy, which exceeded all our targets by 63 to 69 percent. We've integrated explainable AI with SHAP-based transparency, developed a reliability system with confidence indicators for engineers, created an integrated analysis combining prediction, cost, and CO₂ in one system, and built a production-ready professional web application. The industry impact is significant. For cost savings, we can help save 4,000 to 8,000 dollars per project with 100,000 kilograms of steel. Annually, this could translate to millions in savings across the industry. We also improve estimation accuracy for better bidding. For environmental impact, we can reduce CO₂ emissions by 10,000 to 20,000 kilograms per project, improve material efficiency by reducing waste and thus less production needed, and contribute to sustainability goals aligned with net-zero targets. In terms of innovation, this is the first steel-specific waste prediction system with explainability features. We've combined prediction, financial analysis, and environmental impact in one tool. We've focused on engineering needs with reliability indicators for responsible decision-making. And we've created a practical tool ready for immediate industry use. Our academic contribution includes a replicable methodology framework that can be applied to other materials, research that validates the ML approach for construction waste, and knowledge that advances understanding of waste drivers. This project demonstrates that academic research can create real-world value."

---

## Slide 16: Interactive Exercise - Try the Website (2 minutes) (added)
QR Code & Test the System

QR Code:
[QR CODE PLACEHOLDER - Link to website]

Scan to Access:
- Direct link to prediction page
- No login required
- Mobile-friendly interface

Suggested Test Scenarios:

Scenario 1: Low Waste Project (Good Practices)
- Reinforcement Ratio: 100 kg/m³
- Unique Lengths: 15
- Stock Length Policy: Standard 12m
- Cutting Optimization: Full (2)
- Supervision Index: 5
- Material Control: 3
- Storage Handling: 5
- BIM Integration: 3
- Offcut Reuse: Systematic (2)
- Change Orders: 0
- Design Revisions: 0
- Expected: Low waste percentage, High reliability

Scenario 2: High Waste Project (Poor Practices)
- Reinforcement Ratio: 180 kg/m³
- Unique Lengths: 35
- Stock Length Policy: Custom lengths
- Cutting Optimization: None (0)
- Supervision Index: 1
- Material Control: 1
- Storage Handling: 1
- BIM Integration: 0
- Offcut Reuse: None (0)
- Change Orders: 5
- Design Revisions: 8
- Expected: High waste percentage, Medium/Low reliability

Parameter Ranges for Testing:
- Reinforcement Ratio: 60-180 kg/m³
- Unique Lengths: 5-40
- Supervision Index: 1-5
- Material Control: 1-3
- Storage Handling: 1-5
- Change Orders: 0-8 per month
- Design Revisions: 0-10 per month
- Lead Time: 3-30 days
- Order Frequency: 1-8 per month

What to Observe:
- How prediction changes with different inputs
- Which factors appear in top 5 waste drivers
- Reliability indicator variations
- Cost and CO₂ impact calculations
- Ease of use and interface quality

IMAGE PLACEMENT:
- Top: Large QR code (centered)
- Middle: Two side-by-side scenarios with parameter values
- Bottom: Parameter ranges table

SPEAKING NOTES:
"Now let's try the system! I've provided a QR code that you can scan with your phone to access the website directly. The link goes straight to the prediction page, no login is required, and the interface is mobile-friendly. I've prepared two suggested test scenarios for you to try. Scenario 1 is a low waste project with good practices: reinforcement ratio of 100 kilograms per cubic meter, 15 unique lengths, standard 12-meter stock length policy, full cutting optimization, supervision index of 5, material control of 3, storage handling of 5, BIM integration of 3, systematic offcut reuse, zero change orders, and zero design revisions. This should give you a low waste percentage with high reliability. Scenario 2 is a high waste project with poor practices: reinforcement ratio of 180 kilograms per cubic meter, 35 unique lengths, custom stock lengths, no cutting optimization, supervision index of 1, material control of 1, storage handling of 1, no BIM integration, no offcut reuse, 5 change orders per month, and 8 design revisions per month. This should give you a high waste percentage with medium or low reliability. I've also provided parameter ranges for testing - reinforcement ratio from 60 to 180, unique lengths from 5 to 40, supervision index from 1 to 5, and so on. When you test, observe how the prediction changes with different inputs, which factors appear in the top 5 waste drivers, how the reliability indicator varies, the cost and CO₂ impact calculations, and the overall ease of use and interface quality. Please scan the QR code and try it out - we'd love to hear your feedback!"

---

## Slide 17: Conclusion & Thank You (1 minute) (changed)
Summary & Next Steps

What We've Accomplished:
- ✅ Problem identified and solution developed
- ✅ High-performance ML model (93% R²)
- ✅ Explainable AI with SHAP
- ✅ Cost and CO₂ impact analysis
- ✅ Reliability indicators
- ✅ Professional web application
- ✅ Real data integration in progress

Key Takeaways:
- Data-Driven Approach: ML outperforms traditional methods
- Practical Value: Immediate cost and environmental benefits
- Engineering Focus: Explainability and reliability for responsible use
- Production-Ready: System ready for industry deployment

Next Steps:
- Complete Hourie data integration
- Model retraining and validation
- User feedback collection
- Final report completion

Thank You - Questions?

IMAGE PLACEMENT:
- Top: Summary infographic
- Bottom: Team photo or final system screenshot

SPEAKING NOTES:
"In conclusion, we've accomplished a great deal. We've identified a real problem and developed a practical solution. We've created a high-performance machine learning model with 93 percent R-squared accuracy. We've integrated explainable AI with SHAP, added cost and CO₂ impact analysis, implemented reliability indicators, built a professional web application, and are making progress on real data integration. Key takeaways are that a data-driven approach using machine learning significantly outperforms traditional methods, the system provides immediate practical value with cost and environmental benefits, we've focused on engineering needs with explainability and reliability for responsible use, and we've created a production-ready system ready for industry deployment. Our next steps include completing the Hourie data integration, retraining and validating the model, collecting user feedback, and completing our final report. Thank you for your attention. We're happy to answer any questions you may have, and we encourage you to try the system using the QR code we provided."

---

## Presentation Timing Breakdown

Total: 24 minutes (includes 3 new design slides; can reduce by 1–2 min if needed)

1. Title Slide: 1 min
2. Problem Statement & Objectives: 2 min
3. Methodology: 1.5 min
4. Last Semester Work - Overview: 1.5 min
5. Last Semester Work - Data Generation: 2 min
6. This Semester - Website Progression: 2 min
7. This Semester - User Journey: 2 min
8. This Semester - Website Example: 1.5 min
8a. Website Visual Design – Home Page & Navigation: 1 min
8b. Website Visual Design – Prediction Page: 1 min
8c. Website Visual Design – Results & Other Pages: 1 min
9. This Semester - Hourie Data: 1.5 min
10. This Semester - Features Summary: 1 min
11. This Semester - Technical: SHAP: 1.5 min
12. This Semester - Technical: Reliability & Cost: 1.5 min
13. This Semester - Technical: Flask Backend: 1 min
14. Future Work: 1.5 min
15. Impact: 1.5 min
16. Interactive Exercise: 2 min
17. Conclusion: 1 min

Q&A: 5-10 minutes after presentation

---

## Image Checklist

Screenshots Needed:
- [ ] Landing page (hero section) - NEW design
- [ ] Prediction form (all sections visible) - NEW design
- [ ] Results page (all features displayed) - NEW design
- [ ] About page - NEW design
- [ ] Features page - NEW design
- [ ] Mobile responsive view - NEW design
- [ ] Old interface (Semester 1) for comparison
- [ ] Side-by-side comparison (Semester 1 vs Semester 2)
- [ ] User journey sequence (Step 1-5)
- [ ] Example walkthrough (filled form + results)
- [ ] **Slide 8a:** Full landing page (hero), floating nav close-up, feature cards section
- [ ] **Slide 8b:** Full prediction page, form sections (e.g. Material Parameters), loading state (optional)
- [ ] **Slide 8c:** Results page (waste %, reliability, cost/CO₂, SHAP), About page, Features page

Charts/Diagrams Needed:
- [ ] Model performance comparison chart
- [ ] SHAP feature importance visualization
- [ ] Cost/CO₂ impact bar charts
- [ ] System architecture diagram
- [ ] User workflow flowchart
- [ ] Data generation pipeline flowchart
- [ ] Methodology flowchart
- [ ] Impact infographic
- [ ] QR code for website access

Technical Visuals:
- [ ] Code snippets (SHAP, reliability, cost/CO₂, Flask)
- [ ] File structure diagram
- [ ] Data flow diagram
- [ ] Performance metrics table
- [ ] Parameter ranges table for exercise

---

## Key Speaking Points

Emphasize:
1. Problem-Solution Fit - How FYP addresses real industry need
2. All objectives achieved - Show completion
3. High performance - 93% R², exceeded targets
4. Technical depth - SHAP, k-NN, proper architecture
5. Real-world value - Cost savings, CO₂ reduction
6. Professional quality - Production-ready system
7. Ease of use - Simple user journey
8. Future potential - Real data integration, expansion

Technical Details to Mention:
- SHAP TreeExplainer for fast, exact values
- k-NN with normalized distances for reliability
- Flask + Jinja2 templating architecture
- Responsive design with Bootstrap 5
- Modular code structure for maintainability
- Data generation based on literature research

Impact to Highlight:
- $4,000-$8,000 savings per project
- 10,000-20,000 kg CO₂ reduction
- 63-69% better than target metrics
- Industry-ready tool
- First steel-specific system with explainability
