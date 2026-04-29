"""
Smoke tests: model bundle, Flask pages, /api/predict, form POST /predict.
Run from repo root: pytest tests/test_smoke.py -v
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="module")
def app_module():
    import app as app_mod

    app_mod.app.config["TESTING"] = True
    return app_mod


@pytest.fixture(scope="module")
def client(app_module):
    return app_module.app.test_client()


def _sample_row(pid="pytest-P1"):
    return {
        "project_id": pid,
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
    }


def test_load_model(app_module):
    c = app_module.load_model()
    assert c.best_model is not None
    assert c.feature_columns


def test_build_prediction_bundle(app_module):
    comp = app_module.load_model()
    b = app_module.build_prediction_bundle(comp, _sample_row(), 100_000)
    assert "prediction" in b
    assert isinstance(b["prediction"], float)
    assert "intervals_available" in b
    assert "explanation" in b and b["explanation"].get("method")
    assert "cost_co2" in b
    assert "waste_cost_usd" in b["cost_co2"]
    assert "potential_cost_savings_usd" not in b["cost_co2"]
    assert "counterfactual" in b
    cf = b["counterfactual"]
    assert "available" in cf
    if b["explanation"]["method"] == "SHAP":
        assert b["shap_split"] is True
        assert len(b["positive_features"]) <= 3
        assert len(b["negative_features"]) <= 3
    j = app_module._json_api_response(b)
    json.dumps(j)


def test_json_api_response_serializable(app_module):
    comp = app_module.load_model()
    b = app_module.build_prediction_bundle(comp, _sample_row("pytest-json"), 50_000)
    j = app_module._json_api_response(b)
    json.dumps(j)
    assert j["success"] is True


def test_pages_get_200(client):
    for path in ("/", "/predict", "/about", "/features"):
        r = client.get(path)
        assert r.status_code == 200, path
        assert len(r.data) > 500, path


def test_predict_post_shows_results_card_visible(client):
    """Full-page POST: results panel visible (works without JavaScript)."""
    data = {
        "project_id": "pytest-form",
        "reinforcement_ratio": "120",
        "num_unique_lengths": "20",
        "stock_length_policy": "standard_12m",
        "cutting_optimization": "0",
        "bim_integration": "0",
        "design_revisions": "2",
        "supervision_index": "3",
        "material_control": "2",
        "storage_handling": "3",
        "offcut_reuse": "0",
        "change_orders": "1",
        "contract_type": "lump_sum",
        "lead_time": "15",
        "order_frequency": "4",
        "project_phase": "frame",
        "total_steel_kg": "100000",
    }
    r = client.post("/predict", data=data)
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'id="resultCard"' in html
    assert "display: block" in html
    assert "gaugeScaleCaption" in html or "waste-gauge" in html
    assert "waste-ml-triple" in html


def test_predict_result_card_has_gauge_when_shap(client, app_module):
    """POST /predict returns HTML with gauge markers when model runs."""
    data = {
        "project_id": "pytest-form",
        "reinforcement_ratio": "120",
        "num_unique_lengths": "20",
        "stock_length_policy": "standard_12m",
        "cutting_optimization": "0",
        "bim_integration": "0",
        "design_revisions": "2",
        "supervision_index": "3",
        "material_control": "2",
        "storage_handling": "3",
        "offcut_reuse": "0",
        "change_orders": "1",
        "contract_type": "lump_sum",
        "lead_time": "15",
        "order_frequency": "4",
        "project_phase": "frame",
        "total_steel_kg": "100000",
    }
    r = client.post("/predict", data=data)
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "Prediction Results" in html
    assert "valExpected" in html or "predictionScenarioData" in html or "waste-gauge" in html


def test_api_predict_ok(client):
    body = {**_sample_row("api-1"), "total_steel_kg": 100000}
    r = client.post("/api/predict", json=body)
    assert r.status_code == 200
    j = r.get_json()
    assert j["success"] is True
    assert "predicted_waste_percentage" in j
    assert "gauge" in j and "marker_pct" in j["gauge"]
    assert "cost_co2_impact" in j
    assert "counterfactual_savings" in j
    assert "p10" in j and "p90" in j
    assert "interpretation" in j and len(j["interpretation"]) > 10
    assert j.get("reliability_badge_color") in ("success", "warning", "danger", "secondary")


def test_api_predict_adds_project_id(client):
    body = {**_sample_row()}
    del body["project_id"]
    body["total_steel_kg"] = 10000
    r = client.post("/api/predict", json=body)
    assert r.status_code == 200
    assert r.get_json()["success"] is True


def test_api_predict_bad_json(client):
    r = client.post("/api/predict", data="not-json", content_type="application/json")
    assert r.status_code == 400


def test_debug_explain(client):
    r = client.get("/debug/explain")
    assert r.status_code in (200, 400)


def test_counterfactual_when_shap(app_module):
    from config import CO2_PER_KG_STEEL, STEEL_COST_PER_KG_USD

    comp = app_module.load_model()
    if app_module.build_prediction_bundle(comp, _sample_row(), 100000)["explanation"]["method"] != "SHAP":
        pytest.skip("SHAP not active")
    df_row = _sample_row()
    import pandas as pd

    df = pd.DataFrame([df_row])
    expl = comp.explain_prediction(df, top_n=5)
    cf = comp.calculate_counterfactual_potential(
        df, expl, 100000, STEEL_COST_PER_KG_USD, CO2_PER_KG_STEEL
    )
    assert isinstance(cf["available"], bool)


def test_config_constants():
    from config import CO2_PER_KG_STEEL, STEEL_COST_PER_KG_USD

    assert STEEL_COST_PER_KG_USD > 0
    assert CO2_PER_KG_STEEL > 0
