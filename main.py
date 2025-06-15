from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
import os
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "your_bot_token_here"
TELEGRAM_BOT_SECRET = TELEGRAM_BOT_TOKEN.split(":")[1]  # simple secret for JWT validation

class InitDataRequest(BaseModel):
    initData: str

@app.post("/validate-initdata")
async def validate_initdata(data: InitDataRequest):
    try:
        decoded = jwt.decode(data.initData, TELEGRAM_BOT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        return {"valid": True, "data": decoded}
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=400, detail=f"Invalid initData: {str(e)}")

@app.get("/init-data")
async def get_init_data():
    import json, pathlib
    data_path = pathlib.Path(__file__).parent / "data" / "sticker_data.json"
    with open(data_path, "r") as f:
        return json.load(f)
