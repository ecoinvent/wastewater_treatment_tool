
import numpy as np
import os
from copy import copy
from pycode.defaults import *

HTML_entities = [['&', '&amp;'],
                 ['<', '&lt;'], 
                 ['>', '&gt;'], 
                 ['¢', '&cent;'], 
                 ['£', '&pound;'], 
                 ['¥', '&yen;'], 
                 ['€', '&euro;'], 
                 ['©', '&copy;'], 
                 ['®', '&#174;'] 
                 ]

tag_prefix = '{http://www.EcoInvent.org/EcoSpold02}'

class GenericObject:
    """ Generic object"""
    def __init__(self, d, object_type):
        self.template_name = '{}_2.xml'.format(object_type)
        assert type(d) == dict
        for key, value in d.items():
            setattr(self, key, value)
            

def recursive_rendering(e, env, result_folder, result_filename):
    if type(e) == GenericObject:
        template = env.get_template(e.template_name)
        attr_list = set([a for a in dir(e) if '__' not in a])
        attr_list.difference_update(set(['render', 'template_name']))
        rendered = {attribute: recursive_rendering(getattr(e, attribute), 
             env, result_folder, result_filename) for attribute in attr_list}
        rendered = template.render(**rendered)
        if '\ufeff' in rendered:
            rendered = rendered.replace('\ufeff', '')
        if e.template_name == 'Dataset_2.xml':
            writer = open(os.path.join(result_folder, result_filename), 'w', encoding = 'utf-8')
            writer.write(rendered)
            writer.close()
            print('file "%s" successfully created in folder %s' % (result_filename, result_folder))
    elif type(e) in [list, tuple, set]:
        rendered = [recursive_rendering(ee, env, result_folder, result_filename) for ee in e]
    elif type(e) == str:
        rendered = replace_HTML_entities(e)
    elif type(e) in [int, float, np.float64, bool, np.bool_, 
             np.int64, np.long, type(None)]:
        rendered = copy(e)
    else: 
        raise ValueError('rendering for type "%s" not implemented' % type(e))
    return rendered    
    

def replace_HTML_entities(s):
    #replace HTML entities in a character string
    if s != None and type(s) == str:
        #test if replacement has already occured
        do_it = True
        for before, after in HTML_entities:
            if after in s:
                do_it = False
        if do_it:
            for before, after in HTML_entities:
                s = s.replace(before, after)
        s = s.replace('"', "'") # the character " creates problems in attributes
    return s
    

def create_empty_dataset():
    ''' Create an empty 'dataset' dictionary with all the right keys.'''    

    dataset = {}    
    # Mandatory fixed values
    dataset['activityDataset'] = 'activityDataset'
    dataset['inheritanceDepth'] = 0
    dataset['type'] = 1
    dataset['specialActivityType'] = 0
    dataset['isDataValidForEntirePeriod'] = 'true'
    dataset['macroEconomicScenarioName'] = 'Business-as-Usual'
    dataset['macroEconomicScenarioId'] = 'd9f57f0a-a01f-42eb-a57b-8f18d6635801'    
    dataset['tag'] = ['Treatment']
        
    # Mandatory values fixed to None (will not show in the rendered template)
    empty_fields = ['parentActivityId',
                    'parentActivityContextId',
                    'energyValues',
                    'masterAllocationPropertyId', 
                    'masterAllocationPropertyIdOverwrittenByChild', 
                    'activityNameContextId', 'geographyContextId', 
                    'macroEconomicScenarioContextId', 
                    'macroEconomicScenarioContextId', 
                    'originalActivityDataset', 
                    'macroEconomicScenarioComment',
                    ]
    dataset.update({f: None for f in empty_fields})   
    # Add lists to dict elements that are exchange lists
    dataset['Properties'] = []
    for group in ['ReferenceProduct',
                  'ByProduct',
                  'FromTechnosphere',
                  'FromEnvironment',
                  'ToEnvironment',
                  ]:
        dataset[group] = [] 

    d = {'personContextId': None, 
         'isActiveAuthor': 'false', 
         'personId': '788d0176-a69c-4de0-a5d3-259866b6b100', 
         'personName': '[Current User]', 
         'personEmail': 'no@email.com'
         }
    dataset['dataEntryBy'] = GenericObject(d, 'DataEntryBy')

    # DataGeneratorAndPublication
    # Assume the author is the tool author

    #mandatory values
    d = {'isCopyrightProtected': 'true', 
         'accessRestrictedTo': 1, 
         'dataPublishedIn': 0}
    empty_fields = ['personContextId', 'publishedSourceContextId', 'publishedSourceIdOverwrittenByChild', 
      'companyContextId', 'companyIdOverwrittenByChild', 'publishedSourceId', 'companyCode', 
      'publishedSourceYear', 'publishedSourceFirstAuthor', 'pageNumbers', 'companyId']
    d.update({f: None for f in empty_fields})
    #variable fields: depends on the user - assume constant for now
    # See original code to deal with case where we want to make this variable
    d.update({
            'personName': 'Pascal Lesage', #TODO
            'personId': '788d0176-a69c-4de0-a5d3-259866b6b100',
            'personEmail': 'pascal.lesage@polymtl.ca',
            'companyName': 'CIRAIG'
            })    
    dataset['dataGeneratorAndPublication'] = GenericObject(
                                                d,
                                               'DataGeneratorAndPublication'
                                               )
    # File attribute- all default values    
    #mandatory values
    d = {'majorRelease': 3, 
         'minorRelease': 4, 
         'majorRevision': 0, 
         'minorRevision': 1, 
         'defaultLanguage': 'en', 
         }
    empty_fields = ['internalSchemaVersion', 'creationTimestamp', 'lastEditTimestamp', 
      'fileGenerator', 'fileTimestamp', 'contextId', 'contextName', 'requiredContext']
    d.update({f: None for f in empty_fields})
    dataset['fileAttributes'] = GenericObject(d, 'FileAttribute')

    # Classifications: all default values
    #mandatory values
    d = {'classificationSystem': 'ISIC rev.4 ecoinvent', 
         'classificationValue': '3700:Sewerage', 
         'classificationId': 'a84d0ee4-d77c-4905-b876-3ef60873c763',
         'classificationContextId': None,
         }
    dataset['classifications'] = [GenericObject(d, 'TClassification')]
    
    return dataset


def create_empty_exchange():
    empty_fields = ['intermediateExchangeContextId', 'activityLinkId', 
        'activityLinkContextId', 'activityLinkIdOverwrittenByChild', 
        'casNumber', 'intermediateExchangeId', 'elementaryExchangeId', 
        'elementaryExchangeContextId', 'formula', 'productionVolumeAmount', 
        'productionVolumeVariableName', 'productionVolumeMathematicalRelation', 
        'productionVolumeSourceIdOverwrittenByChild', 'productionVolumeSourceId', 
        'productionVolumeSourceContextId', 'productionVolumeSourceYear', 
        'productionVolumeSourceFirstAuthor', 'unitContextId', 'mathematicalRelation', 
        'variableName', 'isCalculatedAmount', 'sourceId', 'sourceContextId', 
        'sourceIdOverwrittenByChild', 'sourceYear', 'sourceFirstAuthor', 
        'pageNumbers', 'specificAllocationPropertyId', 'specificAllocationPropertyContextId', 
        'specificAllocationPropertyIdOverwrittenByChild', 'productionVolumeComment', 
        'productionVolumeUncertainty', 'tag', 'classifications', 'subcompartmentId', 
        'compartment', 'subcompartment'
        ]
    return {f: None for f in empty_fields}


def create_empty_uncertainty():
    empty_fields = ['minValue',
                    'mostLikelyValue',
                    'maxValue',
                    'standardDeviation95',
                    'comment',
                    ]
    return {f: None for f in empty_fields}
    

def add_uncertainty(o, uncertainty_dict, PV=False):
    if PV==False and o['amount'] <= 0:
        pass
    else:
        unc = create_empty_uncertainty()
        if PV:
            unc['field'] = 'productionVolumeUncertainty'
            unc['meanValue'] = o['productionVolumeAmount']
        else:
            unc['field'] = 'uncertainty'
            unc['meanValue'] = o['amount']
        unc['type'] = 'lognormal'
        unc['mu'] = np.log(unc['meanValue'])
        unc['variance'] = uncertainty_dict['variance']
        if uncertainty_dict['pedigreeMatrix'] is not None:
            assert set(uncertainty_dict['pedigreeMatrix']).issubset(set([1, 2, 3, 4, 5, 1., 2., 3., 4., 5.]))
            pedigree_factors = np.array(
                        [
                            [0, 0., .0006, .002, .008, .04],
                            [0, 0., .0001, .0006, .002, .008],
                            [0, 0., .0002, .002, .008, .04],
                            [0, 0., 2.5e-5, .0001, .0006, .002],
                            [0, 0., .0006, .008, .04, .12]
                        ]
                            )
            unc['varianceWithPedigreeUncertainty'] = copy(uncertainty_dict['variance'])
            for i in range(len(uncertainty_dict['pedigreeMatrix'])):
                unc['varianceWithPedigreeUncertainty'] += pedigree_factors[i, uncertainty_dict['pedigreeMatrix'][i]]
            unc['pedigreeMatrix'] = uncertainty_dict['pedigreeMatrix']
        else:
            unc['varianceWithPedigreeUncertainty'] = uncertainty_dict['variance']
        unc['comment'] = uncertainty_dict['comment']
        o[unc['field']] = GenericObject(unc, 'TUncertainty')
    return o
    

def create_empty_property():
    empty_fields = ['propertyContextId', 'unitContextId', 'isDefiningValue', 
    'isCalculatedAmount', 'sourceId', 'sourceContextId', 
    'sourceIdOverwrittenByChild', 'sourceYear', 'sourceFirstAuthor', 
    'mathematicalRelation', 'variableName', 'uncertainty', 'comment']
    return {field: None for field in empty_fields}


def get_prop_name(MD, prop_id):
    return MD['Properties'][MD['Properties']['id']==prop_id].index.tolist()[0]


def get_prop_unit(MD, prop_id):
    return MD['Properties'][MD['Properties']['id']==prop_id]['unitName'].values[0]


def get_prop_comment(MD, prop_id):
    return MD['Properties'][MD['Properties']['id']==prop_id]['comment'].values[0]


def get_prop_id(MD, prop_name):
    return MD['Properties'].loc[prop_name, 'id'].values[0]


def generate_WW_properties(MD, passed_props):
    required = [
        'water in wet mass',
        'water content',
        'dry mass',
        'carbon content, fossil',
        'carbon content, non-fossil',
        'wet mass',
    ]

    reported = [
            {
                'name': get_prop_name(MD, k),
                'amount': v,
                'unit': get_prop_unit(MD, k),
                'comment': get_prop_comment(MD, k),
                'uncertainty': default_WW_property_uncertainty,
            }
        for k, v in passed_props.items()
        ]

    ignore_in_mass_balance = [
        'BOD5, mass per volume',  # Expressed as O2
        'COD, mass per volume',  # Expressed as O2
        'mass concentration, DOC',  # Included in TOC
        'mass concentration, nitrogen',  # Sum parameter, already accounting for constituents
        'mass concentration, sulfur', # Sum parameter, already accounting for constituents
        'mass concentration, phophorus',  # Sum parameter, already accounting for constituents
        'mass concentration, dissolved Kjeldahl Nitrogen as N',  # Already accounting for N
        'mass concentration, Kjeldahl Nitrogen as N'  # Already accounting for N
    ]

    # Assumption: volume of substances in water is negligible
    wet_mass = 1000  # Mass of 1m3 of water
    dry_mass = 0
    for prop in reported:
        if prop['name'] in ignore_in_mass_balance:
            pass
        elif prop['name'] == "mass concentration, dissolved ammonia NH4 as N":
            dry_mass+=prop['amount']* 18/14
        elif prop['name'] == "mass concentration, dissolved nitrate NO3 as N":
            dry_mass+=prop['amount']* (14+3*16)/14
        elif prop['name'] == "mass concentration, dissolved nitrite NO2 as N":
            dry_mass+=prop['amount']* (14+2*16)/14
        elif prop['name'] == "mass concentration, particulate nitrogen":
            dry_mass+=prop['amount']* (14)/14 #TODO --> missing deafult N content of particulate nitrogen
        elif prop['name'] == "mass concentration, dissolved organic nitrogen as N":
            dry_mass+=prop['amount']* (14)/14 #TODO --> missing deafult N content of dissolved nitrogen, also check if NH4, NO3 and NO2 are included...
        elif prop['name'] == "mass concentration, dissolved phosphate PO4 as P":
            dry_mass+=prop['amount']* (31+4*16)/31
        elif prop['name'] == "mass concentration, particulate phophorus":
            dry_mass+=prop['amount']* (31)/31  #TODO-->missing default P content of dissolved nitrogen, also check if NH4, NO3 and NO2 are included...
        elif prop['name'] == "mass concentration, dissolved sulfate SO4 as S":
            dry_mass+=prop['amount']* (32+4*16)/32
        elif prop['name'] == "mass concentration, particulate sulfur":
            dry_mass+=prop['amount']* (32)/32  #TODO-->missing S content of particulate sulfur
        else:
            dry_mass += prop['amount']

    obligatory = [
        {
            'name': 'wet mass',
            'amount': 1000 + dry_mass,
            'comment': "Based on the mass of 1m3 of water + mass of all constituents of wastewater. "\
                       "Assumes the volume of constituents other than water is negligible.",
            'uncertainty': no_uncertainty,
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
            'amount': 1000/wet_mass,
            'comment': "Based on the mass of 1m3 of water",
            'unit': 'dimensionless',
            'uncertainty': no_uncertainty,
        },
        {
            'name': 'dry mass',
            'amount': dry_mass,
            'comment': "Estimated by summing all constituents of wastewater."\
                       " Uncertainties due to some parameters expressed as constituents "\
                       "(e.g. particulate nitrogen expressed as N)",
            'uncertainty': no_uncertainty,
            'unit': 'kg',
        },
        {
            'name': 'carbon content, fossil',
            'amount': 0,  #TODO-->Estimate C content based on TOC??
            'comment': "TODO",
            'uncertainty': no_uncertainty, #TODO,
            'unit': 'dimensionless',
        },
        {
            'name': 'carbon content, non-fossil',
            'amount': 0,  # TODO-->Estimate C content based on TOC??
            'comment': "TODO",
            'uncertainty': no_uncertainty,  # TODO
            'unit': 'dimensionless',
        }
    ]

    return [prop for prop in [*reported, *obligatory]]

