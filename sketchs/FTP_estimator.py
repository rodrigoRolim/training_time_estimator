"""
Banister's performance model was used to compute the historical ride data of the rider

First, the metrics average power and total time are extracted from tcx file. And then applied in the
following formula TSS ~= ((total_time_sec * average_power) / (FTP_base / 3600)) * 100. This formula compute
the Training Stress Score (TSS) for each activity. This output will be used to compute the Chronic Training Load
(CTL), the Acute Training Load (ATL) and then the Training Stress Balance (TSB).

- CTL + (TSS - CTL) / 42
- ATL + (TSS - ATL) / 7
- TSB = CTL - ATL

1. CTL (Chronic Training Load) represents long-term fitness.
  it is weighted avegarage of past TSS values, where recent rides matter more than rides from months ago
  the weight decays exponentially over time
  CTL is an exponentially weighted moving average (EWMA) of TSS:
    CTL_t = CTL_t-1 + (TSS_t - CTL_t-1) / T
2. 
if the TSB is negative, then decrease the effective FTP proporcionally
if the TSB is positve, then encrease the effective FTP proporcionally

"""

import xml.etree.ElementTree as ET
from datetime import datetime
import glob
import numpy as np

def get_normalized_power(watts, window=30):
  watts = np.array(watts, dtype=float)
  rolling_mean = np.convolve(watts, np.ones(window) / window, mode='valid') # moving average
  rolling_fourth_power = rolling_mean ** 4
  return (np.mean(rolling_fourth_power)) ** 0.25

def get_TSS_from_tcx_file(file_path, FTP_BASE=250):
  if FTP_BASE <= 0:
    return 0

  tree = ET.parse(file_path)
  root = tree.getroot()
  tcx_namespace = {
    'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    'ext': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
  }

  total_time = float(root.find('.//tcx:TotalTimeSeconds', tcx_namespace).text)
  watts = []

  for watt in root.findall('.//ext:Watts', tcx_namespace):
    try:
      watts.append(float(watt.text))
    except:
      continue
  
  np_value = get_normalized_power(watts)

  # compute approximate TSS
  IF = np_value / FTP_BASE # intensity force
  duration_hours = total_time / 3600
  TSS = duration_hours * (IF ** 2) * 100

  # Extract start time
  start_time_str = root.find('.//tcx:Lap', tcx_namespace).get('StartTime')
  start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))

  return {"date": start_time.date(), "TSS": TSS}

def get_tss_list(root_path=".", FTP_BASE=250):
  TSS_LIST = []
  # Read all TCX files
  for file in glob.glob(f"{root_path}/*.tcx"):
    TSS_LIST.append(get_TSS_from_tcx_file(file, FTP_BASE))

  # Sort by date
  TSS_LIST.sort(key=lambda x: x['date'])

  return TSS_LIST

# compute CTL, ATL and TSB
# CTL chronic training load
def compute_CTL(TSS, current_ctl):
  return current_ctl + (TSS - current_ctl) / 42  # 42-day constant

# ATL acute training load
def compute_ATL(TSS, current_atl):
  return current_atl + (TSS - current_atl) / 7 # 7-day

# TSB training stress balance
def compute_TSB(CTL, ATL):
  return CTL - ATL

def get_metrics_list(root_path='.', FTP_BASE=250):
  TSS_LIST = get_tss_list(f'{root_path}', FTP_BASE) # the TSS_LIST must be a constant persisted into DB
  CTL, ATL = 0, 0
  CTL_LIST, ATL_LIST, TSB_LIST = [], [], []

  for i, tss_entry in enumerate(TSS_LIST):
    TSS = tss_entry['TSS']

    # Apply exponential moving averages
    CTL = compute_CTL(TSS, CTL)
    ATL = compute_ATL(TSS, ATL)
    TSB = compute_TSB(CTL, ATL)

    tss_entry['CTL'] = CTL
    tss_entry['ATL'] = ATL
    tss_entry['TSB'] = TSB
  
  return TSS_LIST

def adjust_ftp_using_TSB(latest_tsb, FTP_BASE=250):
  k1 = 0.005 # scaling factor
  effective_ftp = max(FTP_BASE * (1 + k1 * latest_tsb), FTP_BASE * 0.85) # limit minimum
  return effective_ftp

def update_ftp(FTP_BASE = 250, historic_file="."):
  TSS_LIST = get_metrics_list(historic_file, FTP_BASE)
  adjusted_ftp = adjust_ftp_using_TSB(TSS_LIST[-1]['TSB'], FTP_BASE)

  return adjusted_ftp

# print(adjusted_ftp)
# for e in TSS_LIST:
#  print(f"{e['date']}: TSS={e['TSS']:.1f}, CTL={e['CTL']:.1f}, ATL={e['ATL']:.1f}, TSB={e['TSB']:.1f}")

"""
A future table to persist the ride historic used to updated FTPs a long the time
date            ride date
distance_km     Total distance of ride
total_time_sec  Duration
avg_power       Average power (watts)
avg_heart_rpm   Average heart rate
TSS             Training Stress Score
CTL             Chronic Training Load
ATL             Acute Training Load
TSB             Training Stress Balance
route_name      Route name
effective_ftp   FTP adjusted for fatigue
"""