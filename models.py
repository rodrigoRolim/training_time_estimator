from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form

class RouteSegment(BaseModel):
  index: int
  distance: float # in meters
  grade: float
  heading: float
  zone: str # zone name
  power_w: float # in watts
  time_min: float 

class RouteSegmentsGroupedByDistance(BaseModel):
  distance: float
  grade: float
  heading: float
  zone: str

class RouteSegmentGroupedByZoneAndTime(BaseModel):
  zone: str
  power_w: float
  time_min: float

#class RouteSegment(BaseModel):
#  distance: float # distance
#  grade: float # average grade
#  heading: float
#  zone: str

class RideParameters(BaseModel):
  ftp: int
  wind_speed: float
  wind_dir: int
  rider_mass: float
  bike_mass: float
  route_segments: List[RouteSegmentsGroupedByDistance]
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

class WorkoutRequest(BaseModel):
  ftp: int
  segments: List[RouteSegment]

class EstimateFTPRequest(BaseModel):
  segments: List[RouteSegment]
  wind_dir: int
  wind_speed: float
  rider_mass: float
  bike_mass: float
  target_time_sec: int