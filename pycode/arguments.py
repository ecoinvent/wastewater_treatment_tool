""" List of arguments that must be passed by the ICRA tool"""
required_arguments = [
    "root_dir", # Root directory of data and code
    "tool_use_type", # "average" or specific
    "untreated_fraction", #float, [0, 1]
    "overload_loss_fraction_particulate", #float, [0, 1]
    "overload_loss_fraction_dissolved", #float, [0, 1]
    "WW_type", #str, from (1) in http://84.89.61.64:8030/ecoinvent/simplified_data_entry.php
    "geography", #str
    "timePeriodStart", #TODO --> Should we use defaults (which?) or ask for this data in tool?
    "timePeriodEnd", #TODO --> Should we use defaults (which?) or ask for this data in tool?
    
other_args = {
    'specific': [
        "technology", # str, TODO
        "capacity", # Class1, Class2, etc.
    ],
    'average': [
    ]
}
        

required_arguments_specific_use = [
    "technology", # str, TODO
    "capacity", # Class1, Class2, etc.
    

    

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
timePeriodStart = '1995-01-01'
timePeriodEnd = '2025-12-31'



