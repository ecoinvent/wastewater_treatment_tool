"""Default arguments, to be validated bi ICRA"""

default_activity_ends_treatment =\
"This activity ends with the discharge of treated wastewater to the natural environment."\
"This activity includes the transportation of wastewater via the sewer grid, "\
"and the treatment of the wastewater in the wastewater treatment plant."\
"The amounts of infrastructure and consumables are also included as inputs to the activity."\
" By definition, wastewater not sent to the sewer grid is also excluded. "\
"The fraction of wastewater discharged to the sewer grid but ultimately not treated because the sewer is "\
"unconnected and direct emissions due to hydraulic overload are also excluded. "\
"These are included in another dataset specifically covering the discharge of untreated wastewater. "\
"The production of sludge is included, but its treatment is covered by another treatment activity."

default_activity_ends_no_treatment =\
"This activity ends with the discharge of untreated wastewater to the natural environment."

default_activity_starts =\
"From the discharge of wastewater to the sewer grid."

no_uncertainty = {
    'variance':0, 
    'pedigreeMatrix':[1,1,1,1,1],
    'comment': "Uncertainty not considered"
    }

default_technology_level = "Current"
default_timePeriodStarts = "1995-01-01" #TODO - I'm not sure what makes sense here, or if this value should be location-specific
default_timePeriodEnds = "2025-12-31" #TODO - I'm not sure what makes sense here, or if this value should be location-specific

default_tech_descr_avg = \
"The treatment dataset represents a weighted average of multiple models of wastewater treatment plants. "+\
"TODO Some more text"

default_tech_description_specific_0 = "SOME INTRO SENTENCE ON THE FACT THAT THE USER MODELED THIS HIMSELF" #TODO

model_description_0 = \
"The inventory for most exchanges based on a marginal approach. The TODO model "\
"was run twice: once with the contribution of the wastewater of interest, "\
"and once without. The inputs and outputs attributed to the wastewater "\
"of interest were determined based on the difference between these two model "\
"runs. For more information, see the documentation on the tool's website, ",
"TODO_URL_TO TOOL"

model_description_1 = \
"TODO: Exchanges not based on the marginal approach include X (based on y) "\
"and z (based on w)"

model_description_avg = \
"TODO a comment about averaging"

default_timePeriodComment = "TODO, descr: additional explanations concerning the temporal validity of the flow data reported."

list_countries_with_specific_data = [ #TODO when we have the data!!!
    "ZA",
    "CH",
]    

default_avg_good_geo_comment = "The data used to model and average the different WWTP is based on country-specific data."
default__avg_bad_geo_comment = "TODO - DEPENDS N HOW WE GLOBALLY AVERAGE"
default_spec_geo_comment =  "The data used to model the WWTP is specific to the location."

default_tech_description_specific_1 = "Some automatic text here to describe technology" #TODO
default_tech_description_specific_2 = "Some automatic text here provide some details on parameters used" #TODO
