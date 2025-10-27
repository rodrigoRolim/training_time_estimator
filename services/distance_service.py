import math
from utils import R

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