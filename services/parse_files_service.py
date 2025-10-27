from models import ParseTcxFileOptions
import xml.etree.ElementTree as ET

# 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
def parse_tcx_to_segmented_route(file_path):
  tcx_namespace = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
  tree = ET.parse(file_path)
  root = tree.getroot()

  # Extract trackpoints: lat, lon, distance, altitude
  points = []

  prev_dist_m = 0.0
  for tp in root.findall('.//tcx:Trackpoint', tcx_namespace):
    lat_el = tp.find('tcx:Position/tcx:LatitudeDegrees', tcx_namespace)
    lon_el = tp.find('tcx:Position/tcx:LongitudeDegrees', tcx_namespace)
    dist_el = tp.find('tcx:DistanceMeters', tcx_namespace)
    alt_el = tp.find('tcx:AltitudeMeters', tcx_namespace)

    if lat_el is not None and lon_el is not None and dist_el is not None and alt_el is not None:
      current_dist_m = float(dist_el.text)
      delta_dist_m = max((current_dist_m - prev_dist_m), 0.0)

      points.append({
        'latitude': float(lat_el.text),
        'longitude': float(lon_el.text),
        'distance': delta_dist_m, # in meters
        'altitude': float(alt_el.text)
      })
      
      prev_dist_m = current_dist_m

  return points