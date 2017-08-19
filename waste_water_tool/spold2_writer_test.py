


"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXX
    DUMMY INPUT DATA
XXXXXXXXXXXXXXXXXXXXXXXXXXXX    
"""

# Temporary
generic_uncertainty_comment = "Comment about how uncertainty was estimated"

# WW properties in pandas dataframe, currently stored in an excel file.
WW_prop_df = get_WW_properties()

# Untreated fraction
untreated_fraction = 0.3  
untreated_fraction_uncertainty = {'variance':0.01,
                                  'pedigreeMatrix':[2,4,3,2,4],
                                  'comment': generic_uncertainty_comment,
                                 }
# Hydraulic overload
overload_loss_fraction_particulate = 0.01
overload_loss_fraction_dissolved = 0.02
overload_loss_fraction_particulate_uncertainty = {'variance':0.01,
                                                  'pedigreeMatrix':[2,4,3,2,4],
                                                  'comment': generic_uncertainty_comment,
                                                  }
overload_loss_fraction_dissolved_uncertainty = {'variance':0.01,
                                                'pedigreeMatrix':[2,4,3,2,4],
                                                'comment': generic_uncertainty_comment,
                                                }

# Name parameters
WW_type = "from ceramic production"
technology = "average"
capacity = 5e9

# Geography
geography = 'GLO'

# Time period
start = '1995-01-31'
end = '2020-12-31'

# Technology level
treatDS_technology_level = 'Current'

# Comments
treatDS_tech_comment_1 = "The technologies modelled are x and y"
treatDS_tech_comment_2 = "They were averaged based on z"
treatDS_tech_comment_3 = "These technologies rock"

treatDS_general_comment_1 = \
"This dataset represents the treatment of wastewater "\
"discharged to the sewer grid {}".format(
        treatment_dataset['WW_type']
        )
treatDS_general_comment_2 = \
"It includes the transportation of the wastewater to the "
"wastewater treatment plant and the actual treatment."

treatDS_general_comment_3 = \
"It was modelled using XYZ"

treatDS_time_period_comment = ['']
treatDS_geography_comment = ['']

# Representativeness
treatDS_samplingProcedure_text = \
"This is a description of the sampling procedure, "
"and it should be changed by IRCA"

treatDS_extrapolation_text = \
"This is a description of the sampling procedure, "
"and it should be changed by IRCA"

treatDS_representativeness_percent = 80

# Reference exchange production volume
total_PV = 1000000
total_PV_uncertainty= {
        'variance':0.01,
        'pedigreeMatrix':[2,4,3,2,4]
        }


"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXX
   Suggested boilerplate
XXXXXXXXXXXXXXXXXXXXXXXXXXXX    

"""
# Included activities
treatDS_includedActivitiesStartText = "From the discharge of wastewater "\
                                      "{} to the sewer grid.".format(
                                              treatment_dataset['WW_type']
                                              )
treatDS_includedActivitiesEndText_last =\
"This activity ends with the discharge of treated wastewater to the natural environment."

treatDS_includedActivitiesEndText_included =\
"This activity includes the transportation of wastewater via the sewer grid, "\
"and the treatment of the wastewater in the wastewater treatment plant."\
"The amounts of infrastructure and consumables are also included as inputs to the activity."

treatDS_includedActivitiesEndText_excluded = \
" By definition, wastewater not sent to the sewer grid is also excluded. "\
"The fraction of wastewater discharged to the sewer grid but ultimately not treated because the sewer is "\
"unconnected and direct emissions due to hydraulic overload are also excluded. "\
"These are included in another dataset specifically covering the discharge of untreated wastewater. "\
"The production of sludge is included, but its treatment is covered by another treatment activity."

# Reference exchange
treatDS_ref_exchange_comment =\
"Refers to the amount of wastewater treated in the wastewater treatment plant."

# Reference exchange production volume
treatDS_PV_comment = "Yearly volume of wastewater treated."
if untreated_fraction != 0:
    treatDS_PV_comment +=\
    " Excludes the fraction that is discharged "\
    "directly to the environment ({:.0f}%).".format(
        untreated_fraction*100)


"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXX
Code execution - MD
XXXXXXXXXXXXXXXXXXXXXXXXXXXX    
"""

# Generate Master data
MD = get_current_MD(return_MD=True)

"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXX
Code execution - Treatment
XXXXXXXXXXXXXXXXXXXXXXXXXXXX    
"""

# Generate the empty dataset
treatment_dataset = create_empty_dataset()

# add name
treatment_dataset = generate_WWT_activity_name(treatment_dataset,
                                               WW_type,
                                               technology,
                                               capacity)
# add nameId
generate_activityNameId(treatment_dataset, MD)

# add geography
generate_geography(treatment_dataset, MD, geography)

# add datasetId
generate_dataset_id(treatment_dataset)

# Generate the genericObject for ecoSpold creation
generate_activityIndex(treatment_dataset)

# Add boundary text
generate_activity_boundary_text(treatment_dataset,
                               treatDS_includedActivitiesStartText,
                               treatDS_includedActivitiesEndText_last,
                               treatDS_includedActivitiesEndText_included,
                               treatDS_includedActivitiesEndText_excluded)
# Technology comment
generate_comment(treatment_dataset,
                 'technologyComment',
                 [treatDS_tech_comment_1,
                  treatDS_tech_comment_2,
                  treatDS_tech_comment_3,
                  ]
                 )

# General comment
generate_comment(treatment_dataset,
                 'generalComment',
                 [treatDS_general_comment_1,
                  treatDS_general_comment_2,
                  treatDS_general_comment_3,
                  ]
                 )

generate_comment(treatment_dataset,
                 'timePeriodComment',
                 treatDS_time_period_comment,
                 )

generate_comment(treatment_dataset,
                 'geographyComment', 
                 treatDS_geography_comment,
                 )

# Representativeness
generate_representativeness(treatment_dataset,
                            treatDS_samplingProcedure_text,
                            treatDS_extrapolation_text,
                            treatDS_representativeness_percent)


# Reference exchange
treatment_dataset, MD = generate_reference_exchange(treatment_dataset,
                                                    treatDS_ref_exchange_comment,
                                                    total_PV,
                                                    total_PV_uncertainty,
                                                    untreated_fraction,
                                                    untreated_fraction_uncertainty,
                                                    treatDS_PV_comment,
                                                    WW_prop_df,
                                                    overload_loss_fraction_particulate,
                                                    overload_loss_fraction_dissolved,
                                                    MD)