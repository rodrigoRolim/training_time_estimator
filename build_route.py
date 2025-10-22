import math
from utils import R
from parser import parse_tcx
from rider_heading import compute_headings, smooth_headings
from grades import compute_grades

def convert_latlon_to_local_points(points):
  """
  Convert latitude and longitude to local meters relative to first point
  """
  lat_0, lon_0 = points[0]['latitude'], points[0]['longitude'] # first point
  local_points = []
  for point in points:
    lat_in_radians = math.radians(point['latitude'])
    lat_in_radians_origin = math.radians(lat_0)
    delta_latitudes = math.radians(point['latitude'] - lat_0)
    delta_longitudes = math.radians(point['longitude'] - lon_0)
    north = R * delta_latitudes
    east = R * math.cos(lat_in_radians) * delta_longitudes
    local_points.append({
      'east': east,
      'north': north,
      'distance': point['distance'],
      'altitude': point['altitude']
    })

  return local_points

def build_route_from_tcxfile(tcx_file, smoothing_window=3):
  points = parse_tcx(tcx_file)
  local_points = convert_latlon_to_local_points(points)
  headings_list = compute_headings(local_points)
  smoothed_headings = smooth_headings(headings_list, smoothing_window)
  grades = compute_grades(local_points)

  # in each tuple, we have (distance, grade, heading)
  route = []
  for i in range(1, len(local_points)):
    distance = local_points[i]['distance']
    grade = grades[i - 1]
    heading = smoothed_headings[i - 1]
    route.append((distance, grade, heading))
  
  return route

# Example of usage
# tcx_file = './2023_Garmin_Gravel_Worlds_150_p_b_Lauf.tcx'
# route = build_route_from_tcxfile(tcx_file, smoothing_window=3)
# for r in route[:10]: # show the first 10 points
#  print(r)