from zones import get_intensity_from_grade
from powers import get_steady_state_velocity
from utils import format_time
from zones import get_power_from_zone

import math

def estimate_training_time_dynamic_ftp(
  ftp, route_segments, wind_speed=0, wind_dir=0, rider_mass=75, bike_mass=8,
  cda=0.30, cr=0.005, air_density=1.225, gravity=9.81, intensity=0.8
):
  total_mass = rider_mass + bike_mass
  total_time_sec = 0
  total_dist_m = 0
  details = []

  for i, (dist_m, grade, heading) in enumerate(route_segments):
    slope = math.atan(grade / 100)
    intensity = get_intensity_from_grade(grade)
    power = ftp * intensity

    wind_component = 0
    if heading is not None:
      wind_component = wind_speed / 3.6 * math.cos(math.radians(heading - wind_dir))

    rider_velocity = get_steady_state_velocity(
      power, air_density, cda, cr, wind_component, total_mass, gravity, slope
    )

    time_segment_sec = dist_m / rider_velocity
    total_time_sec += time_segment_sec
    total_dist_m += dist_m

    details.append({
      "segment": i + 1,
      "distance_km": dist_m / 1000,
      "grade_percent": grade,
      "wind_component_kmh": wind_component * 3.6,
      "speed_kmh": rider_velocity * 3.6,
      "time_min": time_segment_sec / 60
    })

  total_time_h_m = format_time(total_time_sec)
  total_dist_km = total_dist_m / 1000
  return total_time_h_m, total_dist_km, details

def estimate_training_time_static_ftp(
  ftp, route_segments, wind_speed=0, wind_dir=0, rider_mass=75, bike_mass=8,
  cda=0.30, cr=0.005, air_density=1.225, gravity=9.81, intensity=0.8
):
  total_mass = rider_mass + bike_mass
  total_time_sec = 0
  total_dist_m = 0
  power = ftp * intensity
  details = []

  for i, (dist_m, grade, heading) in enumerate(route_segments):
    slope = math.atan(grade / 100)
    wind_component = 0
    if heading is not None:
      wind_component = wind_speed / 3.6 * math.cos(math.radians(heading - wind_dir))

    rider_velocity = get_steady_state_velocity(
      power, air_density, cda, cr, wind_component, total_mass, gravity, slope
    )

    time_segment_sec = dist_m / rider_velocity
    total_time_sec += time_segment_sec
    total_dist_m += dist_m

    details.append({
      "segment": i + 1,
      "distance_km": dist_m / 1000,
      "grade_percent": grade,
      "wind_component_kmh": wind_component * 3.6,
      "speed_kmh": rider_velocity * 3.6,
      "time_min": time_segment_sec / 60
    })
  
  total_time_h_m = format_time(total_time_sec) 
  total_dist_km = total_dist_m / 1000
  return total_time_h_m, total_dist_km, details

def estimate_training_time_power_zones(
  route_segments, ftp, wind_speed=0, wind_dir=0, rider_mass=75, bike_mass=8,
  cda=0.30, cr=0.005, air_density=1.225, gravity=9.81
):
  """
  Estimate time to complete a route using POWER_ZONES for each segment
  route_segments: list of tuples (dist_m, grade_percent, heading, zone_name)
  """
  total_mass = rider_mass + bike_mass
  total_time_sec = 0
  total_dist_m = 0
  details = []

  for i, (dist_m, grade, heading, zone_name) in enumerate(route_segments):
    slope = math.atan(grade / 100)
    power = get_power_from_zone(zone_name, ftp)

    wind_component = 0
    if heading is not None:
      wind_component = wind_speed / 3.6 * math.cos(math.radians(heading - wind_dir))

    rider_velocity = get_steady_state_velocity(
      power, air_density, cda, cr, wind_component, total_mass, gravity, slope
    )

    time_segment_sec = dist_m / rider_velocity
    total_time_sec += time_segment_sec
    total_dist_m += dist_m

    details.append({
      "segment": i + 1,
      "distance_km": dist_m / 1000,
      "grade_percent": grade,
      "zone": zone_name,
      "power_w": power,
      "speed_kmh": rider_velocity * 3.6,
      "time_min": time_segment_sec / 60
    })

  total_time_h_m = format_time(total_time_sec)
  total_dist_km = total_dist_m / 1000
  return total_time_h_m, total_dist_km, details