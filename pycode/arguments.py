""" List of arguments that must be passed by the ICRA tool 

These should simply be passed as a dictionary of the following format: 
arg_dict = {'arg_name_1': arg_1_value,
            'arg_name_2': arg_2_value,
            ...
        }

In other words, you do not have to consider the data formats presented below:
these are for me.

THe arguments are listed here. Some are detailed below in the section 
"some details on more complicated arguments". 
"""
############################################
###########Required args####################
############################################

always_required_arguments = [
    "tool_use_type", # "average" or "specific". 
    "untreated_fraction", #float, [0, 1]
    "CSO_particulate", #float, [0, 1]
    "CSO_dissolved", #float, [0, 1],
    "CSO_amounts",
    "WW_type", #str, from (1) in http://84.89.61.64:8030/ecoinvent/simplified_data_entry.php
    "geography", #str id, see below
    "PV", #float,
    "WW_properties", #dict, see below
    "WWTP_influent_properties", #dict, see below,
    "WWTP_emissions_water", #dict, see below,
    "WWTP_emissions_air", #dict, see below,
    "sludge_amount", #float,
    "sludge_properties", #dict, see below,
    "electricity", #amount
    "FeCl3", #"amount"
    "acrylamide", #amount
    "NaHCO3", #amount
]


# args depending on whether we have a specific or average "tool_use_type"
specific_required_args = {
    'specific': [
        "technology_level_1", # str, ["aerobic, intensive", "aerobic, extensive", "anaerobic"]
        "technology_level_2", # str, built from "binary string", see LB email
        "capacity", # Class1, Class2, etc.
        "tech_description_specific_0", # See below
        "tech_description_specific_1", # See below
    ],
    'average': [
        "technologies_averaged", # Dict of the type {0:{fraction:x, technology_str:y, capacity:z, location:location}, 1:{...}}
    ]
}

# Ars that have defaults, but that we may want to inform based on data from user
optional_args = [
    "timePeriodStart", #TODO --> Should we use defaults (which?) or ask for this data in tool?
    "timePeriodEnd", #TODO --> Should we use defaults (which?) or ask for this data in tool?
]

############################################
#Some details on more complicated arguments#
############################################

"""############## Geographies ################
    id based on the selected location.
   See wastewater_treatment_tool\resources\geographies.json
"""


""" ########## CSO_amounts ################
    calculated emissions from CSO.
    emission_to_water_x are expressed as the `id` of the elementary flows.
    See either wastewater_treatment_tool\resources\emissions_to_water.json 
    your emissions to the required id

CSO_amounts = {
    "emission_to_water_1_id": "amount_1",
    "emission_to_water_2_id": "amount_2",
    ...
    }



    ############## WW_properties ################
    Amounts as entered by user AND as calculated by fractionation.
    The ids are found wastewater_treatment_tool\resources\WW_properties.json

WW_properties = {
    "prop_id_1": "amount_1",
    "prop_id_2": "amount_2",
 #   ...
    }

    ############## WWTP_influent_properties ################
    Amounts of WW pollutants in wastewater as it enters the WWTP.
    This is equal to the amount entered by the user (and adjusted with fractionation)
    minus CSO losses. The ids are the same as those found wastewater_treatment_tool\resources\properties.json
WWTP_influent_properties = {
    "prop_id_1": "amount_1",
    "prop_id_2": "amount_2",
 #   ...
    }
    


    ############## WWTP_emissions_water ################
    Emissions to water from WWTP, as calculated by "Marginal"
    !!! ALL RESULTS MUST BE EXPRESSED PER SPECIFIC m3 OF WASTEWATER (Q1) ENTERING THE WWTP
    The format is the same as for CSO_amounts (see wastewater_treatment_tool\resources\emissions_to_water.json for id)

    ############## WWTP_emissions_air ################
    Emissions to water from WWTP, as calculated by "Marginal"
    !!! ALL RESULTS MUST BE EXPRESSED PER SPECIFIC m3 OF WASTEWATER (Q1) ENTERING THE WWTP
    The format is the same as for CSO_amounts (see wastewater_treatment_tool\resources\emissions_to_air.json for id)

    
    
    ############## sludge_properties ################
    Sludge properties
    Use the 
    The format is the same as for CSO_amounts (see wastewater_treatment_tool\resources\emissions_to_air.json for id)
    
        
    
"""


###########################################
############Argument format: ##############
###########################################

technosphere_exchange_format = {
    'data': {
        'name':'valid_name_from_MD',
        'amount':'float',
        'comment':'str',
        },
    'properties': [
        'prop_dit_1',
        'prop_dict_2',
        'prop_dict_3'
        ],
    'uncertainty': {
        'variance':'float', 
        'pedigreeMatrix':['int','int', 'int','int','int'], #all ints in [1, 2, 3 4, 5]
        'comment': "str"
        }
}    

elementary_flow_exchange_format = {
    'data': {
        'name':'valid_name_from_MD',
        'compartment': 'compartment_name_from_MD',
        'subcompartment': 'subcompartment_name_from_MD',
        'amount':'float',
        'comment':'str',
        },
    'uncertainty': {
        'variance':'float', 
        'pedigreeMatrix':['int','int', 'int','int','int'], #all ints in [1, 2, 3 4, 5]
        'comment': "str"
        }
}

property_dict_format = {
    'name':'name property1, from MD',\
    'amount': 'amount property1, from tool, in proper units',\
    'unit': 'unit property1, from MD',\
    'comment':'str property1',\
    'uncertainty': 'uncertainty_dict property1'
}

uncertainty_dict = {
    'variance':'float', 
    'pedigreeMatrix':['int','int', 'int','int','int'], #all ints in [1, 2, 3 4, 5]
    'comment': "str"
    }

