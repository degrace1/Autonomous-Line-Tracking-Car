# Autonomous Line Tracking Car at high priority level

import os
import sys
sys.path.append(os.path.relpath("./libraries"))

from decision import *

HIGH_PRIO_LEVEL = 0
CIVILIAN_LEVEL = 2 

# run the car at  high priority level
high = Decision(HIGH_PRIO_LEVEL)
high.run()