


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

# Grit
grit_total_amount = 0.031 #kg/m3 in WWTP
grit_plastic_ratio = 0.5
grit_biomass_ratio = 0.5
total_grit_uncertainty = {'variance':0.0006, 'pedigreeMatrix':[1,3,5,5,1], 'comment': ""}
fraction_grit_biomass_uncertainty = {'variance':0.0006, 'pedigreeMatrix':[1,3,5,5,1], 'comment': ""}
grit_plastics_fraction_uncertainty = {'variance':0.0006, 'pedigreeMatrix':[1,3,5,5,1], 'comment': ""}

# Consumables
treatDS_consumable_exchange_name = 'lime'
treatDS_consumable_amount = 0.42 #
treatDS_consumable_uncertainty = {'variance': 0.0006, 'pedigreeMatrix': [2, 4, 3, 3, 1], 'comment':"Comment about the uncertainty"}
treatDS_consumable_comment = "Calcium hydroxide (Ca(OH)2) used for alkalinity addition and pH adjustment for metals removal. Amount calculated based on technology mix and wastewater properties."

# Heat
treatDS_total_heat = 10
treatDS_fraction_from_natural_gas = 0.8
treatDS_heat_uncertainty = {'variance': 0.0006,
                            'pedigreeMatrix': [2, 4, 3, 3, 1],
                            'comment': ""} # Placeholder
treatDS_heat_from_natrual_gas_uncertainty = {'variance': 0.0006,
                                             'pedigreeMatrix': [2, 4, 3, 3, 1],
                                             'comment': ""} # Placeholder
treatDS_heat_NG_comment = "default" # Automatically generate comment, can be overridden
treatDS_heat_other_comment = "default" # Automatically generate comment, can be overridden

# Electricity
treatDS_electricity_amount = 2
treatDS_electricity_uncertainty = {'variance': 0.0006,
                                   'pedigreeMatrix': [2, 4, 3, 3, 1],
                                   'comment':""}
treatDS_electricity_comment="Electricity consumed by the wastewater treatment plant"



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

# Grit
grit_plastics_comment_default = "Amount of plastics removed from wastewater. Based on an assumed {} kg/m3 of grit removed, "\
                                " and an assumed {:2}% of the grit that is plastics".format(grit_default_total_amount,
                                                                                grit_default_plastic_ratio*100)
grit_biomass_comment_default = "Amount of biomass  removed from wastewater. Based on an assumed {} kg/m3 of grit removed, "\
                                " and an assumed {:2}% of the grit that is biomass. "\
                                "Biomass waste management modelled as paper waste management".format(
                                    grit_default_total_amount,
                                    grit_default_biomass_ratio*100)
                                
# Electricity
treatDS_electricity_amount = 2
treatDS_electricity_uncertainty = {'variance': 0.0006,
                                   'pedigreeMatrix': [2, 4, 3, 3, 1],
                                   'comment':""}
treatDS_electricity_comment='default'

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

# Grit
treatment_dataset = add_grit(treatment_dataset,
                             grit_total_amount,
                             grit_plastic_ratio,
                             grit_biomass_ratio,
                             total_grit_uncertainty,
                             fraction_grit_biomass_uncertainty,
                             grit_plastics_fraction_uncertainty,
                             grit_plastics_comment,
                             grit_biomass_comment,
                             PV,
                             MD)

# Lime (as a consumable example)
treatment_dataset = generate_consumables(treatment_dataset,
                                         consumable_example_exchange_name,
                                         consumable_example_amount,
                                         consumable_example_uncertainty,
                                         consumable_example_comment,
                                         MD)

# Heat
treatment_dataset = generate_heat_inputs(treatment_dataset,
                                         treatDS_total_heat,
                                         treatDS_fraction_from_natural_gas,
                                         treatDS_heat_uncertainty,
                                         treatDS_heat_from_natrual_gas_uncertainty,
                                         treatDS_heat_NG_comment,
                                         treatDS_heat_other_comment,
                                         MD)

treatment_dataset = generate_electricity(treatment_dataset,
                                         treatDS_electricity_amount,
                                         treatDS_electricity_uncertainty,
                                         treatDS_electricity_comment,
                                         MD)
