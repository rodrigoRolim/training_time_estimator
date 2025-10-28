from models import Segment
from typing import List
# from logger import logger
from pydantic import BaseModel

class GroupedSegment(BaseModel):
  zone: str
  power_w: float
  time_min: float

def group_segments_by_zone_and_time(segments, min_duration=0.5, min_segments=5):
  merged = []
  current_zone = segments[0].zone
  total_time = 0
  total_power = 0
  buffer = []
  # print(type(segments))
  for segment in segments:
    # logger.info(f"Segment: {segment}")
    zone = segment.zone
    power = segment.power_w
    time_min = segment.time_min

    if zone == current_zone and (total_time < min_duration or len(buffer) < min_segments):
      # same zone, accumulate
      buffer.append(segment)
      total_time += time_min
      total_power += power
    else:
      merged.append(GroupedSegment(
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
    merged.append(GroupedSegment(
      zone=current_zone,
      power_w=total_power / len(buffer),
      time_min=total_time
    ))

  return merged

def generate_mrc_from_zones(segments: List[Segment], ftp, buffer: io.BytesIO):
  if not segments:
    raise ValueError("Empty segment list")

  grouped = group_segments_by_zone_and_time(segments)
  cumulative_time = 0.0

  buffer.write("[COURSE HEADER]\n".encode())
  buffer.write("VERSION = 2\n".encode())
  buffer.write("UNITS = METRIC\n".encode())
  buffer.write("DESCRIPTION = Generated workout\n".encode())
  # buffer.write(f"FILENAME = {filepath}\n".encode())
  buffer.write("MINUTES PERCENT\n".encode())
  buffer.write("[END COURSE HEADER]\n\n".encode())
  buffer.write("[COURSE DATA]\n".encode())

  # Initial block
  first_power = (grouped[0].power_w / ftp) * 100
  buffer.write(f"0.000\t{first_power:.1f}\n".encode())

  for i, seg in enumerate(grouped):
    cumulative_time += seg.time_min
    current_power = (seg.power_w / ftp) * 100

    # end of segment
    buffer.write(f"{cumulative_time:.3f}\t{current_power:.1f}\n".encode())

    # if there's a next segment, repeat time with new power
    if i < len(grouped) - 1:
      next_power = (grouped[i + 1].power_w / ftp) * 100
      buffer.write(f"{cumulative_time:.3f}\t{next_power:.1f}\n".encode())

  buffer.write("[END COURSE DATA]\n".encode())
