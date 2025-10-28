from models import RouteSegmentGroupedByZoneAndTime
from typing import List
# from logger import logger
from pydantic import BaseModel

def generate_mrc_from_zones(grouped_segments_by_time_and_zone: List[RouteSegment], ftp, buffer: io.BytesIO):
  if not grouped_segments_by_time_and_zone:
    raise ValueError("Empty segment list")

  # grouped = group_segments_by_zone_and_time(segments)
  cumulative_time = 0.0

  buffer.write("[COURSE HEADER]\n".encode())
  buffer.write("VERSION = 2\n".encode())
  buffer.write("UNITS = METRIC\n".encode())
  buffer.write("DESCRIPTION = Generated workout\n".encode())
  buffer.write("MINUTES PERCENT\n".encode())
  buffer.write("[END COURSE HEADER]\n\n".encode())
  buffer.write("[COURSE DATA]\n".encode())

  # Initial block
  first_power = (grouped_segments_by_time_and_zone[0].power_w / ftp) * 100
  buffer.write(f"0.000\t{first_power:.1f}\n".encode())

  for i, seg in enumerate(grouped_segments_by_time_and_zone):
    cumulative_time += seg.time_min
    current_power = (seg.power_w / ftp) * 100

    # end of segment
    buffer.write(f"{cumulative_time:.3f}\t{current_power:.1f}\n".encode())

    # if there's a next segment, repeat time with new power
    if i < len(grouped_segments_by_time_and_zone) - 1:
      next_power = (grouped_segments_by_time_and_zone[i + 1].power_w / ftp) * 100
      buffer.write(f"{cumulative_time:.3f}\t{next_power:.1f}\n".encode())

  buffer.write("[END COURSE DATA]\n".encode())
