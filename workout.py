def group_segments_by_zone_and_time(segments, min_duration=0.5):
  merged = []
  current_zone = segments[0]['zone']
  total_time = 0
  total_power = 0
  buffer = []

  for segment in segments:
    zone = segment.get('zone', 'Z2')
    power = segment.get('power_w', 100)
    time_min = segment.get('time_min', min_duration)

    if zone == current_zone:
      # same zone, accumulate
      buffer.append(segment)
      total_time += time_min
      total_power += power
    else:
      # zone changed, commit previous zone
      if total_time >= min_duration:
        merged.append({
          'zone': current_zone,
          'power_w': total_power / len(buffer),
          'time_min': total_time
        })
      else:
        # too short -> merge into previous if exists
        if merged:
          merged[-1]['time_min'] += total_time
        else:
          merged.append({
            'zone': current_zone,
            'power_w': total_power / len(buffer),
            'time_min': total_time
          })

      # reset accumulators
      current_zone = zone
      total_time = time_min
      total_power = power
      buffer = [segment]

  # commit the last buffer
  if total_time > 0:
    merged.append({
      'zone': current_zone,
      'power_w': total_power / len(buffer),
      'time_min': total_time
    })

  return merged

def generate_mrc_from_zones(segments, ftp, filename="example.mrc"):
  grouped = group_segments_by_zone_and_time(segments)
  cumulative_time = 0.0

  with open(filename, 'w') as f:
    f.write("[COURSE HEADER]\n")
    f.write("VERSION = 2\n")
    f.write("UNITS = METRIC\n")
    f.write("DESCRIPTION = Generated workout\n")
    f.write(f"FILENAME = {filename}\n")
    f.write("MINUTES PERCENT\n")
    f.write("[END COURSE HEADER]\n\n")
    f.write("[COURSE DATA]\n")

    # Initial block
    first_power = (grouped[0]['power_w'] / ftp) * 100
    f.write(f"0.000\t{first_power:.1f}\n")

    for i, seg in enumerate(grouped):
      cumulative_time += seg['time_min']
      current_power = (seg['power_w'] / ftp) * 100

      # end of segment
      f.write(f"{cumulative_time:.3f}\t{current_power:.1f}\n")

      # if there's a next segment, repeat time with new power
      if i < len(grouped) - 1:
        next_power = (grouped[i + 1]['power_w'] / ftp) * 100
        f.write(f"{cumulative_time:.3f}\t{next_power:.1f}\n")

    f.write("[END COURSE DATA]\n")

  print(f"✅ Workout saved as {filename}")