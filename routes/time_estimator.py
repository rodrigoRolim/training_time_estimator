from fastapi import APIRouter, File, Form, UploadFile
from models import RideParameters, SegmentGenerationConfig
from services.time_estimator_service import estimate_training_time_required_to_route
from services.route_service import create_segmented_route_from_route_file
import tempfile
import os

router = APIRouter()

@router.post("/estimate-training-time") # ride_parameter + file
async def get_training_time_required_to_route(
  file: UploadFile = File(...), 
  ftp: int = Form(...), 
  wind_dir: int = Form(...), 
  wind_speed: float = Form(...), 
  rider_mass: float =  Form(...), 
  bike_mass: float = Form(...)
):

  # save the file temporarily
  tmp_dir = tempfile.gettempdir()
  file_path = os.path.join(tmp_dir, file.filename)

  with open(file_path, "wb") as tmp_file:
    tmp_file.write(await file.read())
  # 
  # estimate_training_time_required_to_route(ride_parameters)
  # FTP_BASE = 250 # in watts
  # update FTP based on previous ride
  # FTP = update_ftp(FTP_BASE, 'ride_historics')
  # route = create_route(50, 30) # create a route with 50 segments and 30° by step
  # tcx_file = './routes/onthegomap-2.4-km-route.tcx'
  # route = build_route_from_tcxfile(tcx_file, smoothing_window=3)
  config_route_segmentation = SegmentGenerationConfig(
    file = file_path,
    smoothing_window = 3,
    min_distance = 100
  )
  segmented_route = create_segmented_route_from_route_file(config_route_segmentation)

  ride_parameter = RideParameters(
    ftp = ftp,
    wind_speed = wind_speed,
    wind_dir = wind_dir,
    rider_mass = rider_mass,
    bike_mass = bike_mass,
    route_segments = segmented_route,
    cda = 0.30,
    cr = 0.005,
    air_density = 1.225, # at sea level
    gravity = 9.81
  )
  estimated_time, total_distance, segments = estimate_training_time_required_to_route(ride_parameter)
  hours, minutes = estimated_time
  return {"estimated_time": {"hours": hours, "minutes": minutes}, "total_distance": total_distance}

