from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api
import logging

# Configuração global do logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger()  # root logger

app = FastAPI(title="Workout generator Service")

app.include_router(api.router, prefix="/workout")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["Content-Disposition"],
)
@app.get("/")
def health_check():
  return {"message": "Api is running"}