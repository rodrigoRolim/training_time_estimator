import math
from utils import R

def get_heading_btw_points(east_origin, north_origin, east_end, north_end):
  dx = east_end - east_origin # east difference
  dy = north_end - north_origin # north difference  
  if abs(dx) < 1e-9 and abs(dy) > 1e-9:
    return None
  
  theta = math.atan2(dx, dy) # note: dx first so 0° = north, clockwise positive
  return (math.degrees(theta) + 360) % 360

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
  mean_angle = math.degrees(math.atan2(sum_x, sum_y))
  return (mean_angle + 360) % 360

def compute_headings(local_points):
  """
  compute instantaneous headings btw two points
  """
  headings_list = []
  for i in range(1, len(local_points)):
    east_0, north_0 = local_points[i - 1]['east'], local_points[i - 1]['north']
    east_1, north_1 = local_points[i]['east'], local_points[i]['north']
    heading = get_heading_btw_points(east_0, north_0, east_1, north_1)
    if heading is None:
      heading = 0.0
    headings_list.append(heading)

  return headings_list

def smooth_headings(headings_list, window_size=3):
  """
  Smooth headings with circular moving average. It is used to remove the potencial jitter on headings
  """
  smoothed = []
  for i in range(len(headings_list)):
    start = max(0, i - window_size + 1)
    window = [heading for heading in headings_list[start:i + 1] if heading is not None]
    if window:
      smoothed.append(get_circular_mean_deg(window))
    else:
      smoothed.append(None)
  return smoothed


