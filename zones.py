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