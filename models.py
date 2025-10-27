from pydantic import BaseModel
from typing import List

class RouteSegment(BaseModel):
  distance: float # distance
  grade: float # average grade
  heading: float
  zone: str

class RideParameters(BaseModel):
  ftp: int
  wind_speed: float
  wind_dir: int
  rider_mass: float
  bike_mass: float
  route_segments: List[RouteSegment]
  cda: float # coefficient of drag 
  cr: float # coefficient of rolling
  air_density: float
  gravity: float # ~ 9.81

class SegmentGenerationConfig(BaseModel):
  file: str
  smoothing_window: int = 3
  min_distance: int = 100 # meters

class ParseTcxFileOptions(BaseModel):
  filepath: str
  namespace: str

class PowerBalanceParameter(BaseModel):
  current_velocity: float
  air_density: float
  cda: float # coefficient of drag
  cr: float # coefficient of rolling
  wind_component: float
  total_mass: float
  gravity: float
  slope: float
