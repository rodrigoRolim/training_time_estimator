import math
from models import PowerBalanceParameter
"""
  take the route L and divide it into n segments. In each segment, the rider should overcome the resistances forces calculate
  in the three function bellow. The sum of this three resistance forces multiply by velocity needed result in the energy necessary
  to overcome the resistances.
"""
power_aereo = lambda air_density, cda, velocity_relative: 0.5 * air_density * cda * velocity_relative ** 2
power_rolling = lambda total_mass, cr, gravity, slope: cr * total_mass * gravity * math.cos(slope)
power_climb = lambda total_mass, gravity, slope: total_mass * gravity * math.sin(slope)

def power_balance(power_balance_parameter: PowerBalanceParameter):
  velocity_relative = power_balance_parameter.current_velocity + power_balance_parameter.wind_component
  P_aero = power_aereo(
    power_balance_parameter.air_density, 
    power_balance_parameter.cda, 
    velocity_relative
  )
  P_rolling = power_rolling(
    power_balance_parameter.total_mass, 
    power_balance_parameter.cr, 
    power_balance_parameter.gravity, 
    power_balance_parameter.slope
  )
  P_climb = power_climb(
    power_balance_parameter.total_mass, 
    power_balance_parameter.gravity, 
    power_balance_parameter.slope
  )
  return (P_aero + P_rolling + P_climb) * power_balance_parameter.current_velocity

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
    if power_balance(PowerBalanceParameter(
      current_velocity=velocity_middle, 
      air_density=air_density, 
      cda=cda, 
      cr=cr, 
      wind_component=wind_component, 
      total_mass=total_mass, 
      gravity=gravity, 
      slope=slope
    )) > power:
      velocity_max = velocity_middle
    else:
      velocity_min = velocity_middle
  return velocity_middle