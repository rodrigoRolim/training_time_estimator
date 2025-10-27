import math

"""
  take the route L and divide it into n segments. In each segment, the rider should overcome the resistances forces calculate
  in the three function bellow. The sum of this three resistance forces multiply by velocity needed result in the energy necessary
  to overcome the resistances.
"""
power_aereo = lambda air_density, cda, velocity_relative: 0.5 * air_density * cda * velocity_relative ** 2
power_rolling = lambda total_mass, cr, gravity, slope: cr * total_mass * gravity * math.cos(slope)
power_climb = lambda total_mass, gravity, slope: total_mass * gravity * math.sin(slope)

def power_balance(
  current_velocity,
  air_density,
  cda,
  cr,
  wind_component,
  total_mass,
  gravity,
  slope
):
  velocity_relative = current_velocity + wind_component
  P_aero = power_aereo(air_density, cda, velocity_relative)
  P_rolling = power_rolling(total_mass, cr, gravity, slope)
  P_climb = power_climb(total_mass, gravity, slope)
  return (P_aero + P_rolling + P_climb) * current_velocity

def get_steady_state_velocity(
  power, 
  air_density, 
  cda, 
  cr, 
  wind_component, 
  total_mass, 
  gravity, 
  slope
):
  velocity_min, velocity_max = 0.1, 25 # m/s | ~0.36 - 90 km/h

  for _ in range(40):
    velocity_middle = (velocity_min + velocity_max) / 2
    if power_balance(velocity_middle, air_density, cda, cr, wind_component, total_mass, gravity, slope) > power:
      velocity_max = velocity_middle
    else:
      velocity_min = velocity_middle
  return velocity_middle