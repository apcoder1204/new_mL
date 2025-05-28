from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import cloudpickle

# Load model
with open("wifi_threat_model_pipeline4.pkl", "rb") as f:
    model = cloudpickle.load(f)

# FastAPI app
app = FastAPI()

# Input model
class Features(BaseModel):
    Packet_Size: float
    TTL: int
    Time_Delta: float
    src_port: int
    dst_port: int
    Known_BSSID: str
    Protocol: str
    TCP_Flags: str
    Packet_Direction: str

# Prediction endpoint
@app.post("/predict")
def predict(data: Features):
    try:
        input_df = pd.DataFrame([data.dict()])
        prediction = model.predict(input_df)[0]
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
