import numpy as np
import math 

def dVision(radius):
    v = math.exp(-12.48963 * (1/radius))
    d = -8.974553 - (-2003.164/12.48963)*(1 - v)
    return d
    