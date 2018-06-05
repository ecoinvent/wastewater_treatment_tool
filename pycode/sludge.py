from .defaults import *
from .spold_utils import *

def return_sludge_exc_and_props(sludge_properties, WWTP_emissions_sludge, activity_PV, name, MD):
    """ Return an exchange dict and a list of properties to append exchange
    sludge_properties and WWTP_emissions_sludge refer to the corresponding dicts in self.
    """
    exc = sludge_exc_calc(sludge_properties, activity_PV, name)
    if exc == "No sludge":
        pass
    else:
        sludge_uncertainty = {
                'variance': 0.0006,
                'pedigreeMatrix': [4, 5, 1, 5, 4],
                'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
        }
        sludge_PV_uncertainty = {
                'variance': 0.0006,
                'pedigreeMatrix': [4, 5, 1, 5, 4],
                'comment': "Pedigree scores associated with quality of WHO data on fraction of " \
                           "wastewater discharged to sewer that is connected to a wastewater treatment plant " \
                           "and uncertainty on the amount of sludge generated per m3 of wastewater treated."
        }
        properties = generate_properties_list(sludge_properties, WWTP_emissions_sludge, -exc['amount'], MD)
        return {
            'exc':exc,
            'properties':properties,
            'uncertainty':sludge_uncertainty,
            'PV_uncertainty':sludge_PV_uncertainty,
        }


def sludge_exc_calc(sludge_properties, activity_PV, name):
    """ Calculate total sludge per m3 activity water

    This is the "amount" of the exchange.
    Calculated from "sludge_properties"
    Total dry mass = TSS_removed_kgd + P_X_TSS + Excess_sludge_kg
    """
    potential_contributions = [
        'TSS_removed_kgd',  # primary
        'P_X_TSS',  # secondary
        'Excess_sludge_kg'  # precipitation from chemical P removal
    ]
    mapping_to_comments = {
        'TSS_removed_kgd': "Sludge from primary settler",  # primary
        'P_X_TSS': "Sludge from secondary settler",  # secondary
        'Excess_sludge_kg': "Excess sludge from chemical P precipitation"  # precipitation from chemical P removal
    }
    amounts = [d['value']
               for d in sludge_properties
               for contrib in potential_contributions
               if d['id'] == contrib
               ]

    amount = sum(amounts)
    if amount != 0:
        sources = [mapping_to_comments[d['id']]
                   for d in sludge_properties
                   for contrib in potential_contributions
                   if d['id'] == contrib
                   ]
        comment_0 = "Total sludge production on a dry matter basis from treatment of 1m3 of wastewater."
        if len(sources) == 1:
            comment_1 = sources[0]
        else:
            comment_1 = "Sources of sludge: "
            for i in range(len(sources)):
                comment_1 += "{}={:.3}%. ".format(sources[i], amounts[i] / amount * 100)
        sludge = create_empty_exchange()
        sludge.update(
            {
                'group': 'ByProduct',
                'name': name,
                'unitName': 'kg',
                'amount': -amount,
                'comment': comment_0 + comment_1,
                'productionVolumeAmount': activity_PV['value'] * amount,
                'productionVolumeComment': "On a dry matter basis.",
            }
        )
        return sludge
    else:
        return "No sludge"

def generate_properties_list(sludge_properties, WWTP_emissions_sludge, amount, MD):

    properties = sludge_mass_property_calcs(sludge_properties, amount)
    sludge_Fe_content = sludge_Fe_content_calc(WWTP_emissions_sludge, sludge_properties, amount)
    if sludge_Fe_content is not None:
        properties.append(sludge_Fe_content)
    sludge_N_content = sludge_N_content_calc(sludge_properties, amount)
    if sludge_N_content is not None:
        properties.append(sludge_N_content)
    sludge_HPO_content = sludge_HPO_content_calc(sludge_properties, amount, MD)
    if sludge_HPO_content is not None:
        for prop in sludge_HPO_content:
            properties.append(prop)
    sludge_others_content = sludge_others_content_calc(WWTP_emissions_sludge, amount, MD)
    if sludge_others_content is not None:
        for prop in sludge_others_content:
            properties.append(prop)
    return properties




def sludge_mass_property_calcs(sludge_properties, amount):
    """ Returns the water content, as property, unit=kg water/kg dry matter

    Calculated from "sludge_properties"
    (sludge_primary_water_content + sludge_secondary_water_content + sludge_precipitation_water_content)/amount
    """
    potential_sources = [
        "sludge_primary_water_content",
        "sludge_secondary_water_content",
        "sludge_precipitation_water_content",
    ]
    total_water = sum([d['value']
                       for d in sludge_properties
                       for contrib in potential_sources
                       if d['id'] == contrib
                       ])
    if total_water != 0:
        wet_mass = (amount + total_water) / amount
        water_in_wet_mass = total_water / amount
        water_content = total_water /amount

        return [
            {
                'name': 'dry mass',
                'amount': 1,
                'comment': "Sludge reported on a dry mass basis, hence value is 1 by definition.",
                'unit': 'kg',
                'uncertainty': {
                    'variance': 0,
                    'pedigreeMatrix': [1, 1, 1, 1, 1],
                    'comment': ""
                },
            },
            {
                'name': 'wet mass',
                'amount': wet_mass,
                'comment': "Based on a water",
                'uncertainty': {
                    'variance': 0.0006,
                    'pedigreeMatrix': [3, 5, 1, 5, 4],
                    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
                },
                'unit': 'kg'
            },
            {
                'name': 'water in wet mass',
                'amount': water_in_wet_mass,
                'comment': "",
                'uncertainty': {
                    'variance': 0.0006,
                    'pedigreeMatrix': [3, 5, 1, 5, 4],
                    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
                },
                'unit': 'kg'
            },
            {
                'name': 'water content',
                'amount': water_content,
                'comment': "",
                'unit': 'dimensionless',
                'uncertainty': {
                    'variance': 0.0006,
                    'pedigreeMatrix': [3, 5, 1, 5, 4],
                    'comment': "Default pedigree scores for technosphere exchanges calculated with the ecoinvent wastewater tool"
                }
            },
        ]
    else:
        return [
            {
                'name': 'dry mass',
                'amount': 1,
                'comment': "Sludge reported on a dry mass basis, hence value is 1 by definition.",
                'unit': 'kg',
                'uncertainty': {
                    'variance': 0,
                    'pedigreeMatrix': [1, 1, 1, 1, 1],
                    'comment': ""
                },
            },
            {
                'name': 'wet mass',
                'amount': 1,
                'comment': "Dry sludge",
                'uncertainty': no_uncertainty,
                'unit': 'kg'
            },
            {
                'name': 'water in wet mass',
                'amount': 0,
                'comment': "",
                'uncertainty': no_uncertainty,
                'unit': 'kg'
            },
            {
                'name': 'water content',
                'amount': 0,
                'comment': "",
                'unit': 'dimensionless',
                'uncertainty': no_uncertainty,
            },
        ]

def sludge_carbon_content_calc(sludge_properties, amount, fraction_C_fossil):
    """ Returns the C content (fossil and non-fossil) as property, unit=kg C/kg dry matter

    Calculated from "sludge_properties"
    C_fossil = (sludge_primary_C_content * sludge_secondary_C_content) * fraction_C_fossil / amount
    C_non_fossil(sludge_primary_C_content * sludge_secondary_C_content) * (1-fraction_C_fossil) / amount
    """
    potential_contributions = [
        'sludge_primary_C_content',  # primary
        'sludge_secondary_C_content',  # secondary
    ]
    mapping_to_comments = {
        'sludge_primary_C_content': "Carbon in sludge from primary settler",  # primary
        'sludge_secondary_C_content': "Carbon in sludge from secondary settler",  # secondary
    }
    amounts = [d['value']
               for d in sludge_properties
               for contrib in potential_contributions
               if d['id'] == contrib
               ]

    total_C = sum(amounts)
    if total_C != 0:
        C_properties = []
        sources = [mapping_to_comments[d['id']]
                   for d in sludge_properties
                   for contrib in potential_contributions
                   if d['id'] == contrib
                   ]
        if len(sources) == 1:
            comment_0 = sources[0]
        else:
            comment_0 = "Carbon in sludge from primary settler ({:.3}) and secondary settler ({:.3})".format(
                amounts[0]/total_C * 100, amounts[1]/total_C * 100,
            )
        fossil_C = total_C * fraction_C_fossil
        non_fossil_C = total_C - fossil_C

        C_properties.append({
            'name': 'carbon content, fossil',
            'amount': fossil_C/amount,
            'comment': comment_0 + "Fossil carbon based on the fraction of carbon that is fossil"\
                       "in the wastewater ({:.3})".format(fraction_C_fossil),
            'unit': 'dimensionless',
            'uncertainty': {
                'variance': 0.006,
                'pedigreeMatrix': [3, 5, 1, 5, 4],
                'comment': "Default pedigree scores for exchanges calculated with the ecoinvent wastewater tool"
            },
        })
        C_properties.append({
            'name': 'carbon content, non-fossil',
            'amount': non_fossil_C / amount,
            'comment': comment_0 + "Non-fossil carbon based on the fraction of carbon that is fossil" \
                                   "in the wastewater ({:.3})".format(fraction_C_fossil),
            'unit': 'dimensionless',
            'uncertainty': {
                'variance': 0.006,
                'pedigreeMatrix': [3, 5, 1, 5, 4],
                'comment': "Default pedigree scores for exchanges calculated with the ecoinvent wastewater tool"
            },
        })
    else:
        pass

def sludge_Fe_content_calc(WWTP_emissions_sludge, sludge_properties, amount):
    """ Return Fe content as property, unit=kg Fe/kg dry sludge

    Considers sludge from precipitation and sludge removed from ww
    (Fe_effluent_sludge + sludge_precipitation_Fe_content)/amount
    Fe_effluent_sludge in WWTP_emissions_sludge
    sludge_precipitation_Fe_content in sludge_properties, and may not exist
    """
    Fe_effluent_sludge = [d['value']
               for d in WWTP_emissions_sludge
               if d['id'] == "Fe_effluent_sludge"
               ]
    if len(Fe_effluent_sludge)==1:
        Fe_effluent_sludge = Fe_effluent_sludge[0]
    else:
        Fe_effluent_sludge = None

    sludge_precipitation_Fe = [d['value']
               for d in sludge_properties
               if d['id'] == "sludge_precipitation_Fe_content"
               ]
    if len(sludge_precipitation_Fe)==1:
        sludge_precipitation_Fe = sludge_precipitation_Fe[0]
    else:
        sludge_precipitation_Fe = None

    if not Fe_effluent_sludge and not sludge_precipitation_Fe:
        return None
    else:
        if Fe_effluent_sludge and sludge_precipitation_Fe:
            total_Fe = Fe_effluent_sludge + sludge_precipitation_Fe
            comment = "Fe removed from wastewater ({:.3} and from FeCl3 used for P removal ({:.3}))".format(
                Fe_effluent_sludge/total_Fe * 100,
                sludge_precipitation_Fe / total_Fe * 100
            )

        elif Fe_effluent_sludge:
            comment = "Fe removed from wastewater"
            total_Fe = Fe_effluent_sludge
        else:
            comment = "Fe from FeCl3 used for P removal"
            total_Fe = sludge_precipitation_Fe
        return {
            'name': 'iron content',
            'amount': total_Fe / amount,
            'comment': comment,
            'unit': 'dimensionless',
            'uncertainty': {
                'variance': 0.65,
                'pedigreeMatrix': [3, 5, 1, 5, 4],
                'comment': "Default pedigree scores for exchanges calculated with the ecoinvent wastewater tool"
            },
        }


def sludge_N_content_calc(sludge_properties, amount):
    """ Return N content of sludge as property, unit=kg N/kg sludge as dry matter

    Calculated from sludge_properties['sludge_primary_N_content'] and sludge_properties['sludge_secondary_N_content']
    sum of N in primary and secondary sludge / amount
"""
    potential_contributions = [
        'sludge_primary_N_content',  # primary
        'sludge_secondary_N_content',  # secondary
    ]
    mapping_to_comments = {
        'sludge_primary_N_content': "N in sludge from primary settler",  # primary
        'sludge_secondary_N_content': "N in sludge from secondary settler",  # secondary
    }
    amounts = [d['value']
               for d in sludge_properties
               for contrib in potential_contributions
               if d['id'] == contrib
               ]

    total_N = sum(amounts)
    if total_N == 0:
        return None
    else:
        sources = [mapping_to_comments[d['id']]
                   for d in sludge_properties
                   for contrib in potential_contributions
                   if d['id'] == contrib
                   ]
        if len(sources) == 1:
            comment_0 = sources[0]
        else:
            comment_0 = "Nitrogen in sludge from primary settler ({:.3}) and secondary settler ({:.3})".format(
                amounts[0]/total_N * 100, amounts[1]/total_N * 100,
            )
        return {
                'name': 'nitrogen content',
                'amount': total_N / amount,
                'comment': comment_0,
                'unit': 'dimensionless',
                'uncertainty': {
                    'variance': 0.04,
                    'pedigreeMatrix': [3, 5, 1, 5, 4],
                    'comment': "Default pedigree scores for exchanges calculated with the ecoinvent wastewater tool"
                },
            }

def sludge_HPO_content_calc(sludge_properties, amount, MD):
    """ Return N content of sludge as property, unit=kg N/kg sludge as dry matter

    Calculated from sludge_properties['sludge_primary_X_content'] and sludge_properties['sludge_secondary_X_content']
    sum of X in primary and secondary sludge / amount
"""
    prop_list = []
    for element in ['H', 'P', 'O']:
        potential_contributions = [
            'sludge_primary_{}_content'.format(element),  # primary
            'sludge_secondary_{}_content'.format(element),  # secondary
        ]
        mapping_to_comments = {
            'sludge_primary_{}_content'.format(element): "{} in sludge from primary settler".format(element),  # primary
            'sludge_secondary_{}_content'.format(element): "{} in sludge from secondary settler".format(element),  # secondary
        }
        ecoinvent_ids = [
            [d['ecoinvent_id']
             for d in sludge_properties
             for contrib in potential_contributions
             if d['id'] == contrib
             ]
        ]
        amounts = [d['value']
                   for d in sludge_properties
                   for contrib in potential_contributions
                   if d['id'] == contrib
                   ]
        total = sum(amounts)
        if total == 0:
            pass
        else:
            ecoinvent_id = ecoinvent_ids[0]
            sources = [mapping_to_comments[d['id']]
                       for d in sludge_properties
                       for contrib in potential_contributions
                       if d['id'] == contrib
                       ]
            if len(sources) == 1:
                comment_0 = sources[0]
            else:
                comment_0 = "{} in sludge from primary settler ({:.3}) and secondary settler ({:.3})".format(
                    element,
                    amounts[0]/total * 100, amounts[1]/total * 100,
                )

            prop_list.append({
                    'name': get_prop_name(MD, ecoinvent_id[0]),
                    'amount': total / amount,
                    'comment': comment_0,
                    'unit': 'dimensionless',
                    'uncertainty': {
                        'variance': 0.04,
                        'pedigreeMatrix': [3, 5, 1, 5, 4],
                        'comment': "Default pedigree scores for exchanges calculated with the ecoinvent wastewater tool"
                    },
                }
            )
    if len(prop_list)==0:
        return None
    else:
        return prop_list

def sludge_others_content_calc(WWTP_emissions_sludge, amount, MD):
    """ Calculate properties for all other elements."""
    ignore = [
        'COD_effluent_sludge',
        'TKN_effluent_sludge',
        'NOx_effluent_sludge',
        'TP_effluent_sludge',
        'Fe_effluent_sludge'
    ]
    others = [props for props in WWTP_emissions_sludge
              if props['id'] not in ignore
              and props['ecoinvent_id'] is not False
              ]
    prop_list = []
    for element in others:
        if element['value']==0:
            pass
        else:
            if element['id'].split('_')[0] in metals:
                basic_variance = 0.65
            else:
                basic_variance = 0.04
            prop_list.append({
                'name': get_prop_name(MD, element["ecoinvent_id"]),
                'amount': element['value'] / amount,
                'comment': "Removed from wastewater",
                'unit': 'dimensionless',
                'uncertainty': {
                    'variance': basic_variance,
                    'pedigreeMatrix': [3, 5, 1, 5, 4],
                    'comment': "Default pedigree scores for exchanges calculated with the ecoinvent wastewater tool"
                },
            }
            )
    if len(prop_list) == 0:
        return None
    else:
        return prop_list