# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
from .utils import *
from .load_master_data import load_MD
from .defaults import *
from .placeholders import *
from .arguments import *
from .spold_utils import *


class WWecoSpoldGenerator(object):
    """ Class to organize all the data and functions associated with ecoSpold generation.
    
    Is instantiated with data passed from the JavaScript wastewater treatment tool.
    """
    
    #def __init__(self, root_dir, untreated_fraction, overload_loss_fraction_particulate,
    #             overload_loss_fraction_dissolved, WW_type, technology, capacity):
    def __init__(self, **kwargs):
        #os.chdir(r'..')
        #self.root_dir = os.getcwd()
        check_for_missing_args(always_required_arguments, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)        
        assert self.tool_use_type in ('average', 'specific'), "tool_use_type should be average or specific"
        check_for_missing_args(specific_required_args[self.tool_use_type], kwargs)
        self.dataset = create_empty_dataset()
        self.MD = load_MD(self.root_dir)

    def generate_ecoSpold2(self, name=None):
        self.dataset['has_userMD'] = False
        for field in ['ActivityNames', 'Sources', 'activityIndexEntry', 'Persons', 'IntermediateExchanges']:
            if field in self.dataset and len(self.dataset[field]) > 0:
                self.dataset['has_userMD'] = True
                break
        self.dataset['exchanges'] = []
        for group in [
            'ReferenceProduct',
            'ByProduct',
            'FromTechnosphere',
            'FromEnvironment',
            'ToEnvironment'
        ]:
        #groups need to appear in a specific order
            self.dataset['exchanges'].extend(self.dataset[group])

        dataset = GenericObject(self.dataset, 'Dataset')
        #loading the template environment
        template_path = os.path.join(self.root_dir, 'templates')
        env = Environment(loader=FileSystemLoader(template_path), 
                          keep_trailing_newline = True, 
                          lstrip_blocks = True, 
                          trim_blocks = True)
        if name is None:
            name = "{}.spold".format(self.dataset['id'])
        rendered = recursive_rendering(dataset, env, os.path.join(self.root_dir, 'output'), name)
        return (os.path.join(self.root_dir, 'output'), name)

    def append_exchange(self, exc, properties, uncertainty,
                        PV_uncertainty = None #Relevant for exchanges with production volumes only
                        ):
        """
        Exc: All exchanges are passed as dictionaries.
             
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
            present_properties = [p['name'] for p in properties]
            for i, p in property_sel.iterrows():
                if p['propertyName'] not in present_properties:
                    properties.append(
                        {
                            'name':p['propertyName'],
                            'amount':p['amount'],
                            'unit': p['unitName'],
                            'comment': "Default value. {}".format(p['comment']),
                            'uncertainty': None
                        }
                            )
        exc = self.add_property(exc, properties)
        if uncertainty is not None:
            exc = add_uncertainty(exc, uncertainty)
        if PV_uncertainty:
            exc = add_uncertainty(exc, PV_uncertainty, PV = True)
        self.dataset[exc['group']].append(GenericObject(exc, 'Exchange'))
        return None

    def add_property(self, exc, properties):
        # properties is a list of property_dicts
        exc['properties'] = []
        #for property_name, amount, unit, comment, unc in properties:
        for prop_dict in properties:            
            p = create_empty_property()
            p['name'] = prop_dict['name']
            if p['name'] in self.MD['Properties'].index:
                sel = self.MD['Properties'].loc[p['name']]
                p['propertyId'] = sel['id']
                if not is_empty(sel['unitName']):
                    assert prop_dict['unit'] == sel['unitName'], "{}, {}, {}".format(prop_dict['name'], prop_dict['unit'], sel['unitName'])
                    p['unitName'] = prop_dict['unit']
                    p['unitId'] = self.MD['Units'].loc[p['unitName'], 'id']
            else:
                p['propertyId'] = make_uuid(prop_dict['name'])
                p['unitName'] = prop_dict['unit']
                p['unitId'] = self.MD['Units'].loc[p['unitName'], 'id']
                self.dataset['Properties'].append(GenericObject(p,
                                            'user_MD_Properties'
                                            ))
            p['amount'] = prop_dict['amount']
            p['comment'] = prop_dict['comment']
            if 'uncertainty' in prop_dict and prop_dict['uncertainty'] is not None:
                p = add_uncertainty(p, prop_dict['uncertainty'])
            exc['properties'].append(GenericObject(p, 'TProperty'))
        return exc

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

    def generate_reference_exchange(self, ref_exc_dict):
        exc = create_empty_exchange()
        if self.WW_type=='municipal average':
            name = 'wastewater, municipal average'
        else:
            name = 'wastewater, {}'.format(self.WW_type)
        exc.update({
                'group': 'ReferenceProduct',
                'unitName': 'm3',
                'amount': -1.,
                'productionVolumeAmount': ref_exc_dict['PV']['amount'],
                'productionVolumeComment': ref_exc_dict['PV']['comment'], 
                'comment': ref_exc_dict['data']['comment'], 
                'name': name,
               })
        # Append exchange to dataset
        self.append_exchange(
            exc,
            properties=ref_exc_dict['properties'],
            uncertainty = None,
            PV_uncertainty = ref_exc_dict['PV']['uncertainty']
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

    def generate_time_period(self, timePeriodStart, timePeriodEnd):
        self.timePeriodStart = timePeriodStart
        self.timePeriodEnd = timePeriodEnd
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

    def technology_mix_constructor(self):  #TODO --> Get from Lluis B.
        tech_mix = ""
        for k, v in self.technologies_averaged.items():

            tech_mix += "{:.0f}%: {}, {}, {}".format(
                v['fraction'],
                v['technology_str'],
                v['capacity'],
                v['location']
            )
        return tech_mix

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
        self.dataset['activityName']=self.generate_activity_name()
        self.generate_activityNameId()
        self.generate_time_period(default_timePeriodStarts_treated, default_timePeriodEnds_treated)
        self.generate_geography()
        self.generate_dataset_id()
        self.generate_activityIndex()
        self.generate_technology_level()
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
        self.generate_comment('timePeriodComment', default_timePeriodComment_treatment)
        if self.tool_use_type == 'average':
            if self.geography in list_countries_with_specific_data:
                self.generate_comment('geographyComment', default_avg_good_geo_comment)
            else:
                self.generate_comment('geographyComment', default_avg_bad_geo_comment)
        else:
            self.generate_comment('geographyComment', default_spec_geo_comment)
        self.generate_representativeness(
            default_samplingProcedure_text_treat,
            default_extrapolations_text_treat,
            percent=0
            ) #TODO representativeness for treatment
        ref_exc_dict = {
            'data': {'comment': ref_exchange_comment_treat,},
            'PV':{
              'amount': self.PV * (1-self.untreated_fraction),
              'uncertainty': default_PV_uncertainty_treat,
              'comment': generate_default_PV_comment_treated(self.PV, self.untreated_fraction),
                },
            'properties': generate_WW_properties(self.MD, self.WWTP_influent_properties),
            }
        self.generate_reference_exchange(ref_exc_dict)
        technosphere_inputs = []
        # Electricity demand
        electricity = create_empty_exchange()
        electricity.update(
            {
                'group': 'FromTechnosphere',
                'name': 'electricity, low voltage',
                'unitName': 'kWh',
                'amount': self.electricity,
                'comment': default_electricity_comment,
            }
        )
        self.append_exchange(electricity, [], default_electricity_uncertainty)

        # FeCl3
        if hasattr(self, 'FeCl3') and self.FeCl3 != 0:
            FeCl3 = create_empty_exchange()
            FeCl3.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'iron (III) chloride',
                    'unitName': 'kg',
                    'amount': self.FeCl3,
                    'comment': "Used for chemical removal of P",
                }
            )
            self.append_exchange(FeCl3, [], default_FeCl3_uncertainty)

        if hasattr(self, 'acrylamide') and self.acrylamide != 0:
            acrylamide = create_empty_exchange()
            acrylamide.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'polyacrylamide',
                    'unitName': 'kg',
                    'amount': self.acrylamide,
                    'comment': "Used for sludge dewatering",
                }
            )
        self.append_exchange(acrylamide, [], default_acrylamide_uncertainty)

        if hasattr(self, 'NaHCO3') and self.NaHCO3 != 0:
            NaHCO3 = create_empty_exchange()
            NaHCO3.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'sodium bicarbonate',
                    'unitName': 'kg',
                    'amount': self.NaHCO3,
                    'comment': "Used to maintain alkalinity",
                }
            )
        self.append_exchange(NaHCO3, [], default_NaHCO3_uncertainty)

class DirectDischarge_ecoSpold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to untreated fraction"""

    def __init__(self, **kwargs):
        self.act_type = 'untreated discharge'
        super().__init__(**kwargs)
        self.dataset['activityName']=self.generate_activity_name()
        self.generate_activityNameId()
        self.generate_time_period(default_timePeriodStarts_untreated, default_timePeriodEnds_untreated)
        self.generate_geography()
        self.generate_dataset_id()
        self.generate_activityIndex()
        self.generate_technology_level()
        self.generate_activity_boundary_text(default_activity_ends_untreated)
        self.generate_comment('technologyComment', default_technology_comment_untreated)
        self.generate_comment('generalComment', default_general_comment_untreated )
        self.generate_comment('timePeriodComment', default_time_period_comment_untreated)
        self.generate_comment('geographyComment', ["TODO"])
        self.generate_representativeness(default_representativeness_untreated_1, default_representativeness_untreated_2, 100)
        ref_exc_dict = {
            'data': {'comment': ref_exchange_comment_untreated,},
            'PV':{
              'amount': self.PV * self.untreated_fraction,
              'uncertainty': default_PV_uncertainty_untreated,
              'comment': generate_default_PV_comment_untreated(self.PV, self.untreated_fraction),
                },
            'properties': generate_WW_properties(self.MD, self.WW_properties),
            }

        self.generate_reference_exchange(ref_exc_dict)
        #self.generate_ecoSpold2()
        
