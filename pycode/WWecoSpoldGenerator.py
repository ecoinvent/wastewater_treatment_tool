# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import uuid
import numpy as np
import pandas as pd
from lxml import objectify
from copy import copy
from pickle import dump, load
from .utils import pkl_dump, make_uuid, check_for_missing_args
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
