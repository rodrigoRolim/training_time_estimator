from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from models import RideParameters, SegmentGenerationConfig, Segment, WorkoutRequest
from services.time_estimator_service import estimate_training_time_required_to_route
from services.route_service import create_segmented_route_from_route_file
from services.workout_service import generate_mrc_from_zones

from typing import List
import tempfile
import os
import logging, io, traceback
import traceback

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.post(
  "/estimate-training-time",
  summary="Estimate total training time for a route",
  description="Uploads a TCX file and rider parameters to estimate total route time."  
) # ride_parameter + file
async def get_training_time_required_to_route(
  file: UploadFile = File(...), 
  ftp: int = Form(...), 
  wind_dir: int = Form(...), 
  wind_speed: float = Form(...), 
  rider_mass: float =  Form(...), 
  bike_mass: float = Form(...)
) -> JSONResponse:
  try:
    # save the file temporarily
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, file.filename)
    with open(file_path, "wb") as tmp_file:
      tmp_file.write(await file.read())

    config_route_segmentation = SegmentGenerationConfig(
      file=file_path,
      smoothing_window=3,
      min_distance=100
    )
    segmented_route = create_segmented_route_from_route_file(config_route_segmentation)

    ride_parameter = RideParameters(
      ftp=ftp,
      wind_speed=wind_speed,
      wind_dir=wind_dir,
      rider_mass=rider_mass,
      bike_mass=bike_mass,
      route_segments=segmented_route,
      cda=0.30,
      cr=0.005,
      air_density=1.225,
      gravity=9.81
    )

    estimated_time, total_distance, segments = estimate_training_time_required_to_route(ride_parameter)
    hours, minutes = estimated_time
    return JSONResponse(
      content={
        "estimated_time": {"hours": hours, "minutes": minutes},
        "total_distance": total_distance,
        "segments": segments
      }
    )
  finally:
    if os.path.exists(file_path):
      os.remove(file_path)

@router.post("/create-workout")
async def create_workout_from_route(workout_req: WorkoutRequest) -> StreamingResponse:
  # save the file temporarily
  
  try:
    # Cria um buffer de bytes em memória
    mrc_buffer = io.BytesIO()
    generate_mrc_from_zones(workout_req.segments, workout_req.ftp, mrc_buffer)
    # Volta para o início do buffer para leitura
    mrc_buffer.seek(0)

    # Retorna como StreamingResponse para download
    filename = f"workout_{workout_req.ftp}watts.mrc"
    return StreamingResponse(
      mrc_buffer,
      media_type="text/plain",
      headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
  except Exception as e:
    logger.exception("Erro ao criar workout")
    print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
 