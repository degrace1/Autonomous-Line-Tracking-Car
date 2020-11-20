import numpy as np
def dVision(radius):
    return -0.1424 - (-0.013599/0.06828606)(1 - np.pow(e,-0.06828606 * (1/radius)))
    