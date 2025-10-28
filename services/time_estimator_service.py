import math
from models import RideParameters
from services.parse_files_service import parse_tcx_to_segmented_route
from services.zone_service import get_power_by_zone_name
from services.power_service import get_steady_state_velocity
from utils import format_time


def estimate_training_time_required_to_route(ride_parameters: RideParameters):
  """Estimate training time required to complete a route"""
  total_mass = ride_parameters.rider_mass + ride_parameters.bike_mass
  total_time_sec = 0
  total_dist_m = 0
  details = []

  for i, segment in enumerate(ride_parameters.route_segments):
    slope = math.atan(segment.grade / 100)
    power = get_power_by_zone_name(segment.zone, ride_parameters.ftp)

    wind_component = 0
    if segment.heading is not None:
      wind_component = ride_parameters.wind_speed / 3.6 * math.cos(math.radians(segment.heading - ride_parameters.wind_dir))

    rider_velocity = get_steady_state_velocity(
      power, 
      ride_parameters.air_density, 
      ride_parameters.cda, 
      ride_parameters.cr, 
      wind_component, 
      total_mass, 
      ride_parameters.gravity, 
      slope
    )
    # power_avail = (Pa + Pc + Pr) * v
    time_segment_sec = segment.distance / rider_velocity # the inverse: rider_velocity = segment.distance / time_segment_sec
    total_time_sec += time_segment_sec
    total_dist_m += segment.distance

    details.append({
      "index": i + 1, # util to create the workout file
      "distance": segment.distance, # in meters
      "grade": segment.grade,
      "heading": segment.heading,
      "zone": segment.zone,  # util to create the workout file
      "power_w": power, # util to create the workout file
      "time_min": time_segment_sec / 60 # util to create the workout file
    })

  total_time_h_m_s = format_time(total_time_sec)
  total_dist_km = total_dist_m / 1000
  return total_time_h_m_s, total_dist_km, details
