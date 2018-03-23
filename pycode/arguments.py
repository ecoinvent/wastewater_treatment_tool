""" List of arguments that must be passed by the ICRA tool"""

# Always required args
required_arguments = [
    "root_dir", # Root directory of data and code
    "tool_use_type", # "average" or specific
    "untreated_fraction", #float, [0, 1]
    "overload_loss_fraction_particulate", #float, [0, 1]
    "overload_loss_fraction_dissolved", #float, [0, 1]
    "WW_type", #str, from (1) in http://84.89.61.64:8030/ecoinvent/simplified_data_entry.php
    "geography", #str
    "PV", #float,
    "WW_obligatory_properties",
]

# args depending on whether we have a specific or average "tool_use_type"
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

# Ars that have defaults, but that we may want to inform based on data from user
optional_args = [
    "timePeriodStart", #TODO --> Should we use defaults (which?) or ask for this data in tool?
    "timePeriodEnd", #TODO --> Should we use defaults (which?) or ask for this data in tool?
]

###########################################
############Argument format: ##############
###########################################

technosphere_exchange_format = {
    'name':'valid_name_from_MD',
    'amount':'float',
    'comment':'str',
    'properties': ['prop_dit_1', 'prop_dict_2',  'prop_dict_3'], #...
    'uncertainty': 'uncertainty_dict'
}    

elementary_flow_exchange_format = {
    'name':'valid_name_from_MD',
    'compartment': 'compartment_name_from_MD',
    'subcompartment': 'subcompartment_name_from_MD',
    'amount':'float',
    'uncertainty': 'uncertainty_dict',
    'comment':'str',
}

property_dict_format = {
    'property_name':'name property1, from MD',\
    'amount': 'amount property1, from tool, in proper units',\
    'unit': 'unit property1, from MD',\
    'comment':'str property1',\
    'uncertainty_dict': 'uncertainty_dict property1'
}

uncertainty_dict = {
    'variance':'float', 
    'pedigreeMatrix':['int','int', 'int','int','int'], #all ints in [1, 2, 3 4, 5]
    'comment': "str"
    }

