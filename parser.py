import xml.etree.ElementTree as ET

def parse_tcx(filename):
  tcx_namespace = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
  tree = ET.parse(filename)
  root = tree.getroot()

  # Extract trackpoints: lat, lon, distance, altitude
  points = []
  # d = 0.0
  prev_dist_m = 0.0
  for tp in root.findall('.//tcx:Trackpoint', tcx_namespace):
    lat_el = tp.find('tcx:Position/tcx:LatitudeDegrees', tcx_namespace)
    lon_el = tp.find('tcx:Position/tcx:LongitudeDegrees', tcx_namespace)
    dist_el = tp.find('tcx:DistanceMeters', tcx_namespace)
    alt_el = tp.find('tcx:AltitudeMeters', tcx_namespace)
    if lat_el is not None and lon_el is not None and dist_el is not None and alt_el is not None:
      current_dist_m = float(dist_el.text)
      delta_dist_m = max((current_dist_m - prev_dist_m), 0.0)
      # print(float(dist_el.text), delta_dist)
      points.append({
        'latitude': float(lat_el.text),
        'longitude': float(lon_el.text),
        'distance': delta_dist_m, # in meters
        'altitude': float(alt_el.text)
      })
      prev_dist_m = current_dist_m
      # d = d + delta_dist
  return points

# filename = './2023_Garmin_Gravel_Worlds_150_p_b_Lauf.tcx'
# points, d = parse_tcx(filename)
#print(points[:10])
#print(d / 1000)