"""
Let the route L be divided into n segments.
For each segment i the rider must overcome the main resistive forces:
 - Ftotal_i = Fd_i +Fr_i + Fg_i

where:
  1. Aerodynamic drag: Fd_i = 0.5 * p * CdA * (v_i + vwind_i)^2
  2. Rolling resistance: Fr_i = Cr * m * g * cos(teta_i)
  3. Gravitational component: Fg_i = m * g * sin(teta_i)

where
  1. p is the air density approximately 1.225 kg/m^3 at a sea level;
  2. CdA is the coefficiente of drag vs frontal area (m^2)
  3. v_i is the ground speed in the i segment (m/s)
  4. vwind_i is the wind component along direction of motion (positive for headwind, negative for tailwind)
  5. Cr is the rolling coefficient (~ 0.0004 - 0.0006 for road tires)
  6. m is the total mass = rider mass + bike mass
  7. g is the gravity = 9.80665 m/s^2
  8. teta_i is the slope angle in the i segment

The power required to maintain a steady velocity v_i in segment i is given by:
  - P_i = Ftotal_i * v_i 

Given a constant available power P_available (tipically a fraction of FTP), the steady-state velocity v_i can be estimated 
by solving this P_i(v_i) = P_available

Finally, the time to complete segment i is t_i = d_1 / v_i, where d_i is the distance in meters

So the total estimated time to complete the route L is
  - T = sum(t_i)

This equation is not complete yet, cause i think we should consider the 'rider fatigate' too in this math.

There are two estimator function based on FTP: one with constant FTP and other with dynamic FTP conforme the zones

The route is build by a list of tuple (x, y, z) where x is the distance; y is the gradient (uphill or downhill) and z is the headings

the powers.py file determine the resistance forces and the steady-velocity
the create_random_route.py file create route in segments randomly
the zones.py file define the zones based on the grade
the training_time_estimator estimate the time needed to complete the route create randomly

I create the algorithm in python just for representation. All this code will be convert to rust language for desktop application
"""

from training_time_estimator import estimate_training_time_dynamic_ftp, estimate_training_time_static_ftp
from create_random_route import create_route

route = create_route(50, 30) # create a route with 50 segments and 30° by step

# FTP varies based on zones. I think this version is more realistic
time_d_ftp, dist_d_ftp, details_d_ftp = estimate_training_time_dynamic_ftp(
  ftp=250, # in watts
  route_segments=route,
  wind_speed=10, # m/s
  wind_dir=90, # wind direction in angle 0° = winds come from north; 90° = from East; 180° = from South; 270° = from west (just examplification)
  rider_mass=75, # the rider mass
  bike_mass=8 # the bike mass
)
# FTP is constant here
time_s_ftp, dist_s_ftp, details_s_ftp = estimate_training_time_static_ftp(
  ftp=250,
  route_segments=route,
  wind_speed=10,
  wind_dir=90,
  rider_mass=75,
  bike_mass=8
)

hours_d_ftp, minutes_d_ftp = time_d_ftp
hours_s_ftp, minutes_s_ftp = time_s_ftp
print(f"Estimated time for dynamic ftp based on zones: {hours_d_ftp}h {minutes_d_ftp}m")
print(f"Distance: {dist_d_ftp}km")
print("--------")
print(f"Estimated time for static ftp: {hours_s_ftp}h {minutes_s_ftp}m")
print(f"Distance: {dist_s_ftp}km")
