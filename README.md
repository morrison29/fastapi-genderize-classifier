# Genderize Classifier API

A FastAPI service that integrates with the Genderize API to classify names and return structured results with confidence scoring.

## Endpoint
GET /api/classify?name={name}

## Example Response
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}

## Error Format
{
  "status": "error",
  "message": "Error description"
}

## Setup
pip install -r requirements.txt  
uvicorn main:app --reload

## Tech Stack
FastAPI, Python, httpx

## Live API
https://your-app.up.railway.app