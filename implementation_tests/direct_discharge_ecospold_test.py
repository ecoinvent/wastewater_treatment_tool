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
from pycode  import DirectDischarge_ecoSpold, WWT_ecoSpold
from pycode import defaults
#from pycode.placeholders import *


os.chdir(r'..')
root_dir = os.getcwd()
#print(root_dir)
sys.path.append(root_dir)


# Obligatory
temp_tool_use_type = 'average'
temp_untreated_fraction = 0.3
temp_CSO_particulate = {
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }
temp_CSO_dissolved={
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }
temp_CSO_amounts = {
    'f65558fb-61a1-4e48-b4f2-60d62f14b085': 0.005
    }
temp_WW_type = 'average'
temp_geography = 'GLO'
temp_PV = 10000
temp_WW_properties = {
        'dd13a45c-ddd8-414d-821f-dfe31c7d2868': 0.0006950881210075167,
        '3f469e9e-267a-4100-9f43-4297441dc726': 0.00039705575632341893,
        'efe22a60-b1a3-4b33-a5ba-4bf575e0a889': 0.00010407157626042784,
        'a547f885-601d-4d52-9bf9-60f0cef06269': 0.00019404032071619403,
        'f7fa53fa-ee5f-4a97-bcd8-1b0851afe9a6': 0.00010573692724599181,
        '4f461b9d-5a7b-4a46-8803-23f6df0dc522': 0.0002752476374165145,
        'c8ebc911-268a-4dfe-a426-73e1e35b587a': 0.0009628960051219199,
        '88c9f622-8451-41aa-98b0-c56b191a7e0a': 0.0006513361223486207,
        'cbc4a2c2-1710-4e6c-9b90-e1e72819d7b9': 0.00099982944144738,
        'f04a971d-f503-4ca0-b2b1-0ecd2e53ea61': 3.6652735422261216e-05,
        '7fe01cf6-6e7b-487f-b37e-32388640a8a4': 0.0006562458014476974,
        '1e4ef691-c7d3-49fc-9aee-6d77575a7b8a': 0.0006622034342957929,
        '8175120e-a5b7-4f19-afca-5620e9e4dd8b': 0.0003309085411166807,
        '7f3410da-b91e-40d8-9545-ab269ff66900': 0.0007137440867422037,
        'c0447419-7139-44fe-a855-ea71e2b78585': 0.0009501836807688239,
        '0f205308-d33a-430b-b3ec-b62bef311f2f': 0.0009428764195810917,
        '8e73d3fb-bb81-4c42-bfa6-8be4ff13125d': 0.0005734478654127366,
        '4d60d7ca-8f4b-4d14-b137-3670858e48ca': 9.255780037230077e-05,
        '98549452-463c-463d-abee-a95c2e01ade3': 0.0009804561211974557
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
temp_electricity = 42
temp_FeCl3 = 12
temp_NaHCO3 = 666
temp_acrylamide = 99


# Specific to "average" case
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

test_inputs_average = {
    "root_dir": root_dir,
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
    "technologies_averaged": temp_technologies_averaged,
    "electricity": temp_electricity,
    "FeCl3": temp_FeCl3,
    "NaHCO3": temp_NaHCO3,
    "acrylamide": temp_acrylamide
}
direct_discharge_test = DirectDischarge_ecoSpold(**test_inputs_average)
treatment_test = WWT_ecoSpold(**test_inputs_average)

direct_discharge_test.generate_ecoSpold2()
treatment_test.generate_ecoSpold2()

