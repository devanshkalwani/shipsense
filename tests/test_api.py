
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_predict_valid_order():
    payload = {
        "customer_state": "SP", "primary_payment_type": "credit_card",
        "total_payment_value": 150.0, "purchase_month": 6, "purchase_dayofweek": 2,
        "purchase_hour": 14, "is_weekend": 0, "approval_delay_hours": 0.5,
        "item_count": 1, "distinct_sellers": 1, "total_freight": 20.0,
        "total_price": 130.0, "freight_pct_of_value": 0.15, "avg_product_weight": 500.0,
        "multi_seller": 0, "ship_distance_km": 350.0, "seller_hist_late_rate": 0.07,
        "product_category_name": "informatica_acessorios"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "risk_score" in body
    assert 0.0 <= body["risk_score"] <= 1.0

def test_predict_rejects_bad_state():
    payload = {
        "customer_state": "ZZ", "primary_payment_type": "credit_card",
        "total_payment_value": 150.0, "purchase_month": 6, "purchase_dayofweek": 2,
        "purchase_hour": 14, "is_weekend": 0, "approval_delay_hours": 0.5,
        "item_count": 1, "distinct_sellers": 1, "total_freight": 20.0,
        "total_price": 130.0, "freight_pct_of_value": 0.15, "avg_product_weight": 500.0,
        "multi_seller": 0, "ship_distance_km": 350.0, "seller_hist_late_rate": 0.07,
        "product_category_name": "informatica_acessorios"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
