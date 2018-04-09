import os
import sys
import json
import pprint
from wastewater_treatment_tool.pycode import DirectDischarge_ecoSpold
from wastewater_treatment_tool.pycode.defaults import *

#!/usr/bin/env python3

#print python version before local imports
print("Running Python",sys.version.split(' ')[0],'\n')

#folder with python packages
sys.path.append("../../../opt/python3/")
#set root_dir #TODO Lluis
os.chdir('..')
root_dir = os.getcwd()


'''
 Receive a json string from stdin
'''
#debug: print input string
#print('input string: ',sys.argv[1].encode('ascii','ignore').decode('ascii'))

#parse json
received_json = json.loads(sys.argv[1])
#print('parsed JSON object: ',json.dumps(received_json, indent=4, sort_keys=True))

'''
 Untreated fraction dataset creation
'''
untreated_fraction = received_json['untreated_fraction']
CSO_particulate    = {'f65558fb-61a1-4e48-b4f2-60d62f14b085': received_json['CSO_particulate']['value'] / 100}
CSO_dissolved      = {'f65558fb-61a1-4e48-b4f2-60d62f14b085': received_json['CSO_soluble']['value'] / 100}
geography          = received_json['geography']
PV                 = received_json['PV']['value']

CSO_amounts = { } #discharged CSO amounts

for i in received_json['CSO_amounts']:
  if 'ecoinvent_id' in i: CSO_amounts.update({i['ecoinvent_id'] : i['value'] })

WW_properties = { } #properties before CSO
for i in received_json['WW_properties']:
  if 'ecoinvent_id' in i: WW_properties.update({i['ecoinvent_id'] : i['value'] })


# TODO - get these arguments from tool
"""'''

WWTP_influent_properties = { } #properties after CSO
tool_use_type      = 'average'
WW_type            = 'average'
PV_comment         = 'Some PV comment'
technologies_averaged = {
  0: {
      'fraction':0.4,
      'technology_str': "The auto_generated string representing tech 0",
      'capacity': "Class 1 (over 100,000 per-capita equivalents)",
      'location': 'Spain',
    },
  1: {
      'fraction':0.6,
      'technology_str': "The auto_generated string representing tech 1",
      'capacity': "Class 2 (50,000 to 100,000 per-capita equivalents)",
      'location': 'Spain',
    },
}
WWTP_emissions_water = { }
WWTP_emissions_air   = { }
sludge_amount        = 0
sludge_properties    = { }
electricity          = 0
FeCl3                = 0
acrylamide           = 0
NaHCO3               = 0
"""

inputs = {
  "tool_use_type":             tool_use_type,
  "untreated_fraction":        untreated_fraction,
  "CSO_particulate":           CSO_particulate,
  "CSO_amounts":               CSO_amounts,
  "CSO_dissolved":             CSO_dissolved,
  "WW_type":                   WW_type,
  "geography":                 geography,
  "PV":                        PV,
  "WW_properties":             WW_properties,
  "WWTP_influent_properties":  WWTP_influent_properties,
  "WWTP_emissions_water":      WWTP_emissions_water,
  "WWTP_emissions_air":        WWTP_emissions_water,
  "sludge_amount":             sludge_amount,
  "sludge_properties":         sludge_properties,
  "technologies_averaged":     technologies_averaged,
  "electricity":               electricity,
  "FeCl3":                     FeCl3,
  "acrylamide":                acrylamide,
  "NaHCO3":                    NaHCO3,
}

'''
pretty printer (debug)
'''
pp=pprint.PrettyPrinter(indent=2)
pp.pprint(inputs)


untreated = DirectDischarge_ecoSpold(root_dir, **args)
treated = WWT_ecoSpold(root_dir, **args)
result = {
        'untreated': DirectDischarge_ecoSpold.generate_ecoSpold2(),
        'treated': WWT_ecoSpold.generate_ecoSpold2(),
    }
