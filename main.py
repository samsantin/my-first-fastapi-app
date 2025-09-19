import os
from fastapi import FastAPI, Security, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from dotenv import load_dotenv

# ---------- Cargar variables ----------
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ---------- Modelos ----------
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float

# ---------- App ----------
app = FastAPI(title="API Key Demo")

# ---------- Seguridad por header ----------
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ---------- Endpoint protegido ----------
@app.get("/api/v1/secure-data/", tags=["secure"])
async def secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "Secure data access granted."}

# ---------- Endpoints de ejemplo previos ----------
@app.get("/")
async def hello_world():
    return "Hello World!"

@app.get("/api/v1/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/api/v1/items/")
async def create_item(item: Item):
    return (f"El item {item.name} es: "
            f"{item.description}, cuesta {item.price}, "
            f"y tiene un impuesto de {item.tax}")