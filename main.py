from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timezone

app = FastAPI()

# ✅ CORS (REQUIRED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENDERIZE_URL = "https://api.genderize.io"


@app.get("/api/classify")
async def classify_name(name: str = Query(...)):
    
    if not name or name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Name parameter is required"}
        )
    
    if not isinstance(name, str):
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Name parameter must be a string"}
        )
    try:
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name})
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail={"status": "error", "message": "Failed to fetch from Genderize API"}
            )

        data = response.json()

        gender = data.get("gender")
        probability = data.get("probability")
        count = data.get("count")


        if gender is None or count == 0:
            return {
                "status": "error",
                "message": "No prediction available for the provided name"
            }

        
        sample_size = count
        is_confident = probability >= 0.7 and sample_size >= 100

        processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return {
            "status": "success",
            "data": {
                "name": name.lower(),
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at
            }
        }

    except httpx.RequestError as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "Internal server error"}
        )