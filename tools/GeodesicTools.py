from math import radians, cos, sin, atan2, sqrt


def getDistance(x1, x2): #  Haversine formula
  R = 6378137 #  Earth’s mean radius in meter
  dLong = radians(x2[0] - x1[0])
  dLat = radians(x2[1] - x1[1])
  a = sin(dLat / 2) * sin(dLat / 2) + cos(radians(x1[1])) * cos(radians(x2[1])) * sin(dLong / 2) * sin(dLong / 2)
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  d = R * c
  return d #  returns the distance in meter