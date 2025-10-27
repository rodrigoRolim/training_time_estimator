R = 6371000.0 # Earth radius in meters

def format_time(total_seconds):
  total_minutes = int(total_seconds // 60)
  hours = total_minutes // 60
  minutes = total_minutes % 60

  return hours, minutes