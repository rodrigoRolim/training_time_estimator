from models import SegmentGenerationConfig, RouteSegment
from services.parse_files_service import parse_tcx_to_segmented_route
from services.distance_service import convert_latlon_to_local_points
from services.heading_service import compute_headings, smooth_headings
from services.grade_service import compute_grades
from services.zone_service import get_zone_by_grade

def create_segmented_route_from_route_file(segment_generation_config: SegmentGenerationConfig): # only .tcx for now
  # Parse and preprocess points
  points = parse_tcx_to_segmented_route(segment_generation_config.file)  # raw TCX points with lat, lon, ele
  local_points = convert_latlon_to_local_points(points)
  headings_list = compute_headings(local_points)
  smoothed_headings = smooth_headings(headings_list, segment_generation_config.smoothing_window)
  grades = compute_grades(local_points)

  # Accumulate distance for aggregation
  route = []
  acc_distance = 0
  acc_weighted_grade = 0
  start_index = 0

  for i in range(1, len(local_points)):
    distance = local_points[i]['distance']
    acc_distance += distance
    acc_weighted_grade += grades[i - 1] * distance

    # Check if we reached the minimum distance threshold or last point
    if acc_distance >= segment_generation_config.min_distance or i == len(local_points) - 1:
      avg_grade = acc_weighted_grade / acc_distance
      heading = smoothed_headings[i - 1]
      zone_name = get_zone_by_grade(avg_grade)

      route_segment = RouteSegment(
        distance=acc_distance,
        grade=avg_grade,
        heading=heading,
        zone=zone_name
      )
      route.append(route_segment)

      # Reset accumulators for next segment
      acc_distance = 0
      acc_weighted_grade = 0
      start_index = i

  return route