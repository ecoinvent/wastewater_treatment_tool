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
        for k, v in kwargs.iteritems():
            setattr(self, k, v)        
        assert self.tool_use_type in ('average', 'specific'), "tool_use_type should be average or specific"
        check_for_missing_args(other_args[self.tool_use_type], kwargs)
        self.dataset = self.create_empty_dataset()
        self.MD = load_MD(self.root_dir)
        
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
                'personName': 'Pascal Lesage',
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

    def generate_other_meta(self)
        self.generate_activityNameId()
        self.generate_time_period()
        self.generate_geography()
        self.generate_dataset_id()
        self.generate_activityIndex()
        self.generate_activity_boundary_text(default_activity_ends_treatment)
        self.generate_technology_level(self, technology_level)

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

    def generate_activity_boundary_text(self):
        self.dataset.update({'includedActivitiesStart': default_activity_starts,
                             'includedActivitiesEnd': activity_ends)
                            })        

    def generate_technology_level(self, level_as_string):
        level_string_to_int = {
                'Undefined':0,
                'New':1,
                'Modern':2,
                'Current':3,
                'Old':4,
                'Outdated':5
                }
        self.dataset.update({
                'technologyLevel':level_string_to_int[level_as_string],
                })
            
class WWT_ecoSpold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to WWT dataset""" 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset.update({'activityName': self.create_WWT_activity_name()})       

    def create_WWT_activity_name(self):
        if self.WW_type = "municipal average":
            WW_type_name = ", municipal average"
        else:
            WW_type_name = " {}".format(self.WW_type)
        if self.tool_use_type == "average":
            return "treatment of wastewater{}, average treatment".format()
        else:
            return "treatment of wastewater{}, {}, {}".format(WW_type_name, self.technology, self.capacity)


class DirectDischarge_ecoSold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to untreated fraction""" 
    
    def __init__(self, **kwargs):
        super().__init__(root_dir, **kwargs)
        self.dataset.update({'activityName': self.create_untreated_activity_name()})
        self.generate_other_meta()
                
    def create_untreated_activity_name(self):
        if self.WW_type = "municipal average":
            WW_type_name = ", municipal average"
        else:
            WW_type_name = " {}".format(self.WW_type)
        return "direct discharge of wastewater{}".format(WW_type_name)
        

