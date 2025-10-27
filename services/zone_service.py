def get_power_zones(FTP):
  POWER_ZONES = {
    'Z1': {'name': 'Active Recovery', 'min': 0, 'max': 0.55 * FTP},
    'Z2': {'name': 'Endurance', 'min': 0.55 * FTP, 'max': 0.75 * FTP},
    'Z3': {'name': 'Tempo', 'min': 0.75 * FTP, 'max': 0.90 * FTP},
    'Z4': {'name': 'Threshold', 'min': 0.90 * FTP, 'max': 1.05 * FTP},
    'Z5': {'name': 'VO2max', 'min': 1.05 * FTP, 'max': 1.20 * FTP},
    'Z6': {'name': 'Anaerobic', 'min': 1.20 * FTP, 'max': float('inf')}
  }

  return POWER_ZONES

def get_power_by_zone_name(zone_name, ftp):
  """Return midpoint watts of the given power zone"""
  power_zones = get_power_zones(ftp)
  zone = power_zones[zone_name]
  if zone['max'] == float('inf'):
    return zone['min']  # take minimum for Z6
  return (zone['min'] + zone['max']) / 2

def get_zone_by_grade(grade):
  if grade < -2:
    return 'Z1'  # Active Recovery (descent)
  elif grade < 1:
    return 'Z2'  # Endurance (flat)
  elif grade < 3:
    return 'Z3'  # Tempo (slight climb)
  elif grade < 6:
    return 'Z4'  # Threshold (moderate climb)
  elif grade < 10:
    return 'Z5'  # VO2max (intense climb)
  else:
    return 'Z6'  # Anaerobic (very steep)

def get_intensity_from_grade(grade):
  if grade < -2:
    return 0.6 # descent - Z1
  elif grade < 1:
    return 0.7 # flat - Z2
  elif grade < 3:
    return 0.85 # slight climb - Z3
  elif grade < 6:
    return 1.0 # moderate climb - Z4
  elif grade < 10:
    return 1.15 # intense climb - Z5
  else:
    return 1.3 # very intense climb - Z6
