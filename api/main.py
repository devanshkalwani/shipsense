import joblib
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="Shipsense Delay Risk API", version="1.0")

# --- Load model and metadata once at startup ---
MODEL_PATH = "../models/shipsense_delay_model_v2.joblib"
METADATA_PATH = "../models/model_metadata_v2.json"
CATEGORY_PATH = "../models/category_mappings.json"

model = joblib.load(MODEL_PATH)
with open(METADATA_PATH) as f:
    metadata = json.load(f)
with open(CATEGORY_PATH) as f:
    category_mappings = json.load(f)

FEATURE_ORDER = metadata["features"]
CAT_COLS = metadata["categorical_features"]


class OrderFeatures(BaseModel):
    customer_state: str
    primary_payment_type: str
    total_payment_value: float = Field(..., ge=0)
    purchase_month: int = Field(..., ge=1, le=12)
    purchase_dayofweek: int = Field(..., ge=0, le=6)
    purchase_hour: int = Field(..., ge=0, le=23)
    is_weekend: Literal[0, 1]
    approval_delay_hours: float = Field(..., ge=0)
    item_count: int = Field(..., ge=1)
    distinct_sellers: int = Field(..., ge=1)
    total_freight: float = Field(..., ge=0)
    total_price: float = Field(..., ge=0)
    freight_pct_of_value: float = Field(..., ge=0)
    avg_product_weight: float = Field(..., ge=0)
    multi_seller: Literal[0, 1]
    ship_distance_km: float = Field(..., ge=0)
    seller_hist_late_rate: float = Field(..., ge=0, le=1)
    product_category_name: str


class PredictionResponse(BaseModel):
    risk_score: float
    is_high_risk: bool
    model_version: str = "v2"


@app.get("/health")
def health_check():
    return {"status": "ok", "model_version": "v2", "test_auc": metadata.get("test_auc")}


@app.post("/predict", response_model=PredictionResponse)
def predict(order: OrderFeatures):
    try:
        data = order.model_dump()
        df = pd.DataFrame([data])

        # Re-apply the exact training-time categories so LightGBM sees the same encoding
        for col in CAT_COLS:
            df[col] = pd.Categorical(df[col], categories=category_mappings[col])
            if df[col].isnull().any():
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown value for '{col}'. Expected one of: {category_mappings[col]}"
                )

        df = df[FEATURE_ORDER]  # enforce exact training column order

        risk_score = float(model.predict_proba(df)[:, 1][0])
        return PredictionResponse(
            risk_score=round(risk_score, 4),
            is_high_risk=risk_score >= 0.5
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
