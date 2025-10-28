from models import SegmentGenerationConfig, RouteSegmentsGroupedByDistance, RouteSegmentGroupedByZoneAndTime
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
      weighted_avg_grade = acc_weighted_grade / acc_distance
      heading = smoothed_headings[i - 1]
      zone_name = get_zone_by_grade(weighted_avg_grade)

      route_segment = RouteSegmentsGroupedByDistance(
        distance=acc_distance,
        grade=weighted_avg_grade,
        heading=heading,
        zone=zone_name
      )
      route.append(route_segment)

      # Reset accumulators for next segment
      acc_distance = 0
      acc_weighted_grade = 0
      start_index = i

  return route

def group_segments_by_zone_and_time(segments, min_duration=0.5, min_segments=5):
  merged = []
  current_zone = segments[0].zone
  total_time = 0
  total_power = 0
  buffer = []

  for segment in segments:
    zone = segment.zone
    power = segment.power_w
    time_min = segment.time_min

    if zone == current_zone and (total_time < min_duration or len(buffer) < min_segments):
      # same zone, accumulate
      buffer.append(segment)
      total_time += time_min
      total_power += power
    else:
      merged.append(RouteSegmentGroupedByZoneAndTime(
        zone=current_zone,
        power_w=total_power / len(buffer),
        time_min=total_time
      ))

      # reset accumulators
      current_zone = zone
      total_time = time_min
      total_power = power
      buffer = [segment]

  # commit the last buffer
  if buffer:
    merged.append(RouteSegmentGroupedByZoneAndTime(
      zone=current_zone,
      power_w=total_power / len(buffer),
      time_min=total_time
    ))

  return merged