"""Some placeholder values while we wait for tool to generate the right input"""

# Root directory of data and code
temp_root_dir = r'C:\mypy\code\wastewater_treatment_tool'

# Technology descriptions for average
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
    

temp_samplingProcedure_text_treat = \
"TODO: Text describing the sampling and calculation procedures applied for " +\
"quantifying the exchanges. Reports whether the sampling procedure for " +\
"particular elementary and intermediate exchanges differ from the general " +\
"procedure. Mentions possible problems in combining different sampling procedures."

temp_extrapolations_text_treat = \
"Describes extrapolations of data from another time period, another " +\
"geographical area or another technology and the way these extrapolations " +\
"have been carried out. It should be reported whether different "+\
"extrapolations have been done on the level of individual exchanges. "+\
"If data representative for a activity operated in one country is used "+\
"for another country's activity, its original representativity can be "+\
"indicated here. Changes in mean values due to extrapolations may also be "+\
"reported here."

temp_PV = 1000000
temp_PV_comment = "Comment about how PV was calculated"
temp_PV_uncertainty = {
    'variance':0, 
    'pedigreeMatrix':[1,1,1,1,1],
    'comment': "TODO_temp  uncertainty"
    }

temp_tool_use_type = 'average' # or specific
temp_untreated_fraction = 0.2 # float, represents the fraction emitted directly to the environment
temps_overload_loss_fraction_dissolved=0.01 # float
temp_overload_loss_fraction_particulates =0.02# float
temp_MW_type='average',
#technology = 'average'
#capacity = 'average'
temp_loc='GLO'


# Properties format needs to change to dict!
temp_WW_obligatory_properties = [
    ('carbon content, fossil',
     0.01,
     'dimensionless',
     'ICRA comment',
     {'variance':0.01, 'pedigreeMatrix':[2,4,3,2,4],'comment':""}
    ),
    ('carbon content, non-fossil',
     0.01,
     'dimensionless',
     'ICRA comment',
     {'variance':0.01, 'pedigreeMatrix':[2,4,3,2,4],'comment':"ICRA comment"}
    ),
    ('dry mass',
     0.01,
     'kg',
     'ICRA comment',
     {'variance':0.6, 'pedigreeMatrix':[2,4,3,2,4],'comment':"ICRA comment"}
    ),
    ('water content',
     0.01,
     'dimensionless',
     'ICRA comment',
     {'variance':0.01, 'pedigreeMatrix':[2,4,3,2,4],'comment':"ICRA comment"}
    ),
    ('water in wet mass',
     999.99,
     'kg',
     'ICRA comment',
     {'variance':0.01, 'pedigreeMatrix':[2,4,3,2,4],'comment':"ICRA comment"}
    ),
    ('wet mass',
     1000,
     'kg',
     'ICRA comment',
     {'variance':0.01, 'pedigreeMatrix':[2,4,3,2,4],'comment':"ICRA comment"}
    )    
]