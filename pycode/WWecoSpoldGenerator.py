# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import uuid
import numpy as np
import pandas as pd
from lxml import objectify
from copy import copy
from pickle import dump, load
from .utils import *
from .load_master_data import load_MD
from .defaults import *
from .placeholders import *
from .arguments import *


class GenericObject:
    """ Generic object"""
    def __init__(self, d, object_type):
        self.template_name = '{}_2.xml'.format(object_type)
        assert type(d) == dict
        for key, value in d.items():
            setattr(self, key, value)
            
class WWecoSpoldGenerator(object):
    """ Class to organize all the data and functions associated with ecoSpold generation.
    
    Is instantiated with data passed from the JavaScript wastewater treatment tool.
    """
    
    #def __init__(self, root_dir, untreated_fraction, overload_loss_fraction_particulate,
    #             overload_loss_fraction_dissolved, WW_type, technology, capacity):
    def __init__(self, **kwargs):
        check_for_missing_args(required_arguments, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)        
        assert self.tool_use_type in ('average', 'specific'), "tool_use_type should be average or specific"
        check_for_missing_args(other_required_args[self.tool_use_type], kwargs)
        self.dataset = self.create_empty_dataset()
        self.MD = load_MD(self.root_dir)
        self.dataset['activityName']=self.generate_activity_name()
        self.generate_activityNameId()
        self.generate_time_period()
        self.generate_geography()
        self.generate_dataset_id()
        self.generate_activityIndex()
        self.generate_technology_level()
    
    def generate_ecoSpold2(self):
        self.dataset['has_userMD'] = False
        for field in ['ActivityNames', 'Sources', 'activityIndexEntry', 'Persons', 'IntermediateExchanges']:
            if field in self.dataset and len(self.dataset[field]) > 0:
                self.dataset['has_userMD'] = True
                break
        self.dataset['exchanges'] = []
        for group in ['ReferenceProduct', 'ByProduct', 'FromTechnosphere', 'FromEnvironment', 'ToEnvironment']:
        #groups need to appear in a specific order
            self.dataset['exchanges'].extend(self.dataset[group])

        self.dataset = GenericObject(self.dataset, 'Dataset')
        #loading the template environment
        template_path = os.path.join(self.root_dir, 'templates')
        env = Environment(loader=FileSystemLoader(template_path), 
                          keep_trailing_newline = True, 
                          lstrip_blocks = True, 
                          trim_blocks = True)
        rendered = self.recursive_rendering(self.dataset, env, os.path.join(self.root_dir, 'output'), "{}.spold".format(self.dataset['id']))
    
    @staticmethod
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
        elif type(e) in [int, float, numpy.float64, bool, numpy.bool_, 
                 numpy.int64, numpy.long, type(None)]:
            rendered = copy(e)
        else: 
            raise ValueError('rendering for type "%s" not implemented' % type(e))
        return rendered    
    
    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
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

    def append_exchange(self, exc, #exchange dictionary, see detail below
                        properties = [], # If relevant. list of tuples with appropriate format.
                        uncertainty = None, #Uncertainty dict
                        PV_uncertainty = None #Relevant for exchanges with production volumes only
                        ):
        """
        Exc:All exchanges are passed as dictionaries. 
            All exchanges shall have the following keys:
                group, name, comment, unitName, amount
            Exchanges with group == ReferenceProduct or ByProduct shall also 
                have a productionVolumeAmount and productionVolumeComment.
            Exchanges with the group == FromEnvironment of ToEnvironment shall
                also have a compartment and subcompartment
        properties: list of tuples with the following data:
            (property_name, amount, comment, uncertainty)                                                 }
        `uncertainty` comes as dict with format {'variance': variance,
                                                 'pedigreeMatrix': [x,x,x,x,x],
                                                 'comment': comment
                                                 }
        PV_uncertainty
        """
        # Add unitId to exchange
        exc['unitId'] = self.MD['Units'].loc[exc['unitName'], 'id']

        # Add IntermediateExchange to MD if new:
        if exc['group'] in ['ReferenceProduct', 'ByProduct', 'FromTechnosphere'] \
            and exc['name'] not in self.MD['IntermediateExchanges'].index:
            self.new_intermediate_exchange(exc)
        # Generate UUID for exchange. New UUID for each exchange/dataset combination
        l = [self.dataset[field] for field in [
                                        'activityName',
                                        'geography',
                                        'startDate',
                                        'endDate'
                                        ]
            ]
        l.extend(str(exc[field]) for field in ['name',
                                               'compartment',
                                               'subcompartment']
            )
        
        exc['id'] = make_uuid(l)
        
        # assign groupType
        if 'From' in exc['group']:
            exc['groupType'] = 'inputGroup'
        else:
            exc['groupType'] = 'outputGroup'

        # If elementary flow, add some fields.
        # Note: assumed all elementary flows already in MD
        if 'Environment' in exc['group']:
            ee = (exc['name'], exc['compartment'], exc['subcompartment'])
            sel = self.MD['ElementaryExchanges'].loc[ee]
            if isinstance(sel, pd.DataFrame):
                if len(sel) > 1:
                    raise ValueError('Multiple MD entries corresponding to %s, %s, %s' % ee)
                sel = sel.iloc[0]
            exc['elementaryExchangeId'] = sel['id']
            exc['exchangeType'] = 'elementaryExchange'
            exc['subcompartmentId'] = self.MD['Compartments'].loc[ee[1:], 'subcompartmentId']
            exc['groupCode'] = 4
            if ee in self.MD['ElementaryExchanges prop.'].index:
                property_sel = self.MD['ElementaryExchanges prop.'].loc[[ee]]
            else:
                property_sel = pd.DataFrame()
       
        else: # If intermediateExchange
            sel = self.MD['IntermediateExchanges'].loc[exc['name']]
            exc['intermediateExchangeId'] = sel['id'] # There even if new because added above
            exc['exchangeType'] = 'intermediateExchange'
            if exc['group'] == 'ReferenceProduct':
                exc['groupCode'] = 0
            elif exc['group'] == 'FromTechnosphere':
                exc['groupCode'] = 5
            elif exc['group'] == 'ByProduct':
                exc['groupCode'] = 2
            else:
                raise ValueError('"%s" is not a valid group' % exc['group'])
            if exc['name'] in self.MD['IntermediateExchanges prop.'].index:
                property_sel = self.MD['IntermediateExchanges prop.'].loc[[exc['name']]]
            else:
                property_sel = pd.DataFrame()
            #'add classifications': issue #1
        #make sure the unit is the same as the MD
        assert exc['unitName'] == sel['unitName']
        
        #use MD properties for the properties not specified by the user
        if len(property_sel) > 0:
            present_properties = [p[0] for p in properties]
            for i, p in property_sel.iterrows():
                if p['propertyName'] not in present_properties:
                    properties.append(
                            (p['propertyName'],
                             p['amount'],
                             p['unitName'],
                             "Default value. {}".format(p['comment']),
                             None)
                            )
        exc = self.add_property(exc, properties)
        
        if uncertainty:
            exc = self.add_uncertainty(exc,
                                  uncertainty['pedigreeMatrix'],
                                  uncertainty['variance'],
                                  uncertainty['comment']
                                  )
        if PV_uncertainty:
            exc = self.add_uncertainty(exc,
                                  PV_uncertainty['pedigreeMatrix'],
                                  PV_uncertainty['variance'],
                                  PV_uncertainty['comment'],
                                  PV = True)
        self.dataset[exc['group']].append(GenericObject(exc, 'Exchange'))
        return None

    @staticmethod
    def create_empty_uncertainty():
        empty_fields = ['minValue',
                        'mostLikelyValue',
                        'maxValue',
                        'standardDeviation95',
                        'comment',
                        ]
        return {f: None for f in empty_fields}
        
    @staticmethod
    def add_property(exc, properties):
        exc['properties'] = []
        for property_name, amount, unit, comment, unc in properties:
            p = create_empty_property()
            p['name'] = property_name
            if property_name in self.MD['Properties'].index:
                sel = self.MD['Properties'].loc[property_name]
                p['propertyId'] = sel['id']
                if not is_empty(sel['unitName']):
                    assert unit == sel['unitName'], "{}, {}, {}".format(property_name, unit, sel['unitName'])
                    p['unitName'] = unit
                    p['unitId'] = self.MD['Units'].loc[p['unitName'], 'id']
            else:
                p['propertyId'] = make_uuid(property_name)
                p['unitName'] = unit
                p['unitId'] = self.MD['Units'].loc[p['unitName'], 'id']
                self.dataset['Properties'].append(GenericObject(p,
                                            'user_MD_Properties'
                                            ))
            p['amount'] = amount
            p['comment'] = comment
            if not is_empty(unc):
                p = self.add_uncertainty(p,
                                    unc['pedigreeMatrix'],
                                    unc['variance'],
                                    unc['comment'])
            exc['properties'].append(GenericObject(p, 'TProperty'))
        return exc
    

    def create_empty_property():
        empty_fields = ['propertyContextId', 'unitContextId', 'isDefiningValue', 
        'isCalculatedAmount', 'sourceId', 'sourceContextId', 
        'sourceIdOverwrittenByChild', 'sourceYear', 'sourceFirstAuthor', 
        'mathematicalRelation', 'variableName', 'uncertainty', 'comment']
        return {field: None for field in empty_fields}

    @staticmethod
    def add_uncertainty(o, pedigreeMatrix, variance, comment, PV = False):
        unc = create_empty_uncertainty()
        if PV:
            unc['field'] = 'productionVolumeUncertainty'
            unc['meanValue'] = o['productionVolumeAmount']
        else:
            unc['field'] = 'uncertainty'
            unc['meanValue'] = o['amount']
        unc['type'] = 'lognormal'
        unc['mu'] = numpy.log(unc['meanValue'])
        unc['variance'] = variance
        assert set(pedigreeMatrix).issubset(set([1, 2, 3, 4, 5, 1., 2., 3., 4., 5.]))
        pedigree_factors = numpy.array([[0, 0., .0006, .002, .008, .04], 
                        [0, 0., .0001, .0006, .002, .008], 
                        [0, 0., .0002, .002, .008, .04], 
                        [0, 0., 2.5e-5, .0001, .0006, .002], 
                        [0, 0., .0006, .008, .04, .12]])
        unc['varianceWithPedigreeUncertainty'] = copy(variance)
        for i in range(len(pedigreeMatrix)):
            unc['varianceWithPedigreeUncertainty'] += pedigree_factors[i, pedigreeMatrix[i]]
        unc['pedigreeMatrix'] = pedigreeMatrix
        unc['comment'] = comment
        o[unc['field']] = GenericObject(unc, 'TUncertainty')
        return o
    
    def new_intermediate_exchange(self, exc):
        fields = ['name', 'unitName', 'casNumber', 'comment', 'unitId']
        to_add = {field: exc[field] for field in fields}
        to_add['id'] = make_uuid(exc['name'])
        tab = 'IntermediateExchanges'
        #add entry to user MD
        if tab not in self.dataset:
            self.dataset[tab] = []
        self.dataset[tab].append(GenericObject(to_add, 'user_MD_IntermediateExchanges'))
        #add entry to MD
        new_entry = list_to_df([to_add]).set_index('name')
        self.MD['IntermediateExchanges'] = pd.concat([self.MD[tab], new_entry])
        return None

    def generate_reference_exchange(
                              self,
                              exc_comment,
                              PV,
                              PV_uncertainty,
                              PV_comment,
                              #WW_prop_df, TODO
                              WW_obligatory_properties,
                              #overload_loss_fraction_particulate,
                              #overload_loss_fraction_dissolved,
                              ):
        exc = self.create_empty_exchange()
        if self.WW_type=='municipal average':
            name = 'wastewater, municipal average'
        else:
            name = 'wastewater, {}'.format(self.WW_type)
            
        exc.update({
                'group': 'ReferenceProduct',
                'unitName': 'm3',
                'amount': -1.,
                'productionVolumeAmount': PV,
                'productionVolumeComment': PV_comment, 
                'comment': exc_comment, 
                'name': name,
               })
        
        #PV_uncertainty
        PV_uncertainty = PV_uncertainty
        # Properties
        """
        overflow_losses_dict = calc_overflow_losses_dict(WW_prop_df,
                                                         overload_loss_fraction_particulate,
                                                         overload_loss_fraction_dissolved
                                                         )
        properties_list = generate_properties_list(WW_prop_df, overflow_losses_dict)
        properties_list += WW_obligatory_properties
        """
        # Append exchange to dataset
        self.append_exchange(exc, properties=[], 
                            uncertainty = None, PV_uncertainty = PV_uncertainty
                            )
        return None
    def generate_activity_name(self):
        if self.WW_type == "municipal average":
            WW_type_name = ", municipal average"
        else:
            WW_type_name = " {}".format(self.WW_type)
        
        if self.act_type == 'untreated discharge':
            return "direct discharge of wastewater{}".format(WW_type_name)
            
        else:
            if self.tool_use_type == "average":
                return "treatment of wastewater{}, average treatment".format(WW_type_name)
            else:
                return "treatment of wastewater{}, {}, {}".format(WW_type_name, self.technology, self.capacity)
        
    def generate_activityNameId(self):
        ''' Return activityNameId from MD or create one.'''

        if self.dataset['activityName'] in self.MD['ActivityNames'].index:
            self.dataset.update({'activityNameId':
                self.MD['ActivityNames'].loc[dataset['activityName'], 'id']
                            })
        else:
            print("new name {} identified, generating new UUID".format(
                    self.dataset['activityName']))
            activityNameId = make_uuid(self.dataset['activityName'])
            #creating a new user masterdata entry
            d = {'id': activityNameId, 
                 'name': self.dataset['activityName']}
            self.dataset.update(
                       {
                        'activityNameId' : activityNameId,
                        'ActivityNames': [GenericObject(d, 'user_MD_ActivityNames')]
                       }
                    )
                    
    def generate_geography(self):
        self.dataset.update(
            {
                'geography': self.geography,
                'geographyId': self.MD['Geographies'].loc[self.geography, 'id']
                        
            }
        )
        
    def generate_time_period(self):
        if not hasattr(self, 'timePeriodStart'):
            self.timePeriodStart = default_timePeriodStarts
        if not hasattr(self, 'timePeriodEnds'):
            self.timePeriodEnd = default_timePeriodEnds
        self.dataset.update({'startDate':self.timePeriodStart,
                        'endDate':self.timePeriodEnd})
   
    def generate_dataset_id(self):
        '''the activityName, geography, startDate and endDate need to be
            defined first'''
        l = [
            self.dataset['activityName'],
            self.dataset['geography'],
            self.dataset['startDate'],
            self.dataset['endDate']
            ]
        self.dataset.update({'id':make_uuid(l)})

    def generate_activityIndex(self):
        d = {'id': self.dataset['id'], 
             'activityNameId': self.dataset['activityNameId'],
             'geographyId': self.dataset['geographyId'],
             'startDate': self.dataset['startDate'],
             'endDate': self.dataset['endDate'],
             'specialActivityType': self.dataset['specialActivityType'],
             'systemModelId': '8b738ea0-f89e-4627-8679-433616064e82',
             }
        self.dataset['ActivityIndex'] = [GenericObject(d, 'user_MD_ActivityIndex')]

    def generate_activity_boundary_text(self, activity_ends):
        self.dataset.update({'includedActivitiesStart': default_activity_starts,
                             'includedActivitiesEnd': activity_ends
                            })        

    def generate_technology_level(self):
        level_string_to_int = {
                'Undefined':0,
                'New':1,
                'Modern':2,
                'Current':3,
                'Old':4,
                'Outdated':5
                }
        if not hasattr(self, 'technology_level'):
            self.technology_level = default_technology_level
        self.dataset.update({
                'technologyLevel':level_string_to_int[self.technology_level],
                })
            
    def technology_mix_constructor(self):
        return [
            "{0:.0f}%: {}, {}, {}".format(
                d[k]['fraction'],
                d[k]['technology_str'],
                d[k]['capacity'],
                d[k]['location']
                )
        for k in self.technologies_averaged.keys()
        ]
    
    def generate_comment(self, comment_type, list_of_string_comments):
        types_of_comments = [
                'allocationComment',
                'generalComment',
                'geographyComment',
                'technologyComment',
                'timePeriodComment'
                ]
        assert comment_type in types_of_comments, 'no such comment field'
        assert isinstance(list_of_string_comments, list),\
            'list_of_string_comments needs to be a list'
        for comment in list_of_string_comments:
            assert isinstance(comment, str),\
                'Comment should be a string'
        d = {'comments_original': list_of_string_comments}
        self.dataset.update({
                comment_type:GenericObject(d, 'TTextAndImage')
                })

    def  generate_representativeness(self,
                                     samplingProcedure_text,
                                     extrapolations_text,
                                     percent):
        assert all([str(percent).isnumeric(), 0<=percent<=100]),\
            'Percent needs to be a number between 0 and 100'
        assert isinstance(samplingProcedure_text, str),\
            'The sampling procedure text should be a string'
        assert isinstance(extrapolations_text, str),\
            'The extrapolation text should be a string'        
        d = {'systemModelId': '8b738ea0-f89e-4627-8679-433616064e82',
             'systemModelContextId': None,
             'systemModelName': 'Undefined', 
             'reviews': None, 
             'percent': percent,
             'samplingProcedure':samplingProcedure_text,
             'extrapolations':extrapolations_text,
             }
        self.dataset['modellingAndValidation'] = GenericObject(d,
                                                'ModellingAndValidation'
                                                )

 
class WWT_ecoSpold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to WWT dataset""" 
    def __init__(self, **kwargs):
        self.act_type = 'treatment'
        super().__init__(**kwargs)
        self.generate_activity_boundary_text(default_activity_ends_treatment)            
        if self.tool_use_type == 'average':
            self.tech_description = [
                default_tech_descr_avg,
                self.technology_mix_constructor()
            ]
        else:
            self.tech_description = [
                default_tech_description_specific_0, #See defaults
                default_tech_description_specific_1, #See arguments
                default_tech_description_specific_2, #See arguments,
        ]
        self.generate_comment('technologyComment', self.tech_description)
        self.generalComment = [
            model_description_0,
            model_description_1
            ]
        if self.tool_use_type == 'average':
            self.generalComment.append(model_description_avg)
        self.generate_comment('generalComment', self.generalComment)
        self.generate_comment('timePeriodComment', default_timePeriodComment)
        if self.tool_use_type == 'average':
            if self.location in list_countries_with_specific_data:
                self.generate_comment('geographyComment', default_avg_good_geo_comment)
            else:
                self.generate_comment('geographyComment', default_avg_bad_geo_comment)
        else:
            self.generate_comment('geographyComment', default_spec_geo_comment)
        self.generate_representativeness(
            placeholder_samplingProcedure_text_treat,
            placeholder_extrapolations_text_treat,
            percent=0 #TODO: how to estimate this
            )
        



class DirectDischarge_ecoSold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to untreated fraction""" 
    
    def __init__(self, **kwargs):
        self.act_type = 'untreated discharge'
        super().__init__(**kwargs)
        self.generate_activity_boundary_text(default_activity_ends_no_treatment)            
        self.generate_comment('technologyComment', ["No technology modeled: direct discharge."])
        self.generate_comment('generalComment', ["Based on statistical data about #TODO"])
        self.generate_comment('timePeriodComment', [""])
        self.generate_comment('geographyComment', ["TODO"])
        self.generate_representativeness("", "", 100)
        self.generate_reference_exchange(exc_comment="TODO",
                                        PV=self.PV * self.untreated_fraction,
                                        PV_uncertainty=no_uncertainty,
                                        PV_comment="TODO",
                                        #WW_prop_df, TODO
                                        WW_obligatory_properties=None, #TODO
                                        #overload_loss_fraction_particulate,
                                        #overload_loss_fraction_dissolved,
                                        )
