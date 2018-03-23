""" List of arguments that must be passed by the ICRA tool"""
required_arguments = [
    "root_dir", # Root directory of data and code
    "tool_use_type", # "average" or specific
    "untreated_fraction", #float, [0, 1]
    "overload_loss_fraction_particulate", #float, [0, 1]
    "overload_loss_fraction_dissolved", #float, [0, 1]
    "WW_type", #str, from (1) in http://84.89.61.64:8030/ecoinvent/simplified_data_entry.php
    "geography", #str
]
    
other_required_args = {
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

optional_args = [
    "timePeriodStart", #TODO --> Should we use defaults (which?) or ask for this data in tool?
    "timePeriodEnd", #TODO --> Should we use defaults (which?) or ask for this data in tool?
]

########################################################################
# General
########################################################################

# Root directory of data and code
root_dir = r'C:\mypy\code\wastewater_treatment_tool'

########################################################################
# Loading master data
########################################################################
# None if we stick to the proposed directory structure 

########################################################################
# High-level parameters
########################################################################
tool_use_type = "average" # or specific. 

untreated_fraction = 0.2 # float, represents the fraction emitted directly to the environment
overload_loss_fraction_particulate = 0.01 # float
overload_loss_fraction_dissolved = 0.02 # float

########################################################################
# Metadata
########################################################################
WW_type = 'lime production'
technology = 'average'
capacity = 'average'
geography = 'GLO'

default_tech_description_specific_1 = "Some automatic text here to describe technology" #TODO
default_tech_description_specific_2 = "Some automatic text here provide some details on parameters used" #TODO



