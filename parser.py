import xml.etree.ElementTree as ET

def parse_tcx(filenam):
  ns = {'txc': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
  tree = ET.parse(filename)
  root = tree.getroot()

  # Extract trackpoints: lat, lon, distance, altitude
  points = []
  for tp in root.findall('.//tcx:Trackpoint', ns):
    lat_el = tp.find('tcx:Position/tcx:LatitudeDegrees', ns)
    lon_el = tp.find('tcx:Position/tcx:LongitudeDegrees', ns)
    dist_el = tp.find('tcx:DistanceMeters', ns)
    alt_el = tp.find('tcx:AltitudeMeters', ns)