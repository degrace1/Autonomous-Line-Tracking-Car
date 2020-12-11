# Autonomous Line Tracking Car at civilian priority level

import os
import sys
sys.path.append(os.path.relpath("./libraries"))

from decision import *

HIGH_PRIO_LEVEL = 0
CIVILIAN_LEVEL = 2 

# run the car at low priority level
civilian = Decision(CIVILIAN_LEVEL)
civilian.run()