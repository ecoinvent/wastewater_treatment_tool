"""
###################################
Untreated fraction dataset creation
###################################

Current status:
- temporary (placeholder) arguments and defaults
- No adding of CSO and untreated values (waiting for inputs)
- Generates ecoSpold
"""

import os
import sys 

#os.chdir(r'..')
#root_dir = os.getcwd()
#print(root_dir)
sys.path.append("..")

from pycode  import DirectDischarge_ecoSpold
from pycode.placeholders import *
from pycode.defaults import *

test_inputs_average = {
    'untreated_fraction': temp_untreated_fraction, #float, [0, 1]
    'tool_use_type': 'average', # "average" or specific
    'CSO_particulate': temp_overload_loss_fraction_particulates,
    'CSO_dissolved': temps_overload_loss_fraction_dissolved,
    'WW_type': temp_MW_type,
    'geography': temp_loc,
    'PV': temp_PV,
    'PV_comment': temp_PV_comment,
    'PV_uncertainty': temp_PV_uncertainty,
    'technologies_averaged': temp_technologies_averaged,
    'WW_properties': temp_obligatory_properties,
}

direct_discharge_test = DirectDischarge_ecoSpold(**test_inputs_average)