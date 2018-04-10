"""Default arguments, to be validated bi ICRA"""

# Untreated fraction

default_timePeriodStarts_untreated = "1995-01-01"  # TODO - what makes sense as a valid time period for untreated fraction?
default_timePeriodEnds_untreated = "2025-12-31"  # TODO - what makes sense as a valid time period for untreated fraction?
default_technology_level = "Current"
default_activity_starts = "From the discharge of wastewater to the sewer grid."
default_activity_ends_untreated = "This activity ends "\
    "with the discharge of untreated wastewater to the natural environment. " \
    "This includes discharge of wastewater from sewers not connected to wastewater treatment plants " \
    "and discharge due to combined sewer overflow (CSO), which are direct discharges of wastewater " \
    "to the environment during episodes (e.g. heavy rainfall, snow melt) where wastewater volume exceeds " \
    "the capacity of the sewer system or treatment plant."
default_technology_comment_untreated = ["No technology modelled: direct discharge."]
default_general_comment_untreated = ["Based on statistical data about #TODO"]  #TODO - General comment untreated
default_time_period_comment_untreated = [
    "Untreated fraction based on country-specific data for 2015",
    "Combined sewer overflow data based on TODO"  # TODO - CSO comment for time period
]
default_geography_comment_untreated = [
    "Untreated fraction based on country-specific data",
    "CSO",  #TODO - CSO comment for geography
]
default_representativeness_untreated_1 = "" # TODO --> representativeness comment 1
default_representativeness_untreated_2 = ""# TODO --> representativeness comment 2
ref_exchange_comment_untreated = "Wastewater sent to sewer system and directly emitted to environment"
def generate_default_PV_comment_untreated(PV, untreated_fraction):
    return  "Calculated based on total amount of wastewater set to the "\
            "sewer system ({}), as determined from the amount of wastewater "\
            "and the production volume of the generating activity "\
            "and the fraction of wastewater sent to sewers not connected "\
            "to a wastewater treatment plant ({})".format(PV, untreated_fraction)
default_PV_uncertainty_untreated = {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for PV, untreated
    'comment': "TODO"  #TODO --> PV uncertainty comment
}
default_WW_property_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for WW properties
    'comment': "TODO"  # TODO --> property uncertainty comment
}

# Treatment defaults

default_timePeriodStarts_treated = "1995-01-01"  # TODO - what makes sense as a valid time period for untreated fraction?
default_timePeriodEnds_treated = "2025-12-31"  # TODO - what makes sense as a valid time period for untreated fraction?
default_activity_ends_treatment = "This activity ends "\
    "with the discharge of treated wastewater to the natural environment." \
    "This activity includes the transportation of wastewater via the sewer grid, " \
    "and the treatment of the wastewater in the wastewater treatment plant." \
    "The amounts of infrastructure and consumables are also included as inputs to the activity." \
    " By definition, wastewater not sent to the sewer grid is also excluded. " \
    "The fraction of wastewater discharged to the sewer grid but ultimately not treated because the sewer is " \
    "unconnected and direct emissions due to combined sewer overflow are also excluded. " \
    "These are included in another dataset specifically covering the discharge of untreated wastewater. " \
    "The production of sludge is included, but its treatment is covered by another treatment activity."

'''
  decode a technology mix description based on 7 bits packed into a string
  bit position | technology
  -------------+--------------------------
  0            | primary settler
  1            | bod removal
  2            | nitrification
  3            | denitrification
  4            | bio P removal
  5            | chem P removal
  6            | metals and other elements
  -------------+--------------------------
  example: "1110001"
  means:
    treatment with primary settler,
    with bod removal,
    with nitrification,
    without denitrification,
    without bio P removal,
    without chem P removal,
    with metals and other elements,
'''


def technology_mix_constructor(technologies_averaged):  # TODO --> test when tool runs n times
    """ Generate string representing technology mix from a technology mix dict"""
    tech_mix = "Averaged technologies:"
    for tech in technologies_averaged:
        tech_mix += "\nShare: {:.0f}%; {}; Capacity: {}; Location: {}".format(
            tech['fraction']*100,
            decode_tech_bitstring(tech['technology_str'])[0:-1],
            tech['capacity'],
            tech['location']
        )
    return tech_mix

def decode_tech_bitstring(bit_string): #i.e "1110001"
    tecs=[
    'Primary settler',
    'Aerobic BOD removal',
    'Nitrification',
    'Denitrification',
    'Biological P removal',
    'Chemical P removal',
    'Metals and other elements',
    ]

    #check if length of bit string is too large
    if(len(bit_string)>len(tecs)):
        raise ValueError('bit string has more characters than existing wwt technologies')
    #check that there is at least some information
    if(len(bit_string)==0 or all([bit_string[i]=="0" for i in range(len(bit_string))])):
        raise ValueError('no information on technologies')
    if not all([bit_string[i] in ["0", "1"] for i in range(len(bit_string))]):
        raise ValueError('bit string had a character which is not 0 or 1')

    #loop bit_string characters
    tech_list = [tecs[i] for i in range(len(bit_string)) if bit_string[i]=="1"]

    rv=', '.join(map(str, tech_list))
    rv="Technology summary: "+rv+"."
    return(rv)


default_tech_descr_avg = "The treatment dataset represents a "\
    "weighted average of multiple models of wastewater treatment plants. " + \
    "TODO Some more text" #TODO text to describe weighted average approach

default_tech_description_specific_0 = "SOME INTRO SENTENCE ON THE FACT THAT THE USER MODELED THIS HIMSELF"  # TODO - user modelled himself...
default_tech_description_specific_1 = "Some automatic text here to describe technology"  # TODO
default_tech_description_specific_2 = "Some automatic text here provide some details on parameters used"  # TODO

model_description_0 = "The inventory for most exchanges based on a "\
    "marginal approach. The TODO model " \
    "was run twice: once with the contribution of the wastewater of interest, " \
    "and once without. The inputs and outputs attributed to the wastewater " \
    "of interest were determined based on the difference between these two model " \
    "runs. For more information, see the documentation on the tool's website, URL"  #TODO add URL

model_description_1 = "Exchanges not based on the marginal approach include "\
    "X (based on y) and z (based on w)" #TODO exchanges not based on marginal approach
model_description_avg = "TODO a comment about averaging" #TODO add description of averaging
default_timePeriodComment_treatment = ["TODO, descr: additional explanations concerning the temporal validity of the flow data reported."]

list_countries_with_specific_data = [  # TODO when we have the data!!!
    "ZA",
    "CH",
]

default_avg_good_geo_comment = ["The data used to model and average the different WWTP is based on country-specific data."]
default_avg_bad_geo_comment = ["TODO - DEPENDS N HOW WE GLOBALLY AVERAGE"] #TODO depends on n-model approach
default_spec_geo_comment = ["The data used to model the WWTP is specific to the location."]#TODO get info on countries used to model vs. country required

default_samplingProcedure_text_treat = "TODO"  #TODO
default_extrapolations_text_treat = "TODO"  #TODO
ref_exchange_comment_treat = "Wastewater emitted to the sewer "\
    "system and treated. Wastewater properties differ from those of "\
    "wastewater actually sent to the sewer system in that they account for "\
    "losses due to combined sewer overflow (CSO)"
default_PV_uncertainty_treat = {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for PV, treated
    'comment': "TODO"  #TODO --> PV uncertainty comment
}
def generate_default_PV_comment_treated(PV, untreated_fraction):
    return  "Calculated based on total amount of wastewater set to the "\
            "sewer system ({}), as determined from the amount of wastewater "\
            "and the production volume of the generating activity "\
            "and the fraction of wastewater sent to sewers not connected "\
            "to a wastewater treatment plant ({}). Only the fraction sent "\
            "to a wastewater treatment pland included in production volume".format(PV, untreated_fraction)
default_electricity_comment = "How is this calculated?"  #TODO electricity text
default_electricity_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for FeCl3
    'comment': "TODO"  #TODO --> FeCl3 uncertainty comment
}
default_FeCl3_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for FeCl3
    'comment': "TODO"  #TODO --> FeCl3 uncertainty comment
}
default_acrylamide_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for acrylamide
    'comment': "TODO"  #TODO --> acrylamide uncertainty comment
}

default_NaHCO3_uncertainty= {
    'variance': 0.0006,
    'pedigreeMatrix': [1, 2, 3, 4, 5],  # TODO - pedigree matrix for NaHCO3
    'comment': "TODO"  #TODO --> NaHCO3 uncertainty comment
}

no_uncertainty = {
    'variance': 0,
    'pedigreeMatrix': [1, 1, 1, 1, 1],
    'comment': "Uncertainty not considered"
}

