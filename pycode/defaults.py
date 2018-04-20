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
    'Co',
    'Cr',
    'Cu',
    'Fe',
    'Hg',
    'Mn',
    'Mo',
    'Ni',
    'Pb',
    'Sn',
    'Zn', ]

non_metals = [
    'As',
    'Ca',
    'Cl',
    'F',
    'K',
    'Mg',
    'Na',
    'Si',
    'BOD',
    'PO4',
    'NH4',
    'TP',
    'TKN',
    'COD',
    'TSS'
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
    for tech in technologies_averaged.values():
        tech_mix += "\n\tShare: {:.0f}%; \n\t\t{}; \n\t\tCapacity: {} PE;"\
                    "\n\t\tCapacity class: {} PE; \n\t\tLocation: {}".format(
            tech['fraction'] * 100,
            decode_tech_bitstring(tech['technology_str'])[0:-1],
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
    'variance': 0.0006,
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