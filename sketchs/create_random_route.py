import pandas as pd
import numpy as np

def create_route(num_segments=50, step_degress=45): 
  random_generator = np.random.default_rng(42)

  distances = random_generator.uniform(0.5, 8.0, num_segments).round(2) # km per segment
  grades = random_generator.uniform(-6, 8, num_segments).round(1) # percent slope
  headings = random_generator.choice(np.arange(0, 360, step_degress), num_segments) # every 45 degree step

  route = list(zip(distances, grades, headings))

  return route
