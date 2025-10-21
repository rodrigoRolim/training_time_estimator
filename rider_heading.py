import math

R = 6371000.0 # Earth radius in meters

def convert_latlon_to_local_meters(lat_end, lon_end, lat_origin, lon_origin):
  """
  I belive the map of the zwift is flat so we need a local flat coordinate system.

  Convert lat/lon (degress) to local East North meters relative to origin. Uses equirectangular approximation, 
  which is sufficient for short distances.
  
  Returns earth_m, north_m
  """
  lat_origin_meter = math.radians(lat_origin) # origin latitude in meters
  lat_end_meter = math.radians(lat_end) # end latitude in meters
  delta_longitudes = math.radians(lon_end - lon_origin)
  delta_latitudes = math.radians(lat_end - lat_origin)
  north = R * delta_latitudes
  east = R * math.cos(lat_end_meter) * delta_longitudes
  return east, north

def get_heading_btw_points(east_origin, north_origin, east_end, north_end):
  dx = east_end - east_origin # east difference
  dy = north_end - north_origin # north difference  
  if abs(dx) < 1e-9 and abs(dy) > 1e-9:
    return None
  
  theta = math.atan2(dx, dy) # note: dx first so 0° = north, clockwise positive
  return (math.degrees(theta) + 360) % 360


print("Heading (deg): ", heading_deg)

def get_circular_mean_deg(angle_list_deg):
  """
  cause we are recording positions vert frenquently, small errors in lat/lon or tiny fluctuations in the
  simulator can cause the calculated heading to jump rapidly from one value to another. So due this oscillation
  present in simulator we have a jitter and we must solve this. There some common methods to smoothing the jitter.
  I'll use the Circular moving average.

  Compute circular mean of angles in degrees
  """
  sum_x = sum(math.cos(math.radians(a)) for a in angle_list_deg)
  sum_y = sum(math.sin(math.radians(a)) for a in angle_list_deg)
  mean_angle = math.degrees(math.atan(sum_x, sum_y))
  return (mean_angle + 360) % 360

# example usage with two trackpoints
lat_0, lon_0 = 40.87733, -96.72649 # first trackpoint (given) point zero P0
# hypothetical second point (replace with actual next trackpoint)
lat_1, lon_1 = 40.87740, -96.72630 # second point P1
# third point
# lat_2, lon_2 = 40.87746, -96.72633 # third point P2

east_0, north_0 = convert_latlon_to_local_meters(lat_0, lon_0, lat_0, lon_0) # (0,0) or just east_0, north_0 = 0, 0
east_1, north_1 = convert_latlon_to_local_meters(lat_1, lon_1, lat_0, lon_0)

# continue...
# east_2, north_2 = convert_latlon_to_local_meters(lat_2, lon_2, lat_0, lon_0)
# ...
# east_n, north_n = convert_latlon_to_local_meters(lat_n, lon_n, lat_0, lon_0)

heading_deg = get_heading_from_local(east_0, north_0, east_1, north_1)