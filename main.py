from fastapi import FastAPI
from routes import time_estimator

app = FastAPI(title="Workout generator Service")

app.include_router(time_estimator.router, prefix="/workout", tags=["items"])

@app.get("/")
def health_check():
  return {"message": "Api is running"}