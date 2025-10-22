import math
def compute_grades(local_points):
  """
  compute grade between two consecutives points
  """
  grades = []
  for i in range(1, len(local_points)):
    dz = local_points[i]['altitude'] - local_points[i-1]['altitude']
    dx = local_points[i]['east'] - local_points[i-1]['east']
    dy = local_points[i]['north'] - local_points[i-1]['north']
    horiz = math.hypot(dx, dy)  # horizontal distance in meters
    if horiz > 1e-6:
      grades.append((dz / horiz) * 100.0)
    else:
      grades.append(0.0)
  
  return grades