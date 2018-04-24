""" Series of functions to convert WW properties from the web tool
to properties that are useful for ecoSpold generation.
"""

from pycode.spold_utils import get_prop_name, get_prop_unit, get_prop_comment
from pycode.defaults import no_uncertainty, metals, non_metals


def calculate_dry_mass_of_ww(prop_dicts, COD_TOC_ratio):
    """ Returns a list of dictionaries ready to be processed by generate_reference_exchange"""

    consider_as_are = {
        'Al': 'mass concentration, aluminium',
        'As': 'mass concentration, arsenic',
        'Ca': 'mass concentration, calcium',
        'Cd': 'mass concentration, cadmium',
        'Cl': 'mass concentration, chlorine',
        'Co': 'mass concentration, cobalt',
        'Cr': 'mass concentration, chromium',
        'Cu': 'mass concentration, copper',
        'F': 'mass concentration, fluorine',
        'Fe': 'mass concentration, iron',
        'Hg': 'mass concentration, mercury',
        'K': 'mass concentration, potassium',
        'Mg': 'mass concentration, magnesium',
        'Mn': 'mass concentration, manganese',
        'Mo': 'mass concentration, molybdenum',
        'Na': 'mass concentration, sodium',
        'Ni': 'mass concentration, nickel',
        'Pb': 'mass concentration, lead',
        'Si': 'mass concentration, silicon',
        'Sn': 'mass concentration, tin',
        'Zn': 'mass concentration, zinc',
        'BOD': 'BOD5, mass per volume',
    }

    mass_ignores = ['PO4', 'NH4']

    mass_conversions_for_dry_mass = {
        'TP': (31 + 4 * 16) / 31,
        'TKN': 18 / 14,
        'COD': (1 / COD_TOC_ratio['value']) * 180 / (6 * 12)  # based on glucose
    }

    dry_mass = 0
    for prop in prop_dicts:
        if 'ecoinvent_id' in prop:
            if prop['id'] in mass_ignores:
                pass
            if prop['id'] in mass_conversions_for_dry_mass:
                dry_mass += prop['value'] * mass_conversions_for_dry_mass[prop['id']]
            else:
                dry_mass += prop['value']
    return dry_mass


def mass_properties(prop_dicts, COD_TOC_ratio):
    dry_mass = calculate_dry_mass_of_ww(prop_dicts, COD_TOC_ratio)
    wet_mass = 1000 + dry_mass
    dry_mass_comment = "The dry mass is estimated making a number of assumptions." \
                       "(1) Chemical oxygen demand is first converted to Total Organic Carbon (reported) as C " \
                       "based on a COD/TOC ratio of {}, and then converted to a total mass assuming all the carbon " \
                       "assuming all the carbon is in glucose (C6H12O6). (2) All Nitrogen in TKN is converted to total mass " \
                       "using the simplification that it is all present as ammonia. (3) All Phosphorous in TP is converted " \
                       "to mass assuming it is present as PO4-".format(COD_TOC_ratio)
    return [
        {
            'name': 'dry mass',
            'amount': dry_mass,
            'comment': dry_mass_comment,
            'unit': 'kg',
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [4, 1, 1, 1, 1],
                'comment': "Pedigree scores associated with conversion of COD, TKN and TP to molar masses. " \
                           "Uncertainty does not account for uncertainty of the actual wastewater composition."
            },

        },
        {
            'name': 'wet mass',
            'amount': 1000 + dry_mass,
            'comment': "Based on the mass of 1m3 of water + mass of all constituents of wastewater. " \
                       "Assumes the volume of constituents other than water is negligible.",
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [1, 1, 1, 1, 1],
                'comment': "Contribution to uncertainty of dry mass assumed negligible."
            },
            'unit': 'kg'
        },
        {
            'name': 'water in wet mass',
            'amount': 1000,
            'comment': "Based on the mass of 1m3 of water",
            'uncertainty': no_uncertainty,
            'unit': 'kg'
        },
        {
            'name': 'water content',
            'amount': 1000 / dry_mass,
            'comment': "Based on the mass of 1m3 of water",
            'unit': 'dimensionless',
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [1, 1, 1, 1, 1],
                'comment': "Contribution to uncertainty of dry mass assumed negligible."
            }
        },
    ]

def carbon_properties(COD, COD_TOC_ratio, fraction_C_fossil):
    C = COD / COD_TOC_ratio['value']
    return [
        {
            'name': 'carbon content, fossil',
            'amount': C * fraction_C_fossil['value'],
            'comment': "Based on an estimated COD to TOC conversion factor of {} and a fraction of " \
                       "C that is fossil as {}.".format(COD_TOC_ratio, fraction_C_fossil),
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'comment': "Uncertainty associated with the COD to TOC ratio and the " \
                           "fraction of carbon that is fossil."
            },
            'unit': 'dimensionless',
        },
        {
            'name': 'carbon content, non-fossil',
            'amount': C * (1 - fraction_C_fossil['value']),
            'comment': "Based on an estimated COD to TOC conversion factor of {} and a fraction of " \
                       "C that is fossil as {}.".format(COD_TOC_ratio, fraction_C_fossil),
            'unit': 'dimensionless',
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'unit': 'dimensionless',
                'comment': "Uncertainty associated with the COD to TOC ratio and the " \
                           "fraction of carbon that is fossil."
            },
        }
    ]

def add_DOC_TOC(COD, VSS, COD_TOC_ratio):
    TOC = COD / COD_TOC_ratio['value']
    DOC = TOC - VSS * 0.5
    return [
        {
            'name': 'mass concentration, TOC',
            'amount': TOC,
            'comment': "estimated from the COD to TOC_ratio ({}).".format(
                COD_TOC_ratio
            ),
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'comment': "Uncertainty associated with the COD to TOC ratio, VSS amount and COD amount."
            },
            'unit': 'kg/m3',
        },
        {
            'name': 'mass concentration, DOC',
            'amount': DOC,
            'comment': "DOC is calculated as Total Organic Carbon (TOC) - Particulate Organics (PO). " \
                       "DOC is estimated from the COD to TOC_ratio ({}). " \
                       "PO is estimated using a C to Volatile Suspended Solids (VSS) ratio of 0.5 gC/gVSS. " \
                       "VSS is estimated as {}.".format(COD_TOC_ratio, VSS),
            'uncertainty': {
                'variance': 0,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'comment': "Uncertainty associated with the COD to TOC ratio"
            },
            'unit': 'kg/m3',
        }
    ]

def non_obligatory_properties(prop_dicts, MD):
    non_obligatory_props = []
    for prop_dict in prop_dicts:
        if "ecoinvent_id" in prop_dict and prop_dict["ecoinvent_id"] is not False:
            prop = {}
            prop['name'] = get_prop_name(MD, prop_dict["ecoinvent_id"])
            prop['amount'] = prop_dict["value"]
            prop['comment'] = get_prop_comment(MD, prop_dict["ecoinvent_id"])
            prop['unit'] = get_prop_unit(MD, prop_dict["ecoinvent_id"])
            if prop_dict['id'] in metals:
                prop['uncertainty'] = {
                                          'variance': 0.65,
                                          'pedigreeMatrix': [1, 1, 1, 1, 1],
                                          'comment': "Default basic uncertainty"
                                      }
            elif prop_dict['id'] in non_metals:
                prop['uncertainty'] = {
                                          'variance': 0.04,
                                          'pedigreeMatrix': [1, 1, 1, 1, 1],
                                          'comment': "Default basic uncertainty"
                                      }
            else:
                print("{} didn't get uncertainty".format(prop_dict['id']))
                prop['uncertainty']=no_uncertainty
            non_obligatory_props.append(prop)
    return non_obligatory_props

def all_ww_props(prop_dicts, COD_TOC_ratio, fraction_C_fossil, MD):
    mass_props = mass_properties(prop_dicts, COD_TOC_ratio)
    COD = [prop_dict['value'] for prop_dict in prop_dicts if prop_dict['id']=='COD'][0]
    VSS = [prop_dict['value'] for prop_dict in prop_dicts if prop_dict['id'] == 'VSS'][0]
    C_props = carbon_properties(COD, COD_TOC_ratio, fraction_C_fossil)
    DOC_TOC = add_DOC_TOC(COD, VSS, COD_TOC_ratio)
    others = non_obligatory_properties(prop_dicts, MD)
    all_mass_props = [prop for prop in mass_props]
    all_C_props = [prop for prop in C_props]
    all_DOC_TOC_props = [prop for prop in DOC_TOC]
    all_others_props = [prop for prop in others]

    return all_mass_props + all_C_props + all_DOC_TOC_props + all_others_props



"""
if __name__=='__main__':
    from pycode.load_master_data import load_MD
    MD = load_MD(r'c:/mypy/code/wastewater_treatment_tool')
    p_dicts =[
            {
                "id": "Q",
                "value": 22700,
                "unit": "m3/d",
                "descr": "Flowrate"
            },
            {
                "id": "T",
                "value": 12,
                "unit": "ºC",
                "descr": "Temperature"
            },
            {
                "id": "COD",
                "value": 0.0003,
                "unit": "kkg/m3_as_O2",
                "descr": "Total_chemical_oxygen_demand",
                "ecoinvent_id": "3f469e9e-267a-4100-9f43-4297441dc726"
            },
            {
                "id": "TKN",
                "value": 0.000035000000000000004,
                "unit": "kkg/m3_as_N",
                "descr": "Total_Kjedahl_nitrogen",
                "ecoinvent_id": "98549452-463c-463d-abee-a95c2e01ade3"
            },
            {
                "id": "TP",
                "value": 0.000006,
                "unit": "kkg/m3_as_P",
                "descr": "Total_phosphorus",
                "ecoinvent_id": "8e73d3fb-bb81-4c42-bfa6-8be4ff13125d"
            },
            {
                "id": "BOD",
                "value": 0.00014000000000000001,
                "unit": "kkg/m3_as_O2",
                "canBeEstimated": True,
                "descr": "Total_5d_biochemical_oxygen_demand",
                "ecoinvent_id": "dd13a45c-ddd8-414d-821f-dfe31c7d2868"
            },
            {
                "id": "sBOD",
                "value": 0.00007000000000000001,
                "unit": "kkg/m3_as_O2",
                "canBeEstimated": True,
                "descr": "Soluble_BOD"
            },
            {
                "id": "sCOD",
                "value": 0.000132,
                "unit": "kkg/m3_as_O2",
                "canBeEstimated": True,
                "descr": "Soluble_COD"
            },
            {
                "id": "bCOD",
                "value": 0.000224,
                "unit": "kkg/m3_as_O2",
                "canBeEstimated": True,
                "descr": "Biodegradable_COD_(a_typical_value_is:_bCOD=1.6·BOD)"
            },
            {
                "id": "rbCOD",
                "value": 0.00008,
                "unit": "kkg/m3_as_O2",
                "canBeEstimated": True,
                "descr": "Readily_biodegradable_COD_(bsCOD=complex+VFA)"
            },
            {
                "id": "VFA",
                "value": 0.000014999999999999999,
                "unit": "kkg/m3_as_O2",
                "canBeEstimated": True,
                "descr": "Volatile_Fatty_Acids_(Acetate)"
            },
            {
                "id": "VSS",
                "value": 0.000059999999999999995,
                "unit": "kkg/m3",
                "canBeEstimated": True,
                "descr": "Volatile_suspended_solids"
            },
            {
                "id": "TSS",
                "value": 0.00007000000000000001,
                "unit": "kkg/m3",
                "canBeEstimated": True,
                "descr": "Total_suspended_solids"
            },
            {
                "id": "NH4",
                "value": 0.000025,
                "unit": "kkg/m3_as_N",
                "canBeEstimated": True,
                "descr": "Ammonia_influent",
                "ecoinvent_id": "f7fa53fa-ee5f-4a97-bcd8-1b0851afe9a6"
            },
            {
                "id": "PO4",
                "value": 0.000005,
                "unit": "kkg/m3_as_P",
                "canBeEstimated": True,
                "descr": "Ortophosphate_influent",
                "ecoinvent_id": "7fe01cf6-6e7b-487f-b37e-32388640a8a4"
            },
            {
                "id": "Alkalinity",
                "value": 0.00014000000000000001,
                "unit": "kkg/m3_as_CaCO3",
                "canBeEstimated": True,
                "descr": "Influent_alkalinity"
            },
            {
                "id": "Al",
                "value": 0.0000010379,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Aluminium",
                "ecoinvent_id": "77154d2e-4b05-48f2-a89a-789acd170497"
            },
            {
                "id": "As",
                "value": 9e-10,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Arsenic",
                "ecoinvent_id": "b321f120-4db7-4e7c-a196-82a231023052"
            },
            {
                "id": "Ca",
                "value": 0.000050834,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Calcium",
                "ecoinvent_id": "ddbab0d1-b156-41bc-98e5-fb680285d7cd"
            },
            {
                "id": "Cd",
                "value": 3e-10,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Cadmium",
                "ecoinvent_id": "1111ac7e-20df-4ab4-9e02-57821894372c"
            },
            {
                "id": "Cl",
                "value": 0.000030030999999999998,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Chlorine",
                "ecoinvent_id": "468e50e8-1960-4eba-bc1a-a9938a301694"
            },
            {
                "id": "Co",
                "value": 1.6e-9,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Cobalt",
                "ecoinvent_id": "2f7030b9-bafc-4b43-8504-deb8b5044130"
            },
            {
                "id": "Cr",
                "value": 1.22e-8,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Chromium",
                "ecoinvent_id": "bca4bb32-f701-46bb-ba1e-bad477c19f7f"
            },
            {
                "id": "Cu",
                "value": 3.7400000000000004e-8,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Copper",
                "ecoinvent_id": "e7451d8a-77af-44e0-86cf-ccd17ac84509"
            },
            {
                "id": "F",
                "value": 3.28e-8,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Fluorine",
                "ecoinvent_id": "763a698f-54d7-4e2a-84a7-9cc8c0271b6a"
            },
            {
                "id": "Fe",
                "value": 0.000007092800000000001,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Iron",
                "ecoinvent_id": "ebf21bca-b7cf-45d0-9d82-bfb80519a970"
            },
            {
                "id": "Hg",
                "value": 2e-10,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Mercury",
                "ecoinvent_id": "a102e6f8-ebc7-450b-a39b-794be96558b7"
            },
            {
                "id": "K",
                "value": 3.989e-7,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Potassium",
                "ecoinvent_id": "8b49eeb7-9caf-4101-b516-eb0aef30d530"
            },
            {
                "id": "Mg",
                "value": 0.0000057071,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Magnesium",
                "ecoinvent_id": "d26c0a60-86aa-41c8-80ee-3acabc4a5095"
            },
            {
                "id": "Mn",
                "value": 5.3e-8,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Manganese",
                "ecoinvent_id": "8d27623b-147c-44e8-93cc-2183eac22991"
            },
            {
                "id": "Mo",
                "value": 9.999999999999999e-10,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Molybdenum",
                "ecoinvent_id": "aa897226-0a91-40e5-aa05-4bae3b9e4213"
            },
            {
                "id": "Na",
                "value": 0.000002186,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Sodium",
                "ecoinvent_id": "7b656e1b-bc07-41cd-bad4-a5b51b6287da"
            },
            {
                "id": "Ni",
                "value": 6.6e-9,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Nickel",
                "ecoinvent_id": "8b574e85-ff07-46bf-a753-f1271299dcf7"
            },
            {
                "id": "Pb",
                "value": 8.600000000000001e-9,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Lead",
                "ecoinvent_id": "71bc04b9-abfe-4f30-ab8f-ba654c7ad296"
            },
            {
                "id": "Si",
                "value": 0.0000031263000000000005,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Silicon",
                "ecoinvent_id": "67065577-4705-4ece-a892-6dd1d7ecd1e5"
            },
            {
                "id": "Sn",
                "value": 3.4e-9,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Tin",
                "ecoinvent_id": "ff888459-10c3-4700-afce-3a024aaf89cf"
            },
            {
                "id": "Zn",
                "value": 1.094e-7,
                "unit": "kkg/m3",
                "isMetal": True,
                "descr": "Influent_Zinc",
                "ecoinvent_id": "6cc518c8-4769-40df-b2cf-03f9fe00b759"
            }
        ]

    all_ww_props(p_dicts, 3, 0.5, MD)
"""