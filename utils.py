R = 6371000.0 # Earth radius in meters

def format_time(total_seconds: float):
  total_seconds = int(total_seconds)
  hours = total_seconds // 3600
  minutes = (total_seconds % 3600) // 60
  seconds = total_seconds % 60

  return hours, minutes, seconds