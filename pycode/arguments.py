""" List of arguments that must be passed by the ICRA tool"""


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
untreated_fraction = 0.2 # float, represents the fraction emitted directly to the environment
overload_loss_fraction_particulate = 0.01
overload_loss_fraction_dissolved = 0.02

########################################################################
# Metadata
########################################################################
WW_type = 'lime production'
technology = 'average'
capacity = 'average'
geography = 'GLO'
timePeriodStart = '1995-01-01'
timePeriodEnd = '2025-12-31'



