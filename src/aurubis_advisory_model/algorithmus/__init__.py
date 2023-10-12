# Algorithm Module initialization for Advisory Frontend
# Created by Tianxiang Lan @ ?? Sept 2023
# This file initiates the algorithm which will be invoked in the the frontends routes.

# Library imports

# Module imports
from connectors import instantiated_osipiconnector # Use this instantiated connector to retrieve data

# Configuration imports
from config import (
    OSI_PI_PARAMETERS_HANDLING, # Should you need more parameters that potentially are parameters, please put them in the config.py file and import from there.
)