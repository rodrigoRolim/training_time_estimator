import math
from models import RideParameters
from services.zone_service import get_power_by_zone_name
from services.power_service import get_steady_state_velocity
from scipy.optimize import root_scalar

def estimate_ftp_for_target_time(
  wind_speed: float, 
  wind_dir: int, 
  rider_mass: float,
  bike_mass: float,
  route_segments: List[RouteSegment],
  cda: float,
  cr: float,
  air_density: float,
  gravity: float, 
  target_time_sec: int
):
  """
  Estimate the FTP required to complete a route in a given target time.
  """

  def total_time_for_ftp(ftp):
    total_mass = rider_mass + bike_mass
    total_time_sec = 0

    for segment in route_segments:
      slope = math.atan(segment.grade / 100)
      power = get_power_by_zone_name(segment.zone, ftp)


      wind_component = 0
      if segment.heading is not None:
        wind_component = wind_speed / 3.6 * math.cos(math.radians(segment.heading - wind_dir))

      rider_velocity = get_steady_state_velocity(
        power,
        air_density, 
        cda, 
        cr, 
        wind_component, 
        total_mass, 
        gravity, 
        slope
      )

      time_segment_sec = segment.distance / rider_velocity
      total_time_sec += time_segment_sec

    return total_time_sec - target_time_sec # we want this to be 0
  
  # solve for FTP btw reasanable bounds
  sol = root_scalar(total_time_for_ftp, bracket=[50, 1500], method='bisect', xtol=0.1)

  if sol.converged:
    return sol.root
  else:
    raise ValueError("Could not converge to an FTP solution for the target time")