from pycode.defaults import basic_pollutants


def total_untreated_release(CSO_amounts, untreated_as_emissions, untreated_fraction, MD):
    """ Sum direct discharge and CSO. WIll fail if untreated_fraction == 0!

    Because of this problem, CSO emissions should ideally be placed in another dataset (market, treatment DS)"""

    efs = []
    for direct_discharge in untreated_as_emissions:
        ef_id = direct_discharge['ecoinvent_id']
        CSO_amount = [cso_amount['value'] for cso_amount in CSO_amounts if cso_amount['ecoinvent_id']==ef_id][0]
        scaled_CSO_amount = CSO_amount*(1-untreated_fraction)/(untreated_fraction)
        total_emission = scaled_CSO_amount + direct_discharge['value']
        fraction_CSO = scaled_CSO_amount/total_emission
        ef = self.create_empty_exchange()
        ef.update(
            {
                'group': 'ToEnvironment',
                'name': self.MD.loc[ef_id, 'name'],
                'compartment': 'water',
                subcompartment: 'surface water',
                'unitName': 'kg',
                'amount': total_emission,
            }
        )
        if fraction_CSO != 0:
            ef.update(
                {
                    comment: "Based on direct release to environment of wastewater " \
                             "discharged to sewers not connected to wastewater treatment plants {0:.4}% " \
                             "and compounds lost due to combined sewer overflow {0:.4}%".format(
                        (1 - fraction_CSO)*100, fraction_CSO*100
                    )
                }
            )
        else:
            ef.update(
                {
                    comment: "Based on direct release to environment of wastewater " \
                             "discharged to sewers not connected to wastewater treatment plants"
                }
            )
        uncertainty = direct_emission_uncertainty(
            ef_id, untreated_as_emissions[ef_id]['value'], scaled_CSO_amount, basic_pollutants, MD)
        efs.append([ef, [], direct_emission_uncertainty])
    return efs

def direct_emission_uncertainty(pollutant_id,
                                untreated_release,
                                scaled_CSO_amounts,
                                basic_pollutant_list,
                                MD):
    """Uncertainty depends on whether direct discharge or CSO is dominant"""
    if untreated_release > scaled_CSO_amounts:  # Mostly CSO
        if MD['property'].loc[pollutant_id, 'name'] in basic_pollutant_list:
            return {
                'variance': 0.04,
                'pedigreeMatrix': [5, 5, 4, 5, 1],
                'comment': "Uncertainty represents that of the wastewater composition, " \
                           "and the pedigree scores are for the releases due to combined sewer overflow, " \
                           "which represent a greater share of emissions {}.".format(
                    scaled_CSO_amounts / (scaled_CSO_amounts+ untreated_release)
                )
            }
        else:
            return {
                'variance': 0.65,
                'pedigreeMatrix': [5, 5, 4, 5, 1],
                'comment': "Uncertainty represents that of the wastewater composition, " \
                           "and the pedigree scores are for the releases due to combined sewer overflow, " \
                           "which represent a greater share of emissions {}.".format(
                    scaled_CSO_amounts / (scaled_CSO_amounts+ untreated_release)
                )
            }
    else:  # Mostly direct discharge
        if MD['property'].loc[pollutant_id, 'name'] in basic_pollutant_list:
            return {
                'variance': 0.04,
                'pedigreeMatrix': [1, 1, 1, 1, 1],
                'comment': "Uncertainty represents that of the wastewater composition only. "\
                "The uncertainty of the releases due to combined sewer overflow {} are "\
                "not considered in the pedigree scores.".format(
                    scaled_CSO_amounts / (scaled_CSO_amounts+ untreated_release)
                )
            }
        else:
            return {
                'variance': 0.65,
                'pedigreeMatrix': [1, 1, 1, 1, 1],
                'comment': "Uncertainty represents that of the wastewater composition only. " \
                           "The uncertainty of the releases due to combined sewer overflow {} are " \
                           "not considered in the pedigree scores.".format(
                    scaled_CSO_amounts / (scaled_CSO_amounts + untreated_release)
                )
            }
