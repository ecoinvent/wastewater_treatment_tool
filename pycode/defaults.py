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

metals = [
    'Al',
    'Cd',
    'Ag',
    'B',
    'Ba',
    'Be',
    'Co',
    'Cr',
    'Cu',
    'Fe',
    'Hg',
    'Mn',
    'Mo',
    'Ni',
    'Pb',
    'Sc',
    'Sn',
    'Sr',
    'Ti',
    'Tl',
    'V',
    'W',
    'Zn', ]

non_metals = [
    'As',
    'Br',
    'Ca',
    'Cl',
    'F',
    'K',
    'I',
    'Mg',
    'Na',
    'Sb',
    'Se',
    'Si',
    'BOD',
    'PO4',
    'NH4',
    'TP',
    'TKN',
    'COD',
    'TSS',
    'NOx'
]

default_sewer_uncertainty = {
    'variance': 0.3,
    'pedigreeMatrix': [5, 5, 5, 5, 5],
    'comment': "Very rough estimate based on Swiss data (Doka 2009) and sampled Spanish WWTP."
}

default_infrastructure_uncertainty = {
    'variance': 0.3,
    'pedigreeMatrix': [5, 5, 1, 5, 5],
    'comment': "Very rough estimate based on a single Spanish plant and an estimated lifetime of 30 years"
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
    for tech in technologies_averaged:
        tech_mix += "\n\tShare: {:.0f}%; \n\t\t{}; \n\t\t{}; \n\t\tCapacity: {} PE;"\
                    "\n\t\tCapacity class: {} PE; \n\t\tLocation: {}".format(
            tech['fraction'] * 100,
            tech['technology_level_1'],
            decode_tech_bitstring(tech['technology_level_2'])[0:-1],
            tech['capacity'],
            tech['class'],
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

default_tech_description_specific = "The parameter values used in the tool to generate this dataset "\
    "were adapted to model a specific wastewater treatment plant configuration. "\
    "The modelled wastewater treatment plant uses {}. {} Its capacity is {}."

treat_common_general_product = "The inventory is mostly based on activated sludge " \
                               "process guidelines typically known as Metcalf and Eddy " \
                               "(Tchobanoglous et al., 2014) that comprise a set of equations " \
                               "that, computed in a sequential manner, are used to quantify a " \
                               "number of design outputs as a function of design inputs. The design " \
                               "inputs include influent characteristics (e.g. flow, concentration of pollutants), " \
                               "operational settings (e.g. oxygen concentration in the biological reactor), safety " \
                               "factors, kinetic and stoichiometric parameters and effluent requirements (e.g. target " \
                               "ammonia concentration in the effluent of the WWTP). The design outputs comprise " \
                               "aerobic, anoxic, anaerobic volumes, dissolved oxygen demand; internal and external " \
                               "recycle flow-rates, settling areas and dosage of chemicals (external carbon source, " \
                               "metal salts, and alkalinity)."

treat_general_comment_avg_municipal = "The treatment of municipal wastewater was modelled in {} WWTP models" \
                                      "These models represent different types of wastewater treatment plants " \
                                      "from this region. The results for each plant are expressed as exchange amount/m3 " \
                                      "of treated wastewater, and a weighted average is calculated based on the " \
                                      "market share of each of the plants."
treat_general_comment_specific_municipal = "The treatment of municipal wastewater was modelled in WWTP model" \
                                           "whose design parameters were adapted by the data provider. "
treat_general_comment_avg_not_municipal = "The treatment of wastewater from {0} was modelled in {1} WWTP models" \
                                          ". The relation of inputs and outputs " \
                                          "to 1m3 of treated wastewater from {0} is based on a marginal approach: " \
                                          "for each of the WWTP models, the model is first run " \
                                          "supposing that the WWTP does not treat the wastewater from {0}, " \
                                          "and then a second time with an additional 1m3 of wastewater from " \
                                          "{0}. Then, the difference between the two sets of results is calculated, " \
                                          "and normalized to 1m3. " \
                                          "A weighted average of these results is then calculated based on the " \
                                          "market share of each of the plants."
treat_general_comment_specific_not_municipal = "The treatment of wastewater from {0} was modelled in a WWTP model " \
                                               "whose design parameters were adapted by the data provider." \
                                               "The relation of inputs and outputs " \
                                               "to 1m3 of treated wastewater from {0} is based on a marginal approach: " \
                                               "for each of the WWTP models, the model is first run " \
                                               "supposing that the WWTP does not treat the wastewater from {0}, " \
                                               "and then a second time with an additional 1m3 of wastewater from " \
                                               "{0}. Then, the difference between the two sets of results is calculated, " \
                                               "and normalized to 1m3."
treat_general_comment_final_note = "Some exchanges are actually not specifically based on the " \
                                   "design guidelines (electricity demand, infrastructure). These are " \
                                   "identified in exchange comments. For more information on the model, " \
    "see the tool's website at {}"


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

default_samplingProcedure_text_treat = "Most exchanges based on a model built from "\
    "activated sludge process guidelines."

def default_extrapolations_text_treat_avg(technologies_averaged):
    list_regions = list(set([d['location'] for d in technologies_averaged]))
    regions_string = ""
    for region in list_regions:
        regions_string += str(region)
    regions_string += "."
    if len(technologies_averaged)==1:
        return "The region used to model the wastewater treatment plant is {}".format(regions_string)
    else:
        return "The regions used to model the wastewater treatment plant are {}".format(regions_string)

default_extrapolations_text_treat_spec = "The model parameters were adapted for "\
    "the specific wastewater treatment plant modelled in this dataset."
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
    'variance': 0.04,
    'pedigreeMatrix': [3, 5, 1, 5, 4],
    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
}
default_FeCl3_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [3, 5, 1, 5, 4],
    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
}
default_acrylamide_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [3, 5, 1, 5, 4],
    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
}

default_NaHCO3_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [3, 5, 1, 5, 4],
    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
}

no_uncertainty = {
    'variance': 0,
    'pedigreeMatrix': [1, 1, 1, 1, 1],
    'comment': "Uncertainty not considered"
}


sludge_uncertainty = {
    'variance': 0.0006,
    'pedigreeMatrix': [3, 5, 1, 5, 4],
    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
}

infra_dict = {
    'Lifetime_WWTP': {
        'Category': 'WWTP',
        'Description': 'Lifetime of the WWTP (years)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 30,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 30,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 30,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 30,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 30,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 30
    },
    'corresp_ecoinvent_class': {
        'Category': 'WWTP',
        'Description': 'Name of the existing intermediate exchange in ecoinvent',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 'wastewater treatment facility, capacity 1.6E8l/year',
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 'wastewater treatment facility, capacity 4.7E10l/year',
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 'wastewater treatment facility, capacity 1.1E10l/year',
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 'wastewater treatment facility, capacity 5E9l/year',
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 'wastewater treatment facility, capacity 5E9l/year',
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 'wastewater treatment facility, capacity 1E9l/year'
    },
    'diff_PE_WWTP': {
        'Category': 'WWTP',
        'Description': 'Difference between our median and Doka (PE) ((ours-Doka)/ours)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': -0.166125,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 0.05156,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 0.2895714285714286,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': -0.6576666666666666,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 0.11316666666666667
    },
    'diff_km_sewer_per_m3': {
        'Category': 'Sewers',
        'Description': 'Difference between our value and Doka (PE) ((ours-Doka)/ours)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 0.5029429999999999,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 0.49411000000000005,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 0.25665142857142853,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 0.5483125,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 0.5482324561403509
    },
    'diff_m3_over_life_WWTP': {
        'Category': 'WWTP',
        'Description': 'Difference between our value and Doka (m3/lifetime) ((ours-Doka)/ours)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': -1.346772104607721,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': -0.8746074363992172,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 0.04438165905631659,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': -2.6695744292237444,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': -0.9631817351598173
    },
    'diff_m3_per_year_WWTP': {
        'Category': 'WWTP',
        'Description': 'Difference between our value and Doka (m3/year) ((ours-Doka)/ours)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': -1.346772104607721,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': -0.8746074363992172,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 0.04438165905631659,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': -2.6695744292237444,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': -0.9631817351598173
    },
    'doka_m3_per_year_WWTP': {
        'Category': 'WWTP',
        'Description': 'Doka yearly capacity (m3/year)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 162812,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 47111450,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 14368866,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 5022730,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 5022730,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 1074842
    },
    'km_sewer_per_m3': {
        'Category': 'Sewers',
        'Description': 'kilometer sewers per m3 over lifetime (km/m3)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 3.762e-07,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 2.4906600249066003e-07,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 3.326810176125245e-07,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 2.9299847792998476e-07,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 4.821917808219178e-07,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 6.246575342465754e-07
    },
    'km_sewer_per_m3_doka': {
        'Category': 'Sewers',
        'Description': 'kilometer sewers per m3 over lifetime, Doka 2009 (km/m3)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 3.762e-07,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 1.238e-07,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 1.683e-07,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 2.178e-07,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 2.178e-07,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 2.822e-07
    },
    'lifetime_sewer': {
        'Category': 'Sewers',
        'Description': 'Lifetime of sewer system (years)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 100,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 100,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 100,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 100,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 100,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 100
    },
    'm3_over_life_WWTP': {
        'Category': 'WWTP',
        'Description': 'm3 treated over lifetime of WWTP',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 4884360,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 602250000,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 229950000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 157680000,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 41062500,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 16425000
    },
    'm3_over_life_WWTP_Doka': {
        'Category': 'WWTP',
        'Description': 'm3 treated over lifetime of WWTP, Doka 2009',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 4884360,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 1413343500,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 431065980,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 150681900,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 150681900,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 32245260
    },
    'm3_over_life_sewers': {
        'Category': 'Sewers',
        'Description': 'Total m3 ww transported by sewer gid over lifetime',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 2007500000,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 766500000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 525600000,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 136875000,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 54750000
    },
    'm_sewers_per_capita': {
        'Category': 'Sewers',
        'Description': 'Meters per capita of sewers, Doka 2009',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 7.6,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 2.5,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 3.4,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 4.4,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 4.4,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 5.7
    },
    'new_name_act': {
        'Category': 'WWTP',
        'Description': 'Proposed name of the activity',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 'wastewater treatment facility, capacity 1.6E8l/year',
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 'wastewater treatment facility construction, capacity class 1, greater than 100,000 PE',
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 'wastewater treatment facility construction, capacity class 2, between 50,000 and 100,000 PE',
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 'wastewater treatment facility construction, capacity class 3a, between 20,000 and 50,000 PE',
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 'wastewater treatment facility construction, capacity class 3b, between 10,000 and 20,000 PE',
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 'wastewater treatment facility construction, capacity class 4, between 2,000 and 10,000 PE'
    },
    'new_name_exc': {
        'Category': 'WWTP',
        'Description': 'Proposed name of the intermediate exchange',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 'wastewater treatment facility construction, capacity 1.6E8l/year',
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 'wastewater treatment facility, capacity class 1, greater than 100,000 PE',
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE',
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE',
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE',
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE'
    },
    'nom_cap_Doka_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity range in Doka (PE)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 806,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 233225,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 71133,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 24865,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 24865,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 5321
    },
    'nom_cap_max_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity range maximum (PE)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 2000,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': '+',
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 100000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 50000,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 20000,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 2000
    },
    'nom_cap_median_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity median (PE)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 1015,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 200000,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 75000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 35000,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 15000,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 6000
    },
    'nom_cap_min_WWTP': {
        'Category': 'WWTP',
        'Description': 'Nominal capacity range minimum (PE)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 30,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 100000,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 50000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 20000,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 10000,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 10000
    },
    'sample_cap_WWTP': {
        'Category': 'WWTP',
        'Description': 'Sample capacity (PE)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 206250,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 105000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 44153,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 18750,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 8750
    },
    'sample_m3_per_d_WWTP': {
        'Category': 'WWTP',
        'Description': 'Daily capacity\xa0 (m3/d)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 55000,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 21000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 14400,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 3750,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 1500
    },
    'sample_m3_per_year_WWTP': {
        'Category': 'WWTP',
        'Description': 'Annula capacity\xa0 (m3/year)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 20075000,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 7665000,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 5256000,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 1368750,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 547500
    },
    'sample_name_WWTP': {
        'Category': 'WWTP',
        'Description': 'Sample WWTP name',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 0,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 'Girona',
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': "L'Escala",
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 'Manlleu',
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 'Balaguer',
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 'Navàs'
    },
    'sewer_length': {
        'Category': 'Sewers',
        'Description': 'Sewer grid length, calculated (km)',
        'wastewater treatment facility construction, capacity 1.6E8l/year': 7.6,
        'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 500,
        'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 255,
        'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE': 154,
        'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE': 66,
        'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE': 34.2
    }
}
