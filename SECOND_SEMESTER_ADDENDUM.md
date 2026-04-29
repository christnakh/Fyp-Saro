# Second Semester — System Extension and Implementation

## How to use this document in the main report

**Balance of this chapter:** Roughly **half** of the substance is written as **continuous paragraphs** (argument, context, and interpretation), and **half** as **bullet lists or tables** (deliverables, steps, and scannable facts). Sections deliberately **alternate** prose and lists so the report is neither a wall of bullets nor an uninterrupted essay.

This addendum is for the **main body** of the report: paste **from §1 onward** **after the Concept Summary** and **before** “Background and Project Objectives.” Do **not** park this chapter only at the very end of the document after References unless an instructor requires it.

**Submission reminders:**

- Add a **Table of Contents** line for *Second Semester: System Extension and Implementation* at that early position and fix page numbers when final.
- Keep **`TECHNICAL_APPENDIX_FULL.md`** with the **rear** materials (full API tables, file tree, extra examples); this file is the **readable** implementation chapter.

**Word export:** Regenerate **`SECOND_SEMESTER_ADDENDUM.docx`** with `python3 scripts/md_addendum_to_docx.py` after edits (`pip install python-docx`).

---

## 1. Introduction and motivation

### 1.1 Why a second-semester extension?

The first semester proved that a **data-driven** approach could estimate steel waste from project attributes. Concretely, the group produced:

- A **literature-grounded synthetic dataset** and generator code (`synthetic_data_generator.py`).
- A **multi-model comparison** with cross-validation and a held-out test split.
- A **selected regressor** (Gradient Boosting under the preliminary evaluation protocol).
- An **initial web interface** that exposed predictions to non-programmers.

Those outcomes answered whether the **prediction problem** was tractable on synthetic data. They did not yet answer whether the tool would be **trusted**, **interpretable**, and **actionable** in estimating and tendering workflows, where a naked percentage is rarely enough.

Experienced engineers and estimators routinely ask **why** a forecast took a given value, whether the case lies **inside or outside** the experience reflected in training, and how the result translates into **cash and embodied carbon** once steel tonnage is known. They also need software that can be **marked**, **demonstrated**, and eventually **hosted** without requiring every stakeholder to install Python. The written brief for this phase is **`extension`** (*Deployment and Enhancement of a Data-Driven Steel Waste Prediction System*). The implementation work concentrated on four themes—**transparent explanations**, **honest reliability signalling**, **cost and CO₂ translation**, and a **maintainable Flask stack with JSON API**—while keeping the same underlying feature set and synthetic training philosophy as semester one. The sections below map each theme to **`model.py`**, **`app.py`**, and the `templates/` / `static/` assets so the report text and the submitted repository stay aligned.

### 1.2 What we set out to build (high level)

Semester two was not meant to discard the regression formulation from semester one; it was meant to **wrap** it in a clearer **decision-support layer**. The table below states the five headline goals in compact form. In prose, the team aimed to keep **waste percentage** as the model target, add **per-prediction explanations** (SHAP when possible, otherwise feature importance), warn users when inputs sit in **unfamiliar regions** of feature space, attach **USD and kg CO₂** using user-supplied total steel mass and documented default factors, and expose the same logic through **HTML pages and `/api/predict`** so demos and integration tests do not depend on manual form entry alone.

| Goal | Idea |
|------|------|
| Transparency | Show which inputs push the prediction up or down for the case at hand. |
| Accountability | Indicate whether the case resembles the data the model learned from. |
| Impact | Translate % waste into money and emissions using user-supplied tonnage. |
| Access | One web UI plus a JSON API implementing the same pipeline. |
| Deployability | Flask application suitable for lab or cloud hosting. |

Later sections unpack each column of that table with alternating explanation and lists, then tie the behaviour to specific functions and routes in the codebase.

---

## 2. System architecture — how the pieces connect

### 2.1 End-to-end flow

Industrial machine-learning systems usually **separate training from serving** so that interactive use stays fast and the trained artefact is **versioned**. This project follows the same idea: batch jobs create data and a pickle; the web process only loads and runs inference.

- **Data generation** — `generate_train_test_data.py` drives `SteelWasteDataGenerator`, writes `train_data.csv` / `test_data.csv` (default **80/20** split, fixed seed), plus `full_dataset.csv` for checks.
- **Model development** — `ModelComparison` in `model.py` fits encoders and scaler, compares **ten** regressors, serialises the **best** model with **`X_train_scaled`** to `models/best_steel_waste_model.pkl`, and can export metrics for report tables.
- **Runtime** — `app.py` loads the pickle **once**, builds one-row DataFrames from the form or JSON, and calls **predict**, **explain_prediction**, **calculate_reliability**, and **calculate_cost_co2_impact** (using **total steel kg** from the user).

Between those stages, **no web server is required** to regenerate CSVs or retrain. Serving reuses **one** preprocessing path for the form and the API, which limits training–serving skew. Embedding **`X_train_scaled`** in the pickle supports **distance-based reliability** without always copying the full training file to every laptop; older bundles without that array may fall back to reading `train_data.csv` when the loader allows it.

### 2.2 Main files and roles

Clean separation between **learning** and **presentation** was a design goal: all numerical and sklearn-dependent logic should live where it can be tested without HTTP, and all request parsing should stay thin.

| File / folder | Role |
|----------------|------|
| `model.py` | Preprocess, train, compare, save/load, predict, explain, reliability, cost/CO₂. |
| `app.py` | Routes, form/JSON → DataFrame mapping, templates, `/api/predict`, errors. |
| `templates/*.html` | Jinja2 pages: landing, predict, about, features, base layout. |
| `static/css`, `static/js` | Styling and minor client behaviour; **no** duplicate model maths. |
| `requirements.txt` | Pinned stack: Flask, pandas, numpy, sklearn, xgboost, shap, joblib. |

That layout means a future **retrain** after real project data arrives is mostly a **`model.py`** run and a new pickle; the Flask templates and routes can stay stable while metrics and comparisons are updated in the written report.

---

## 3. Preprocessing and prediction — how the model sees inputs

### 3.1 Why encode and scale?

Categorical fields such as stock-length policy, contract type, and construction phase are **label-encoded** into integers. Encoders are **fitted on the training split only**, so test rows and live predictions use the **same** category codes and common **label leakage** from the full population is avoided. Numeric columns are then passed through **`StandardScaler`** fit on training: subtract training mean, divide by training standard deviation. That matters both for algorithms whose behaviour depends on relative magnitudes and for **reliability**, which measures distances in the **scaled** space—without scaling, a large-range variable such as reinforcement ratio would drown out others in the neighbour calculation.

All of that is centralised in **`ModelComparison.prepare_features()`**. The **`is_training`** flag distinguishes **fit** from **transform**. One implementation path feeds batch evaluation on `test_data.csv`, the browser form, and **`/api/predict`**, which keeps behaviour consistent across entry points.

### 3.2 Feature set (what enters the model)

The regressor reads **fifteen** columns aligned with `train_data.csv` (ratios, counts, management indices, procurement fields, encoded categoricals). Three special cases matter for readers of the report:

- **`project_id`** — carried for traceability, **dropped** from the feature matrix.
- **`steel_waste_percentage`** — the **target** during training; **omitted** when predicting.
- **`total_steel_kg`** — entered by the user for **cost/CO₂ only**; **not** an input to the regressor.

Conceptually the model predicts a **rate** (waste as a share of theoretical steel); mass is an **engineering multiplier** that turns that rate into **tonnes wasted**, **dollars**, and **kilograms of CO₂**, matching how estimators often combine allowances with bill-of-quantities steel.

### 3.3 Making a prediction (code path)

The HTTP handler collects fields, builds a Python **dict**, wraps **`pd.DataFrame([data])`**, and calls **`predict`**. Internally **`prepare_features`** encodes and scales; **`best_model.predict`** returns a scalar **%**. The **same** DataFrame is immediately passed to **explain** and **reliability**, so every panel on the results page refers to **one** encoded instance—there is no risk of explanation and prediction drifting because of inconsistent preprocessing.

```text
User submits form → app.py builds dict → pd.DataFrame([data])
  → comparator.predict(df)
      → prepare_features(df, is_training=False)
      → best_model.predict(X)
  → scalar waste percentage
```

Using **DataFrames** consistently also simplifies **regression tests** and defence demos: the same row shape works in notebooks, in `test_data.csv` batches, and in JSON from Postman or `curl`.

---

## 4. Model explainability — why and how

### 4.1 Why explain predictions?

A percentage on screen without context often fails the “**so what**” test in civil engineering. The extension therefore treated **interpretability** as part of the product, not an optional extra. The purpose is to support **structured conversation**—for example, whether tighter **supervision**, better **cutting optimisation**, or a stronger **offcut policy** is associated with lower predicted waste **for the scenario just entered**—in language that matches how teams already debate design and procurement.

- Focus on **this project’s** top drivers, not only global model statistics when SHAP is active.
- Show **direction** (tending to raise or lower waste) as well as **rank**.
- Record **which method** was used (`SHAP`, `Feature Importance`, or unavailable) so examiners know what they are looking at.

Those three points connect the UI to the extension’s **transparency** goal without requiring users to read the SHAP literature in full.

### 4.2 How SHAP is used (primary path)

When **SHAP** is installed and the explainer builds successfully, **`explain_prediction`** attributes the model output relative to a baseline using **Shapley values**. Tree ensembles use **TreeExplainer** for efficiency. Operationally, the **scaled** feature vector for the request is evaluated, contributions are sorted by **absolute** value, and the **top five** are rendered. **Positive** contributions are described as pushing waste **up** relative to the baseline; **negative** as pushing **down**—always as **model-internal** effects, not as literal “percentage points per bar diameter” in the physical world.

Explainers are **reconstructed after load** rather than stored inside the pickle, to limit file size and version fragility; where a kernel explainer needs a background distribution, a **random subset** of scaled training rows balances accuracy and startup time.

### 4.3 Fallback — why feature importance?

If SHAP is missing or errors at runtime, the service falls back to **tree `feature_importances_`** when available. That answers a **global** importance question rather than a full instance-level Shapley decomposition, but it preserves a usable ranked list and avoids a blank panel. The JSON and HTML still expose the **`method`** field so advanced readers can interpret the difference.

```python
# Conceptual structure returned by explain_prediction (not a verbatim copy)
{
  "method": "SHAP" | "Feature Importance" | "Not Available",
  "top_features": [{"feature": str, "contribution" or "importance": float, "impact": str}, ...],
  "all_features": { ... }
}
```

**`format_explainability_features()`** in `app.py` turns internal column names into short human labels for the list shown after each prediction.

---

## 5. Prediction reliability — why and how

### 5.1 Why a reliability indicator?

Any empirical model is only well supported **inside** the kinds of projects it saw during training. **Interpolation** near training examples is generally more defensible than **extrapolation** in corners of attribute space where few or no rows existed, even if the algorithm still returns a number. A reliability indicator cannot replace a full **validation study on real sites**, but it can state honestly that some predictions are **more anchored** in the training experience than others and can temper overconfidence when users enter extreme combinations.

- It **does not** claim calibrated **probabilities** of error.
- It **does** nudge users toward caution when the feature vector is **far** from the training cloud.
- It supports the **academic** expectation that limitations are acknowledged, not hidden.

Together, those roles align with responsible use of ML in engineering decision support.

### 5.2 How it is computed

**`calculate_reliability`** operates in the **same scaled space** as **`prepare_features`**. The logic blends two geometric ideas: proximity to real training points, and typicality of each feature relative to training means and spreads.

- Fit **k-nearest neighbours** (Euclidean) on **`X_train_scaled`** with **k = min(10, n_train)** and record mean distance to neighbours.
- Compute mean **normalised deviation** of the input from **training column means** using training standard deviations.
- Map each component to **[0, 1]** and combine **60%** neighbour score **+ 40%** typicality score into **`reliability_score`**.
- Assign **high** (≥ 0.7), **medium** (≥ 0.4), or **low** (< 0.4) with short text and colour badges in the UI.

If **`X_train_scaled`** is unavailable, the function returns **medium** reliability with an explicit message so the app keeps running and prompts regeneration of the model bundle. Implementation references: **`calculate_reliability()`** in `model.py`; colour mapping in `app.py`.

---

## 6. Cost and CO₂ impact — why and how

### 6.1 Why add economics and carbon?

Waste **percentage** is useful internally, but boards and clients often ask for **money** and **carbon**. Folding cost and CO₂ into the same workflow as the prediction reduces **manual transcription** between tools and keeps the **assumptions** (price per kg, kg CO₂ per kg steel) in **one versioned place**—the codebase—rather than in scattered spreadsheets that diverge from the model version.

### 6.2 Formulas (implemented logic)

The implementation in **`calculate_cost_co2_impact`** starts from predicted waste **w** (%) and user **M** (kg total steel). It computes waste mass, monetises it with a default **USD/kg**, multiplies by a default **CO₂ intensity** (kg CO₂ per kg steel), and derives an **illustrative savings** case by assuming waste could be cut to **half** of **w**—a **communicative** scenario, not a promise of achievability.

- **Waste mass** \((w/100) \times M\).
- **Waste cost** = mass × configurable **steel_cost_per_kg** (default in `model.py`).
- **Waste CO₂** = mass × configurable **co2_per_kg_steel** (default in `model.py`).
- **Savings block** = delta mass / cost / CO₂ between **w** and **w/2**.

Defaults are documented in the **docstring** and should be updated when the team adopts **project-specific** prices or **verified** environmental data for rebar. **`total_steel_kg`** is read from the form or JSON in **`app.py`**.

---

## 7. Web application — routes and user flow

### 7.1 Pages (GET)

The interface uses **server-side rendering** (Flask + Jinja2): one Python process, templates on disk, and no separate front-end build chain. That choice keeps **all** prediction and post-processing in one language and makes the project easier to mark in a lab environment.

| Route | Purpose |
|-------|---------|
| `/` | Landing; navigation to prediction. |
| `/predict` | Input form and results panel (results after POST). |
| `/about` | Short project context for examiners and visitors. |
| `/features` | Capability overview without running a prediction. |

### 7.2 Form POST → server render

When the user posts **`/predict`**, Flask reads each field, maps short HTML names to the **canonical** column names expected by **`prepare_features`**, and executes the same **predict → explain → reliability → cost/CO₂** chain used by the API. **`get_waste_category`** applies **Excellent / Good / …** bands from the numeric **%**; those labels are **presentation only** and do not feed back into the regressor. The response HTML includes the explainability block built by **`format_explainability_features`**. Because templates are rendered on the server, there is no risk that a stale browser script applies different formulas than the trained model on disk.

### 7.3 JSON API

**POST `/api/predict`** mirrors the form: JSON keys match training columns plus optional **`total_steel_kg`**. Successful responses bundle:

- **`predicted_waste_percentage`** and **`waste_category`**
- **`reliability`**, **`explainability`**, **`cost_co2_impact`**
- HTTP **400** with an error string when parsing or inference fails

That symmetry is intentional: integration tests and demos can bypass the browser entirely.

```bash
curl -s -X POST http://localhost:5005/api/predict \
  -H "Content-Type: application/json" \
  -d '{"reinforcement_ratio_kg_per_m3":120,"num_unique_required_lengths":20,"stock_length_policy":"standard_12m","cutting_optimization_usage":0,"bim_integration_level":0,"design_revisions_per_month":2,"supervision_index_1to5":3,"material_control_level_1to3":2,"storage_handling_index_1to5":3,"offcut_reuse_policy_0to2":0,"change_orders_per_month":1,"contract_type":"lump_sum","lead_time_days":15,"order_frequency_per_month":4,"project_phase":"frame","total_steel_kg":100000}'
```

### 7.4 Training on first run and debug route

If **`best_steel_waste_model.pkl`** is absent at startup, **`train_model_if_needed`** can train automatically **when** train and test CSVs exist—a convenience for coursework machines. For anything like **production**, the team should run **`python model.py`** explicitly, log metrics, and archive the pickle used for deployment. The **`/debug/explain`** route is **development-only** and should be **removed or locked down** before wide exposure.

---

## 8. Extension proposal vs. what was built

The **`extension`** document listed hosting, explainability, scenario comparison, cost/CO₂, reliability, and documentation. The table below records how far the **repository** matches that list. **Partial** is not a failing grade; it marks a **deliberate** cut line for scope (here, **side-by-side** scenario UI deferred).

| Proposal item | Status | Explanation |
|---------------|--------|-------------|
| Online hosting | **Ready** | Flask app; public URL is deployment, not missing code. |
| Explainability | **Done** | SHAP or feature importance; method shown in UI. |
| Scenario comparison | **Partial** | What-if by **changing inputs and resubmitting**; no dual-panel **A/B** store. |
| Cost & CO₂ | **Done** | User mass + `calculate_cost_co2_impact` defaults. |
| Reliability | **Done** | k-NN + normalised deviation → score + label. |
| Docs / usability | **Done** | About, Features, README, this chapter, technical appendix file. |

In narrative terms, semester two **closes** the loop from “model that scores well on synthetic tests” to “tool that explains itself, flags unfamiliar inputs, and speaks money and carbon.” The largest **product gap** relative to the proposal wording is a **dedicated** two-scenario comparison view; everything else in the table is either **complete** or **deployment-only**.

---

## 9. How to run (reproducibility)

A marker should be able to go from clone to browser in a small number of steps. The bullet list is the **minimal** path; the paragraph after it states what can be skipped for a quick demo and what must be cited in the report.

- Create a **virtual environment** and run **`pip install -r requirements.txt`**.
- Ensure **`data/train_data.csv`** and **`data/test_data.csv`** exist; if not, run **`python data_generation/generate_train_test_data.py`**.
- Train and export the artefact with **`python model.py`** (updates **`models/best_steel_waste_model.pkl`** and comparison CSVs).
- Start the app with **`python app.py`** and open **http://localhost:5005** (default port in source).

If a compatible pickle is already committed for demonstration, step three may be skipped for speed, but any **quoted test metrics** or **screenshots** in the thesis should name **which** pickle and **which** data split they came from.

```bash
# From project root
pip install -r requirements.txt
python data_generation/generate_train_test_data.py   # if CSVs missing
python model.py
python app.py
```

---

## 10. Relation to project objectives

The formal objectives asked for **accurate prediction**, **understanding of drivers**, **a usable interface**, and **economic / environmental context**. Second-semester development **extends** the first-semester proof without discarding it: the **same** regression target and feature philosophy remain, while the **delivery layer** adds explanations, reliability, cost/CO₂, and an API. **Interpretability** outputs support discussions of **which levers** matter; **reliability** supports **cautious** use when data are still synthetic; **cost and CO₂** connect the percentage to **budget and sustainability** narratives in the original proposal.

**External validity** still hinges on **training data quality and domain**. Until large **real** project files augment or replace the generator, report language should treat accuracy and neighbour-based confidence as **conditional** on the synthetic regime. **Retraining** is intentionally cheap at the software level: a new **`model.py`** run and pickle swap refresh every consumer—the form, the API, and any host—without a Flask rewrite.

---

## 11. Limitations and future work

Honest limits strengthen a final-year report. The main **constraints** observed in the current system are:

- **Synthetic dominance** — rules in `synthetic_data_generator.py` drive correlations; **real** contractor data may shift error until reported.
- **Reliability heuristic** — distance-based score, **not** a formal prediction interval or calibrated error probability.
- **Economic and carbon defaults** — placeholders until tied to **quotes** and **verified** factors for specific steel products and regions.
- **Scenario workflow** — users compare cases by **editing and resubmitting**, not by a stored **A vs. B** session in the UI.

Looking forward, natural next steps include **ingesting real site and procurement fields**, **re-evaluating** models on a **real hold-out** set (and updating **Table 3**-style results), adding an optional **dual-scenario** or **export** feature for tenders, **hardening** deployment (HTTPS, WSGI, removal of debug routes), and **localising** currency and language if the tool leaves the academic context.

---

## 12. Suggested figures for the report

Figures matter in defence. Plan visuals so both **inputs** and **full outputs** appear, not only the headline percentage.

- **Predict** screen: form plus **complete** results card—**%**, **category**, **reliability** text and badge, **cost/CO₂** tiles, **explainability** list including **SHAP** vs **Feature Importance** label.
- **Landing**, **About**, and **Features** pages: show polish and navigation.
- **Optional:** one **cropped JSON** response from **`/api/predict`** beside a note that it matches the form pipeline.

High resolution avoids blurry printouts; consistent browser zoom keeps captions honest when you describe what the reader is seeing.

---

## 13. Key code references (for appendix or footnotes)

| Topic | Location |
|-------|----------|
| Preprocess, train, save, load | `model.py` — `prepare_features`, `compare_models`, `save_best_model`, `load_model` |
| Predict + analytics | `model.py` — `predict`, `explain_prediction`, `calculate_reliability`, `calculate_cost_co2_impact` |
| Web + API | `app.py` — `load_model`, `predict()` route, `api_predict`, `get_waste_category`, `format_explainability_features` |
| UI | `templates/predict.html`, `base.html` |
| Synthetic data | `data_generation/synthetic_data_generator.py`, `generate_train_test_data.py` |
| Dependencies | `requirements.txt` |

The table above is the compact index; the prose sections of this chapter explain **why** each area exists and **how** it behaves for users and examiners.

---

*Maintained as: `SECOND_SEMESTER_ADDENDUM.md` in the project root. Pair with `TECHNICAL_APPENDIX_FULL.md` for full tabulated API and file tree.*
