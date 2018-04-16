"""Default arguments, to be validated bi ICRA"""

# Untreated fraction

default_timePeriodStarts_untreated = "2000-01-01"
default_timePeriodEnds_untreated = "2025-12-31"
default_technology_level = "Current"
default_activity_starts = "From the discharge of wastewater to the sewer grid."
default_activity_ends_untreated = "This activity ends " \
                                  "with the discharge of untreated wastewater to the natural environment. " \
                                  "This includes discharge of wastewater from sewers not connected to wastewater treatment plants " \
                                  "and discharge due to combined sewer overflow (CSO), which are direct discharges of wastewater " \
                                  "to the environment during episodes (e.g. heavy rainfall, snow melt) where wastewater volume exceeds " \
                                  "the capacity of the sewer system or treatment plant."
default_technology_comment_untreated = ["No technology modelled: direct discharge."]
default_general_comment_untreated_0 = [
    "This dataset accounts for wastewater sent to the sewer system but ultimately " \
    "not treated in a wastewater treatment plant. It accounts for three things: " \
    "(1) The wastewater that is directly discharged to the environment because it " \
    "is not connected to a wastewater treatment plant; "
    "(2) Wastewater pollutants emitted to the environment due to combined " \
    "sewer overflow (CSO); and (3) the sewer system itself. ",
    "The direct discharge (1) is modelled by simply transferring the wastewater " \
    "pollutants as direct emissions to surface water. The volume of directly " \
    "discharged water is based on the World Health Organization's Progress on " \
    "Drinking Water, Sanitation and Hygiene 2017 update",
    "Pollutants lost to CSO (2) are estimated using Swiss data, as used in ecoinvent " \
    "v2 data based on Doka (2009). This is a rough estimate at best when applied " \
    "to other countries.",
    ""
]


def sewer_estimation_text(tool_use_type):
    if tool_use_type == "average":
        return [
            "The amount of sewers per m3 is based on Swiss data, as used in ecoinvent " \
            "v2 data based on Doka (2009). This data provides estimations of sewer " \
            "infrastructure per m3 of water for different WWTP capacities. This dataset " \
            "creates a weighted average of capacity classes of the wastewater treatment " \
            "plants that are used in the treatment dataset for the same wastewater. " \
            "This is a rough estimation at best, which is reflected in the uncertainty."
        ]
    else:
        return [
            "The amount of sewers per m3 is based on Swiss data, as used in ecoinvent " \
            "v2 data based on Doka (2009). This data provides estimations of sewer " \
            "infrastructure per m3 of water for different WWTP capacities. " \
            "This is a rough estimation at best, which is reflected in the uncertainty."
        ]


default_time_period_comment_untreated = [
    "The discharge of wastewater to the environment without treatment is an atemporal process: it does not have a time period per se.",
    "The untreated fraction, which is used to determine the production volume, is based on 2015 data.",
    "Combined sewer overflow and sewer infrastructure data based on estimates for Swiss condition in the " \
    "1990s, taken from Doka (2009)."
]

default_geography_comment_untreated = [
    "This relates to the geography that the LCI dataset aims to be valid for, " \
    "and not the geography of the data that was used to populate it. For geographical " \
    "representativeness, see Representativeness/Extrapolations field."
]

default_representativeness_untreated_1 = "No sampled data."

def default_representativeness_untreated_2(used_WHO_region):
    discharge_extrapolation = "The data used to estimate the amount of direct discharge is based on data from {}. ".format(
        used_WHO_region
    )
    discharge_extrapolation += "The data for combined sewer overflow and sewer " \
                               "infrastructure is based on Swiss data (Doka, 2009)."
    return discharge_extrapolation


ref_exchange_comment_untreated = "Wastewater sent to sewer system and directly emitted to environment"


def generate_default_PV_comment_untreated(PV, untreated_fraction):
    return "Calculated based on total amount of wastewater set to the " \
           "sewer system ({}), as determined from the amount of wastewater " \
           "and the production volume of the generating activity, " \
           "and the fraction of wastewater sent to sewers not connected " \
           "to a wastewater treatment plant ({})".format(PV, untreated_fraction)


default_PV_uncertainty_untreated = {
    'variance': 0.0006,
    'pedigreeMatrix': [4, 5, 1, 1, 1],
    'comment': "Pedigree scores associated with quality of WHO data on fraction of " \
               "wastewater discharged to sewer that is connected to a wastewater treatment plant."
}



basic_pollutants = [
    "BOD5, mass per volume",
    "COD, mass per volume",
    "mass concentration, DOC",
    "mass concentration, TOC",
    "mass concentration, dissolved ammonia NH4 as N",
    "mass concentration, dissolved nitrate NO3 as N",
    "mass concentration, dissolved nitrite NO2 as N",
    "mass concentration, particulate nitrogen",
    "mass concentration, dissolved organic nitrogen as N",
    "mass concentration, nitrogen",
    "mass concentration, dissolved Kjeldahl Nitrogen as N",
    "mass concentration, Kjeldahl Nitrogen as N",
    "mass concentration, potassium",
    "mass concentration, magnesium",
    "mass concentration, sodium",
    "mass concentration, dissolved phosphate PO4 as P",
    "mass concentration, particulate phophorus",
    "mass concentration, phophorus",
    "mass concentration, dissolved sulfate SO4 as S",
    "mass concentration, particulate sulfur",
    "mass concentration, sulfur",
]

default_sewer_uncertainty = {
    'variance': 0.3,
    'pedigreeMatrix': [5, 5, 5, 5, 5],
    'comment': "Very rough estimate based on Swiss data (Doka 2009) and sampled Spanish WWTP."
}

default_infrastructure_uncertainty = {
    'variance': 0.3,
    'pedigreeMatrix': [5, 5, 1, 5, 1],
    'comment': "Very rough estimate based on a single Spanish plant and an estimated lifetime of 40 years"
}

# ************************************
# Treatment defaults

default_timePeriodStarts_treated = "1995-01-01"
default_timePeriodEnds_treated = "2025-12-31"
default_activity_ends_treatment = "This activity ends " \
                                  "with the discharge of treated wastewater to the natural environment." \
                                  "This activity includes the transportation of wastewater via the sewer grid, " \
                                  "and the treatment of the wastewater in the wastewater treatment plant." \
                                  "The amounts of infrastructure and consumables are also included as inputs to the activity." \
                                  " By definition, wastewater not sent to the sewer grid is also excluded. " \
                                  "The fraction of wastewater discharged to the sewer grid but ultimately not treated because the sewer is " \
                                  "unconnected and direct emissions due to combined sewer overflow are also excluded. " \
                                  "These are included in another dataset specifically covering the discharge of untreated wastewater. " \
                                  "The production of sludge is included, but its treatment is covered by another treatment activity."


def technology_mix_constructor(technologies_averaged):
    """ Generate string representing technology mix from a technology mix dict"""
    tech_mix = "Averaged technologies:"
    for tech in technologies_averaged.values():
        tech_mix += "\n\tShare: {:.0f}%; \n\t\t{}; \n\t\tCapacity: {}; \n\t\tLocation: {}".format(
            tech['fraction'] * 100,
            decode_tech_bitstring(tech['technology_str'])[0:-1],
            tech['capacity'],
            tech['location']
        )
    return tech_mix


def decode_tech_bitstring(bit_string):  # i.e "1110001"
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
    tecs = [
        'Primary settler',
        'Aerobic BOD removal',
        'Nitrification',
        'Denitrification',
        'Biological P removal',
        'Chemical P removal',
        'Metals and other elements',
    ]

    # check if length of bit string is too large
    if (len(bit_string) > len(tecs)):
        raise ValueError('bit string has more characters than existing wwt technologies')
    # check that there is at least some information
    if (len(bit_string) == 0 or all([bit_string[i] == "0" for i in range(len(bit_string))])):
        raise ValueError('no information on technologies')
    if not all([bit_string[i] in ["0", "1"] for i in range(len(bit_string))]):
        raise ValueError('bit string had a character which is not 0 or 1')

    # loop bit_string characters
    tech_list = [tecs[i] for i in range(len(bit_string)) if bit_string[i] == "1"]

    rv = ', '.join(map(str, tech_list))
    rv = "Technology summary: " + rv + "."
    return (rv)


default_tech_descr_avg = "The treatment dataset represents a " \
                         "weighted average of multiple models of wastewater treatment plants."

default_tech_description_specific_0 = "SOME INTRO SENTENCE ON THE FACT THAT THE USER MODELED THIS HIMSELF"  # TODO - user modelled himself...
default_tech_description_specific_1 = "Some automatic text here to describe technology"  # TODO
default_tech_description_specific_2 = "Some automatic text here provide some details on parameters used"  # TODO

model_description_0 = "The inventory for most exchanges based on a " \
                      "marginal approach. The TODO model " \
                      "was run twice: once with the contribution of the wastewater of interest, " \
                      "and once without. The inputs and outputs attributed to the wastewater " \
                      "of interest were determined based on the difference between these two model " \
                      "runs. For more information, see the documentation on the tool's website, URL"  # TODO add URL

model_description_1 = "Exchanges not based on the marginal approach include " \
                      "X (based on y) and z (based on w)"  # TODO exchanges not based on marginal approach
model_description_avg = "TODO a comment about averaging"  # TODO add description of averaging
default_timePeriodComment_treatment = [
    "TODO, descr: additional explanations concerning the temporal validity of the flow data reported."]

list_countries_with_specific_data = [
    "ZA",
]

default_avg_good_geo_comment = [
    "The data used to model and average the different WWTP is based on country-specific data."]
default_avg_bad_geo_comment = [
    "No data was available for the region. Based on a rough approximation of the global data."]
default_spec_geo_comment = ["The data used to model the WWTP is specific to the location."]

default_samplingProcedure_text_treat = "TODO"  # TODO
default_extrapolations_text_treat = "TODO"  # TODO
ref_exchange_comment_treat = "Wastewater emitted to the sewer " \
                             "system and treated. Wastewater properties differ from those of " \
                             "wastewater actually sent to the sewer system in that they account for " \
                             "losses due to combined sewer overflow (CSO)"
default_PV_uncertainty_treat = {
    'variance': 0.0006,
    'pedigreeMatrix': [4, 5, 1, 1, 1],
    'comment': "Pedigree scores associated with quality of WHO data on fraction of " \
               "wastewater discharged to sewer that is connected to a wastewater treatment plant."
}

def generate_default_PV_comment_treated(PV, untreated_fraction):
    return "Calculated based on total amount of wastewater set to the " \
           "sewer system ({}), as determined from the amount of wastewater " \
           "and the production volume of the generating activity, " \
           "and the fraction of wastewater sent to sewers not connected " \
           "to a wastewater treatment plant ({}). Only the fraction sent " \
           "to a wastewater treatment pland included in production volume".format(PV, untreated_fraction)


default_electricity_comment = "Electricity consumption considers energy "\
    "required for aeration, pumping, mixing, dewatering and others (e.g. lighting). "\
    "The estimations are based on design parameters from Metcalf and Eddy (e.g. "\
    "pumping flows, aeration capacity), other sources (e.g. for Standard Aeration Energy) "\
    "and expert judgement."

default_electricity_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [4, 5, 1, 5, 4],
    'comment': "Calculations based on design parameters and assumptions."
}
default_FeCl3_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [4, 5, 1, 5, 4],
    'comment': "Calculations based on design parameters and assumptions."
}
default_acrylamide_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [4, 5, 1, 5, 4],
    'comment': "Calculations based on design parameters and assumptions."
}

default_NaHCO3_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [4, 5, 1, 5, 4],
    'comment': "Calculations based on design parameters and assumptions."
}

no_uncertainty = {
    'variance': 0,
    'pedigreeMatrix': [1, 1, 1, 1, 1],
    'comment': "Uncertainty not considered"
}

# ******* DATA *********#
infrastructure_dict = {
    'Lifetime_WWTP': {
        'Category': 'WWTP',
        'Description': 'Lifetime of the WWTP (years)',
        'Class 1 (over 100,000 per-capita equivalents)': 40,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 40,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 40,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 40,
        'Class 5 (30 to 2000 per-capita equivalents)': 40
    },
    'diff_PE_WWTP': {
        'Category': 'WWTP',
        'Description': 'Difference between our median and Doka (PE) ((ours-Doka)/ours)',
        'Class 1 (over 100,000 per-capita equivalents)': -0.166125,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 0.05156,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 0.17116666666666666,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 0.11316666666666667,
        'Class 5 (30 to 2000 per-capita equivalents)': 0.20591133004926107
    },
    'diff_km_sewer_per_m3': {
        'Category': 'Sewers',
        'Description': 'Difference between our value and Doka (PE) ((ours-Doka)/ours)',
        'Class 1 (over 100,000 per-capita equivalents)': 0.5029429999999999,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 0.49411000000000005,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 0.13276000000000004,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 0.3264309210526316,
        'Class 5 (30 to 2000 per-capita equivalents)': 0.12133134560539283
    },
    'diff_m3_over_life_WWTP': {
        'Category': 'WWTP',
        'Description': 'Difference between our value and Doka (m3/lifetime) ((ours-Doka)/ours)',
        'Class 1 (over 100,000 per-capita equivalents)': -0.7600790784557908,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': -0.4059621656881931,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 0.2832982543759513,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 0.41108856621004564,
        'Class 5 (30 to 2000 per-capita equivalents)': -0.9125485388127854
    },
    'diff_m3_per_year_WWTP': {
        'Category': 'WWTP',
        'Description': 'Difference between our value and Doka (m3/year) ((ours-Doka)/ours)',
        'Class 1 (over 100,000 per-capita equivalents)': -1.346772104607721,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': -0.8746074363992172,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 0.04438165905631659,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 0.21472730593607306,
        'Class 5 (30 to 2000 per-capita equivalents)': 0.7026264840182649
    },
    'doka_m3_per_year_WWTP': {
        'Category': 'WWTP',
        'Description': 'Doka yearly capacity (m3/year)',
        'Class 1 (over 100,000 per-capita equivalents)': 47111450,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 14368866,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 5022730,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 1074842,
        'Class 5 (30 to 2000 per-capita equivalents)': 162812
    },
    'km_sewer_per_m3': {
        'Category': 'Sewers',
        'Description': 'kilometer sewers per m3 over lifetime (km/m3)',
        'Class 1 (over 100,000 per-capita equivalents)': 2.4906600249066003e-07,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 3.326810176125245e-07,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 2.5114155251141555e-07,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 2.4986301369863014e-07,
        'Class 5 (30 to 2000 per-capita equivalents)': 1.408949771689498e-07
    },
    'km_sewer_per_m3_doka': {
        'Category': 'Sewers',
        'Description': 'kilometer sewers per m3 over lifetime, Doka 2009 (km/m3)',
        'Class 1 (over 100,000 per-capita equivalents)': 1.238e-07,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 1.683e-07,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 2.178e-07,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 1.683e-07,
        'Class 5 (30 to 2000 per-capita equivalents)': 1.238e-07
    },
    'lifetime_sewer': {
        'Category': 'Sewers',
        'Description': 'Lifetime of sewer system (years)',
        'Class 1 (over 100,000 per-capita equivalents)': 100,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 100,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 100,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 100,
        'Class 5 (30 to 2000 per-capita equivalents)': 100
    },
    'm3_over_life_WWTP': {
        'Category': 'WWTP',
        'Description': 'm3 treated over lifetime of WWTP',
        'Class 1 (over 100,000 per-capita equivalents)': 803000000,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 306600000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 210240000,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 54750000,
        'Class 5 (30 to 2000 per-capita equivalents)': 21900000
    },
    'm3_over_life_WWTP_Doka': {
        'Category': 'WWTP',
        'Description': 'm3 treated over lifetime of WWTP, Doka 2009',
        'Class 1 (over 100,000 per-capita equivalents)': 1413343500,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 431068000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 150679375,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 32242901,
        'Class 5 (30 to 2000 per-capita equivalents)': 41884813
    },
    'm3_over_life_sewers': {
        'Category': 'Sewers',
        'Description': 'Total m3 ww transported by sewer gid over lifetime',
        'Class 1 (over 100,000 per-capita equivalents)': 2007500000,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 766500000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 525600000,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 136875000,
        'Class 5 (30 to 2000 per-capita equivalents)': 54750000
    },
    'm_sewers_per_capita': {
        'Category': 'Sewers',
        'Description': 'Meters per capita of sewers, Doka 2009',
        'Class 1 (over 100,000 per-capita equivalents)': 2.5,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 3.4,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 4.4,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 5.7,
        'Class 5 (30 to 2000 per-capita equivalents)': 7.6
    },
    'name': {
        'Category': 'WWTP',
        'Description': 'Name of the intermediate exchange',
        'Class 1 (over 100,000 per-capita equivalents)': 'wastewater treatment facility construction, capacity Class 1 (over 100,000 per-capita equivalents), 2.01E10 l/year',
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 'wastewater treatment facility construction, capacity Class 2 (50,000 to 100,000 per-capita equivalents), 7.67E9 l/year',
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 'wastewater treatment facility construction, capacity Class 3 (10,000 to 50,000 per-capita equivalents), 5.26E9 l/year',
        'Class 4 (2000 to 10,000 per-capita equivalents)': 'wastewater treatment facility construction, capacity Class 4 (2000 to 10,000 per-capita equivalents), 1.37E9 l/year',
        'Class 5 (30 to 2000 per-capita equivalents)': 'wastewater treatment facility construction, capacity Class 5 (30 to 2000 per-capita equivalents), 5.48E8 l/year'
    },
    'nom_cap_Doka_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity range in Doka (PE)',
        'Class 1 (over 100,000 per-capita equivalents)': 233225,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 71133,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 24865,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 5321,
        'Class 5 (30 to 2000 per-capita equivalents)': 806
    },
    'nom_cap_max_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity range maximum (PE)',
        'Class 1 (over 100,000 per-capita equivalents)': '+',
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 100000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 50000,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 10000,
        'Class 5 (30 to 2000 per-capita equivalents)': 2000
    },
    'nom_cap_median_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity median (PE)',
        'Class 1 (over 100,000 per-capita equivalents)': 200000,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 75000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 30000,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 6000,
        'Class 5 (30 to 2000 per-capita equivalents)': 1015
    },
    'nom_cap_min_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity range minimum (PE)',
        'Class 1 (over 100,000 per-capita equivalents)': 100000,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 50000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 10000,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 2000,
        'Class 5 (30 to 2000 per-capita equivalents)': 30
    },
    'sample_cap_WWTP': {
        'Category': 'WWTP',
        'Description': 'Sample capacity (PE)',
        'Class 1 (over 100,000 per-capita equivalents)': 206250,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 105000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 44153,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 18750,
        'Class 5 (30 to 2000 per-capita equivalents)': 8750
    },
    'sample_m3_per_d_WWTP': {
        'Category': 'WWTP',
        'Description': 'Daily capacity\xa0 (m3/d)',
        'Class 1 (over 100,000 per-capita equivalents)': 55000,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 21000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 14400,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 3750,
        'Class 5 (30 to 2000 per-capita equivalents)': 1500
    },
    'sample_m3_per_year_WWTP': {
        'Category': 'WWTP',
        'Description': 'Annula capacity\xa0 (m3/year)',
        'Class 1 (over 100,000 per-capita equivalents)': 20075000,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 7665000,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 5256000,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 1368750,
        'Class 5 (30 to 2000 per-capita equivalents)': 547500
    },
    'sample_name_WWTP': {
        'Category': 'WWTP',
        'Description': 'Sample WWTP name',
        'Class 1 (over 100,000 per-capita equivalents)': 'Girona',
        'Class 2 (50,000 to 100,000 per-capita equivalents)': "L'Escala",
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 'Manlleu',
        'Class 4 (2000 to 10,000 per-capita equivalents)': 'Balaguer',
        'Class 5 (30 to 2000 per-capita equivalents)': 'Navàs'
    },
    'sewer_length': {
        'Category': 'Sewers',
        'Description': 'Sewer grid length, calculated (km)',
        'Class 1 (over 100,000 per-capita equivalents)': 500,
        'Class 2 (50,000 to 100,000 per-capita equivalents)': 255,
        'Class 3 (10,000 to 50,000 per-capita equivalents)': 132,
        'Class 4 (2000 to 10,000 per-capita equivalents)': 34.2,
        'Class 5 (30 to 2000 per-capita equivalents)': 7.714
    }
}
