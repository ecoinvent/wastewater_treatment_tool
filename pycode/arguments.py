""" List of arguments that must be passed by the ICRA tool 

These should simply be passed as a dictionary of the following format: 
arg_dict = {'arg_name_1': arg_1_value,
            'arg_name_2': arg_2_value,
            ...
        }

"""
############################################
###########Required args####################
############################################


always_required_arguments = [
    'activity_name',
    'geography',
    'untreated_fraction',
    'tool_use_type',
    'PV',
    'CSO_particulate',
    'CSO_soluble',
    'fraction_C_fossil',
    'url',
    'technologies_averaged',
    'WW_properties',
    'chemicals',
    'electricity',
    'CSO_amounts',
    'WWTP_influent_properties',
    'WWTP_emissions_water',
    'WWTP_emissions_air',
    'WWTP_emissions_sludge',
    'sludge_properties',
    'untreated_as_emissions',
    'COD_TOC_ratio',
]
