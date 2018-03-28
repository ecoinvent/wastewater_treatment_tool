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

temp_tool_use_type = 'average'
temp_untreated_fraction = 0.3
temp_CSO_particulate = {
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }
temp_CSO_dissolved={
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }

temp_WW_type = 'average'

temp_geography = 'GLO'
temp_PV = 10000
temp_PV_comment = 'Some PV comment'
temp_technologies_averaged = {
    0: {
        'fraction':0.4,
        'technology_str': "The auto_generated string representing tech 0",
        'capacity': "Class 1 (over 100,000 per-capita equivalents)",
        'location': 'Spain',
        },
    1: {
        'fraction':0.6,
        'technology_str': "The auto_generated string representing tech 1",
        'capacity': "Class 2 ( 50,000 to 100,000 per-capita equivalents)",
        'location': 'Spain',
         },
    }
temp_CSO_amounts = {
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }
temp_WW_properties = {
    'a547f885-601d-4d52-9bf9-60f0cef06269': 0.011
    }
temp_WWTP_influent_properties = {
    'a547f885-601d-4d52-9bf9-60f0cef06269': 0.01
    }
temp_WWTP_emissions_water = {
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }

temp_WWTP_emissions_air = {
    'f9749677-9c9f-4678-ab55-c607dfdc2cb9': 0.005}
temp_sludge_amount = 0.5
temp_sludge_properties = {
    'a547f885-601d-4d52-9bf9-60f0cef06269': 0.42
    }
test_inputs_average = {
    "tool_use_type": temp_tool_use_type,
    "untreated_fraction": temp_untreated_fraction,
    "CSO_particulate": temp_CSO_particulate,
    "CSO_amounts": temp_CSO_amounts,
    "CSO_dissolved": temp_CSO_dissolved,
    "WW_type": temp_WW_type,
    "geography": temp_geography,
    "PV": temp_PV,
    "WW_properties": temp_WW_properties,
    "WWTP_influent_properties": temp_WWTP_influent_properties,
    "WWTP_emissions_water": temp_WWTP_emissions_water,
    "WWTP_emissions_air": temp_WWTP_emissions_water,
    "sludge_amount": temp_sludge_amount,
    "sludge_properties": temp_sludge_properties,
    "technologies_averaged": temp_technologies_averaged
}

direct_discharge_test = DirectDischarge_ecoSpold(**test_inputs_average)