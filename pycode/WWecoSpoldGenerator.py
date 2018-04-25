# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
from collections import defaultdict
from .utils import *
from .load_master_data import load_MD
from .defaults import *
from .placeholders import *
from .arguments import *
from .spold_utils import *
#from .direct_emissions import total_untreated_release
from .properties import all_ww_props


class WWecoSpoldGenerator(object):
    """ Class to organize all the data and functions associated with ecoSpold generation.
    
    Is instantiated with data passed from the JavaScript wastewater treatment tool.
    """
    
    def __init__(self, **kwargs):
        check_for_missing_args(always_required_arguments, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)        
        assert self.tool_use_type in ('average', 'specific'), "tool_use_type should be average or specific"
        self.dataset = create_empty_dataset()
        self.MD = load_MD(self.root_dir)
        self.geography = self.MD['Geographies'][self.MD['Geographies']['shortname']==self.geography].index[0]
        self.infra_dict = infra_dict
        self.get_infrastructure_class_mix()

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
        if self.activity_name=='municipal average':
            name = 'wastewater, municipal average'
        else:
            name = 'wastewater, {}'.format(self.activity_name)
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
        if self.activity_name == "municipal average":
            activity_name_name = ", municipal average"
        else:
            activity_name_name = " {}".format(self.activity_name)
        
        if self.act_type == 'untreated discharge':
            return "direct discharge of wastewater{}".format(activity_name_name)
            
        else:
            if self.tool_use_type == "average":
                return "treatment of wastewater{}, average treatment".format(activity_name_name)
            else:
                return "treatment of wastewater{}, {}, {} PE".format(
                    activity_name_name,
                    self.technologies_averaged[0]['technology_level_1'],
                    self.technologies_averaged[0]['capacity'],
                )

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
        try:
            self.dataset.update(
                {
                    'geography': self.geography,
                    'geographyId': self.MD['Geographies'].loc[self.geography, 'id']
                }
            )
        except KeyError:
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

    def get_infrastructure_class_mix(self):
        if self.tool_use_type == 'specific':
            self.infrastructure_mix = {self.technologies_averaged[0]['class']:100}
        else:
            self.infrastructure_mix = defaultdict(float)
            for d in self.technologies_averaged:
                self.infrastructure_mix[d['class']]+=d['fraction']

    def add_sewer_exchanges(self):
        sewer_name_mapping = {
            'wastewater treatment facility, capacity class 1, greater than 100,000 PE': 'sewer grid, 4.7E10l/year, 583 km',
            'wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE': 'sewer grid, 1.1E10l/year, 242 km',
            'wastewater treatment facility, capacity class 3a, between 20,000 and 50,000 PE':'sewer grid, 5E9l/year, 110 km',
            'wastewater treatment facility, capacity class 3b, between 10,000 and 20,000 PE':'sewer grid, 5E9l/year, 110 km',
            'wastewater treatment facility, capacity class 4, between 2,000 and 10,000 PE':'sewer grid, 1E9l/year, 30 km',
            'wastewater treatment facility, capacity class 5, less than 2,000 PE':'sewer grid, 1.6E8l/year, 6 km',
        }

        sewer_amounts = {
            k: self.infra_dict['km_sewer_per_m3'][k] * self.infrastructure_mix[k]
            for k in self.infrastructure_mix.keys()
        }
        for sewer_item in sewer_amounts:
            sewer = create_empty_exchange()
            sewer.update(
                {
                    'group': 'FromTechnosphere',
                    'name': sewer_name_mapping[sewer_item],
                    'unitName': 'km',
                    'amount': sewer_amounts[sewer_item],
                    'comment': "Rough estimate based on Swiss data for sewer length per person equivalent. " \
                               "The length per person equivalent is given per WWTP capacity class." \
                               "This value is converted to m3 transported using capacity and treated volume amounts from " \
                               "sample Spanish wastewater treatment plants. The same relations are assumed to " \
                               "hold whether the water sent to the sewer is ultimately discharged to the environment "\
                               "or treated."
                }
            )
            self.append_exchange(sewer, [], default_sewer_uncertainty)

    def add_WWTP_exchanges(self):
        infrastructure_amounts = {
            k: 1 / self.infra_dict['m3_over_life_WWTP'][k]
            for k in self.infrastructure_mix.keys()
        }
        for wwtp in infrastructure_amounts.keys():
            infra = create_empty_exchange()
            infra.update(
                {
                    'group': 'FromTechnosphere',
                    'name': self.infra_dict['new_name_exc'][wwtp],
                    'unitName': 'km',
                    'amount': infrastructure_amounts[wwtp],
                    'comment': "Rough estimate based on Spanish data for one WWTP of this class." \
                               "The expected lifetime is 30 years." \
                               "The conversion from PE to m3 treated is based on observed values " \
                               "({} m3/year / PE).".format(self.infra_dict['sample_m3_per_year_WWTP'][wwtp] \
                                                             / self.infra_dict['sample_cap_WWTP'][wwtp])
                }
            )
            self.append_exchange(infra, [], default_infrastructure_uncertainty)

    def add_DOC_TOC_exchanges(self, COD, VSS):
        TOC = COD / self.COD_TOC_ratio['value']
        DOC = TOC - VSS * 0.5
        TOC_id = 'f65558fb-61a1-4e48-b4f2-60d62f14b085'
        DOC_id = '960c0f37-f34c-4fc1-b77c-22d8b35fd8d5'
        TOC_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == TOC_id]
        DOC_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == DOC_id]
        TOC_ef = create_empty_exchange()
        TOC_ef.update(
            {
                'group': 'ToEnvironment',
                'name': TOC_sel.index[0][0],
                'compartment': TOC_sel.index[0][1],
                'subcompartment': TOC_sel.index[0][2],
                'unitName': 'kg',
                'amount': TOC,
                'comment': "estimated from the COD to TOC_ratio ({}).".format(
                    COD_TOC_ratio
                )
            }
        )
        DOC_ef = create_empty_exchange()
        DOC_ef.update(
            {
                'group': 'ToEnvironment',
                'name': DOC_sel.index[0][0],
                'compartment': DOC_sel.index[0][1],
                'subcompartment': DOC_sel.index[0][2],
                'unitName': 'kg',
                'amount': DOC,
                'comment': "DOC is calculated as Total Organic Carbon (TOC) - Particulate Organics (PO). " \
                           "DOC is estimated from the COD to TOC_ratio ({}). " \
                           "PO is estimated using a C to Volatile Suspended Solids (VSS) ratio of 0.5 gC/gVSS. " \
                           "VSS is estimated as {}.".format(self.COD_TOC_ratio, VSS)
            }
        )
        DOC_TOC_incertainty = {
            'variance': 0.04,
            'pedigreeMatrix': [4, 5, 5, 5, 5],
            'comment': "Uncertainty associated with the COD to TOC ratio, VSS amount and COD amount."
        }
        self.append_exchange(TOC_ef, [], DOC_TOC_incertainty)
        self.append_exchange(DOC_ef, [], DOC_TOC_incertainty)
        return None

    def add_sludge(self):
        pass
        """
        settlers = []
        if self.sludge_composition['PRIMARY']['AMOUNT'] != 0:
            settles.append('primary')
        if self.sludge_composition['SECONDARY']['AMOUNT'] != 0:
            settles.append('secondary')
        if self.sludge_composition['TERTIARY']['AMOUNT'] != 0:
            settles.append('tertiary')

        total_sludge = 100 #todo

        sludge_comment = ""
        if "primary" in settlers:
            pass
        if "secondary" in settlers:
            pass
        if "tertiary" in settlers:
            pass

        if self.activity_name == "municipal average":
            sludge_name = "sludge, from the treatment of average municipal wastewater"
        else:
            sludge_name = "sludge, from the treatment of wastewater from {}".format(self.activity_name)

        sludge = create_empty_exchange()
        sludge.update(
            {
                'group': 'ByProduct',
                'name': sludge_name,
                'unitName': 'kg',
                'amount': self.sludge_amount/(1-temp_sludge_water_content),
                'comment': sludge_comment
            }
        )
        sludge_properties = get_sludge_properties(self.sludge_properties)
        self.append_exchange(sludge, sludge_properties, sludge_uncertainty)
        pass
    """

    def total_untreated_release(self):
        """ Sum direct discharge and CSO. WIll fail if untreated_fraction == 0!

        Because of this problem, CSO emissions should ideally be placed in another dataset (market, treatment DS)"""

        ef_ignores = [
            'TKN_discharged_kgd', #CSO
            'TP_discharged_kgd', #CSO
            'TKN',#"untreated_as_emissions"
            'TP', #"untreated_as_emissions"
        ]

        efs = []
        for direct_discharge in self.untreated_as_emissions:
            tool_id, ef_id = direct_discharge['id'], direct_discharge['ecoinvent_id']
            if tool_id in ef_ignores:
                pass
            else:
                if self.CSO_particulate['value'] + self.CSO_soluble['value'] == 0:
                    CSO_amount = 0
                else:
                    CSO_amount = [cso_amount['value'] for cso_amount in self.CSO_amounts if cso_amount['ecoinvent_id']==ef_id][0]
                scaled_CSO_amount = CSO_amount*(1-self.untreated_fraction)/(self.untreated_fraction)
                total_emission = scaled_CSO_amount + direct_discharge['value']
                fraction_CSO = scaled_CSO_amount/total_emission
                if tool_id == 'NH4':
                    total_emission = total_emission * 18 / 14
                if tool_id == 'PO4':
                    total_emission = total_emission * (31 + 4 * 16) / 31
                sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id']==ef_id]
                ef = create_empty_exchange()
                ef.update(
                    {
                        'group': 'ToEnvironment',
                        'name': sel.index[0][0],
                        'compartment': sel.index[0][1],
                        'subcompartment': sel.index[0][2],
                        'unitName': 'kg',
                        'amount': total_emission,
                    }
                )
                if fraction_CSO != 0:
                    ef.update(
                        {
                            'comment': "Based on direct release to environment of wastewater " \
                                     "discharged to sewers not connected to wastewater treatment plants ({:.4}%) " \
                                     "and compounds lost due to combined sewer overflow ({:.4}%)".format(
                                (1 - fraction_CSO)*100, fraction_CSO*100
                            )
                        }
                    )
                else:
                    ef.update(
                        {
                            'comment': "Based on direct release to environment of wastewater " \
                                     "discharged to sewers not connected to wastewater treatment plants"
                        }
                    )
                uncertainty = self.direct_emission_uncertainty(
                    ef_id, direct_discharge['value'], scaled_CSO_amount, basic_pollutants)
                efs.append([ef, [], uncertainty])
        COD_EF = [ef[0]['amount'] for ef in efs if ef[0]['name']=='COD, Chemical Oxygen Demand']
        if len(COD_EF)>0:
            COD_EF = COD_EF[0]
            COD_influent = [d['value'] for d in self.WW_properties if d['id']=='COD'][0]
            VSS_influent = [d['value'] for d in self.WW_properties if d['id']=='VSS'][0]
            VSS_EF = VSS_influent/COD_influent * COD_EF
            TOC = COD_EF / self.COD_TOC_ratio['value']
            DOC = TOC - VSS_EF * 0.5
            TOC_id = 'f65558fb-61a1-4e48-b4f2-60d62f14b085'
            DOC_id = '960c0f37-f34c-4fc1-b77c-22d8b35fd8d5'
            TOC_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == TOC_id]
            DOC_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == DOC_id]
            TOC_ef = create_empty_exchange()
            TOC_ef.update(
                {
                    'group': 'ToEnvironment',
                    'name': TOC_sel.index[0][0],
                    'compartment': TOC_sel.index[0][1],
                    'subcompartment': TOC_sel.index[0][2],
                    'unitName': 'kg',
                    'amount': TOC,
                    'comment': "estimated from the COD to TOC_ratio ({}).".format(
                        self.COD_TOC_ratio
                    )
                }
            )
            DOC_ef = create_empty_exchange()
            DOC_ef.update(
                {
                    'group': 'ToEnvironment',
                    'name': DOC_sel.index[0][0],
                    'compartment': DOC_sel.index[0][1],
                    'subcompartment': DOC_sel.index[0][2],
                    'unitName': 'kg',
                    'amount': DOC,
                    'comment': "DOC is calculated as Total Organic Carbon (TOC) - Particulate Organics (PO). " \
                               "DOC is estimated from the COD to TOC_ratio ({}). " \
                               "PO is estimated using a C to Volatile Suspended Solids (VSS) ratio of 0.5 gC/gVSS. " \
                               "VSS is estimated from VSS/DOC ratio in raw effluent {}.".format(
                        self.COD_TOC_ratio, VSS_influent/COD_influent)
                }
            )
            DOC_TOC_incertainty = {
                'variance': 0.04,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'comment': "Uncertainty associated with the COD to TOC ratio, VSS amount and COD amount."
            }
            self.append_exchange(TOC_ef, [], DOC_TOC_incertainty)
            self.append_exchange(DOC_ef, [], DOC_TOC_incertainty)
        return efs

    def direct_emission_uncertainty(self, pollutant_name,
                                    untreated_release,
                                    scaled_CSO_amounts,
                                    basic_pollutant_list):
        """Uncertainty depends on whether direct discharge or CSO is dominant"""
        if untreated_release < scaled_CSO_amounts:  # Mostly CSO
            if pollutant_name in basic_pollutant_list:
                return {
                    'variance': 0.04,
                    'pedigreeMatrix': [5, 5, 4, 5, 1],
                    'comment': "Uncertainty represents that of the wastewater composition, " \
                               "and the pedigree scores are for the releases due to combined sewer overflow, " \
                               "which represent a greater share of emissions ({:.4}% of amount).".format(
                        100*scaled_CSO_amounts / (scaled_CSO_amounts+ untreated_release)
                    )
                }
            else:
                return {
                    'variance': 0.65,
                    'pedigreeMatrix': [5, 5, 4, 5, 1],
                    'comment': "Uncertainty represents that of the wastewater composition, " \
                               "and the pedigree scores are for the releases due to combined sewer overflow, " \
                               "which represent a greater share of emissions ({:.4}% of total amount).".format(
                        100*scaled_CSO_amounts / (scaled_CSO_amounts+ untreated_release)
                    )
                }
        else:  # Mostly direct discharge
            if pollutant_name in basic_pollutant_list:
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
    def add_1m3_water(self):
        sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == 'db4566b1-bd88-427d-92da-2d25879063b9']
        ef = create_empty_exchange()
        ef.update(
            {
                'group': 'ToEnvironment',
                'name': sel.index[0][0],
                'compartment': sel.index[0][1],
                'subcompartment': sel.index[0][2],
                'unitName': 'm3',
                'amount': 1,
            }
        )
        self.append_exchange(ef, [], no_uncertainty)

    def add_WWTP_water_emissions(self):
        for WWTP_ef in self.WWTP_emissions_water:
            if WWTP_ef['id'] == "NOx_effluent_water":
                ecoinvent_id = "13331e67-6006-48c4-bdb4-340c12010036"
            else:
                ecoinvent_id = WWTP_ef['ecoinvent_id']
            if 'ecoinvent_id' is not None:
                if WWTP_ef['id'] == "COD_effluent_water":
                    COD_EF= WWTP_ef['value']
                sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == ecoinvent_id]
                ef = create_empty_exchange()
                ef.update(
                    {
                        'group': 'ToEnvironment',
                        'name': sel.index[0][0],
                        'compartment': sel.index[0][1],
                        'subcompartment': sel.index[0][2],
                        'unitName': 'kg',
                        'amount': WWTP_ef['value'],
                    }
                )
                stripped_id = WWTP_ef['id'][0:-15]
                if stripped_id in metals:
                    uncertainty = {
                        'variance': 0.65,
                        'pedigreeMatrix': [3, 5, 1, 5, 4],
                        'comment': "Default basic uncertainty for metals to water."
                    }
                elif stripped_id in non_metals:
                    uncertainty = {
                        'variance': 0.04,
                        'pedigreeMatrix': [3, 5, 1, 5, 4],
                        'comment': "Default basic uncertainty for emissions to water."
                    }
                else:
                    print("No uncertainty for {}".format(WWTP_ef['id']))
                    uncertainty = no_uncertainty
                self.append_exchange(ef, [], uncertainty)
        COD_influent = [d['value'] for d in self.WW_properties if d['id']=='COD'][0]
        VSS_influent = [d['value'] for d in self.WW_properties if d['id']=='VSS'][0]
        BOD_influent = [d['value'] for d in self.WW_properties if d['id'] == 'BOD'][0]
        VSS_EF = VSS_influent/COD_influent * COD_EF
        BOD_EF = BOD_influent/COD_influent * COD_EF
        TOC = COD_EF / self.COD_TOC_ratio['value']
        DOC = TOC - VSS_EF * 0.5
        TOC_id = 'f65558fb-61a1-4e48-b4f2-60d62f14b085'
        DOC_id = '960c0f37-f34c-4fc1-b77c-22d8b35fd8d5'
        BOD_id = '70d467b6-115e-43c5-add2-441de9411348'
        TOC_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == TOC_id]
        DOC_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == DOC_id]
        BOD_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == BOD_id]
        TOC_ef = create_empty_exchange()
        TOC_ef.update(
            {
                'group': 'ToEnvironment',
                'name': TOC_sel.index[0][0],
                'compartment': TOC_sel.index[0][1],
                'subcompartment': TOC_sel.index[0][2],
                'unitName': 'kg',
                'amount': TOC,
                'comment': "estimated from the COD to TOC_ratio ({}).".format(
                    self.COD_TOC_ratio
                )
            }
        )
        DOC_ef = create_empty_exchange()
        DOC_ef.update(
            {
                'group': 'ToEnvironment',
                'name': DOC_sel.index[0][0],
                'compartment': DOC_sel.index[0][1],
                'subcompartment': DOC_sel.index[0][2],
                'unitName': 'kg',
                'amount': DOC,
                'comment': "DOC is calculated as Total Organic Carbon (TOC) - Particulate Organics (PO). " \
                           "DOC is estimated from the COD to TOC_ratio ({}). " \
                           "PO is estimated using a C to Volatile Suspended Solids (VSS) ratio of 0.5 gC/gVSS. " \
                           "VSS is estimated from VSS/DOC ratio in raw effluent {}.".format(
                    self.COD_TOC_ratio, VSS_influent/COD_influent)
            }
        )
        BOD_ef = create_empty_exchange()
        BOD_ef.update(
            {
                'group': 'ToEnvironment',
                'name': BOD_sel.index[0][0],
                'compartment': BOD_sel.index[0][1],
                'subcompartment': BOD_sel.index[0][2],
                'unitName': 'kg',
                'amount': BOD_EF,
                'comment': "Crude assumption based on ratio of COD/BOD in raw wastewater "\
                "and the amount of COD in effluent."
            }
        )
        DOC_TOC_incertainty = {
            'variance': 0.04,
            'pedigreeMatrix': [4, 5, 5, 5, 5],
            'comment': "Uncertainty associated with the COD to TOC ratio, VSS amount and COD amount."
        }
        self.append_exchange(TOC_ef, [], DOC_TOC_incertainty)
        self.append_exchange(DOC_ef, [], DOC_TOC_incertainty)
        self.append_exchange(BOD_ef, [], no_uncertainty)

    def WWTP_air_emissions(self):
        try:
            N2O_dict = [ef for ef in self.WWTP_emissions_air if ef['id']=="N2O_effluent_air"][0]
            N2O = create_empty_exchange()
            N2O_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == N2O_dict['ecoinvent_id']]
            N2O.update(
                {
                    'group': 'ToEnvironment',
                    'name': N2O_sel.index[0][0],
                    'compartment': N2O_sel.index[0][1],
                    'subcompartment': N2O_sel.index[0][2],
                    'unitName': 'kg',
                    'amount': N2O_dict['value'],
                    'comment': ""
                }
            )
            N2O_uncertainty = {
                'variance': 0.12,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'comment': ""
            }
            self.append_exchange(N2O, [], N2O_uncertainty)
        except: #No such flux
            pass

        try:
            CO2_dict = [ef for ef in self.WWTP_emissions_air if ef['id']=='CO2_effluent_air'][0]
            CO2_fossil_amount = CO2_dict['value'] * self.fraction_C_fossil['value']
            CO2_non_fossil_amount = CO2_dict['value'] * (1-self.fraction_C_fossil['value'])
            CO2_fossil_id = 'f9749677-9c9f-4678-ab55-c607dfdc2cb9'
            CO2_non_fossil_id = '73ed05cc-9727-4abf-9516-4b5c0fe54a16'
            CO2_fossil = create_empty_exchange()
            CO2_fossil_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == CO2_fossil_id]
            CO2_fossil.update(
                {
                    'group': 'ToEnvironment',
                    'name': CO2_fossil_sel.index[0][0],
                    'compartment': CO2_fossil_sel.index[0][1],
                    'subcompartment': CO2_fossil_sel.index[0][2],
                    'unitName': 'kg',
                    'amount': CO2_fossil_amount,
                    'comment': ""
                }
            )
            CO2_uncertainty = {
                'variance': 0.0006,
                'pedigreeMatrix': [4, 5, 5, 5, 5],
                'comment': ""
            }
            self.append_exchange(CO2_fossil, [], CO2_uncertainty)
            CO2_non_fossil = create_empty_exchange()
            CO2_non_fossil_sel = self.MD['ElementaryExchanges'][self.MD['ElementaryExchanges']['id'] == CO2_non_fossil_id]
            CO2_non_fossil.update(
                {
                    'group': 'ToEnvironment',
                    'name': CO2_non_fossil_sel.index[0][0],
                    'compartment': CO2_non_fossil_sel.index[0][1],
                    'subcompartment': CO2_non_fossil_sel.index[0][2],
                    'unitName': 'kg',
                    'amount': CO2_non_fossil_amount,
                    'comment': ""
                }
            )
            self.append_exchange(CO2_non_fossil, [], CO2_uncertainty)
        except:
            pass


class WWT_ecoSpold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to WWT dataset""" 
    def __init__(self, root_dir, **kwargs):
        self.root_dir = root_dir
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
                technology_mix_constructor(self.technologies_averaged)
            ]
        else:
            self.tech_description = [
                default_tech_description_specific.format(
                    self.technologies_averaged[0]['technology_level_1'],
                    decode_tech_bitstring(self.technologies_averaged[0]['technology_level_2']),
                    "Capacity: {} PE".format(self.technologies_averaged[0]['capacity']),
                    self.technologies_averaged[0]['class'],
                ),
        ]
        self.generate_comment('technologyComment', self.tech_description)

        # Treatment general comment
        if self.activity_name == 'municipal average':
            if self.tool_use_type == 'average':
                self.general_treat_comment = [
                    treat_common_general_product,
                    treat_general_comment_avg_municipal.format(
                        len(self.technologies_averaged),
                    ),
                    treat_general_comment_final_note.format(
                        self.URL,
                    )
                ]
            else:
                self.general_treat_comment = [
                    treat_common_general_product,
                    treat_general_comment_specific_municipal,
                    treat_general_comment_final_note.format(
                        self.URL,
                    )
                ]
        else:
            if self.tool_use_type == 'average':
                self.general_treat_comment = [
                    treat_common_general_product,
                    treat_general_comment_avg_not_municipal.format(
                        self.activity_name,
                        len(self.technologies_averaged)
                    ),
                    treat_general_comment_final_note.format(
                        self.url,
                    ),
                ]
            else:
                self.general_treat_comment = [
                    treat_common_general_product,
                    treat_general_comment_specific_not_municipal.format(
                        self.activity_name,
                    ),
                    treat_general_comment_final_note.format(
                        self.url,
                    )
                ]

        self.generate_comment('generalComment', self.general_treat_comment)
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
            default_extrapolations_text_treat_avg(self.technologies_averaged),
            percent=0
            )
        ref_exc_dict = {
            'data': {'comment': ref_exchange_comment_treat, },
            'PV': {
                'amount': self.PV['value'] * (1 - self.untreated_fraction),
                'uncertainty': default_PV_uncertainty_treat,
                'comment': generate_default_PV_comment_treated(self.PV,
                                                               self.untreated_fraction
                                                               ),
            },
            'properties': all_ww_props(self.WWTP_influent_properties,
                                       self.COD_TOC_ratio,
                                       self.fraction_C_fossil,
                                       self.MD
                                       )
            }
        self.generate_reference_exchange(ref_exc_dict)

        # Electricity demand
        if hasattr(self, 'electricity') and self.electricity != 0:
            electricity = create_empty_exchange()
            electricity.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'electricity, low voltage',
                    'unitName': 'kWh',
                    'amount': self.electricity['value'],
                    'comment': default_electricity_comment,
                }
            )
            self.append_exchange(electricity, [], default_electricity_uncertainty)

        if 'FeCl3' in self.chemicals and self.chemicals['FeCl3'] != 0:
            FeCl3 = create_empty_exchange()
            FeCl3.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'iron (III) chloride',
                    'unitName': 'kg',
                    'amount': self.chemicals['FeCl3']['value'],
                    'comment': "Used for chemical precipitation of P",
                }
            )
            self.append_exchange(FeCl3, [], default_FeCl3_uncertainty)

        if 'acrylamide' in self.chemicals and self.chemicals['acrylamide'] != 0:
            acrylamide = create_empty_exchange()
            acrylamide.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'polyacrylamide',
                    'unitName': 'kg',
                    'amount': self.chemicals['acrylamide']['value'],
                    'comment': "Polyelectrolyte for thickening",
                }
            )
            self.append_exchange(acrylamide, [], default_acrylamide_uncertainty)

        if 'NaHCO3' in self.chemicals and self.chemicals['NaHCO3']['value']!=0:
            NaHCO3 = create_empty_exchange()
            NaHCO3.update(
                {
                    'group': 'FromTechnosphere',
                    'name': 'sodium bicarbonate',
                    'unitName': 'kg',
                    'amount': self.chemicals['NaHCO3']['value'],
                    'comment': "Used to maintain alkalinity for nitrification."\
                        "Calculated based on alkalinity consumed during nitrification, and"\
                        "an assumed residual alkalinity requirement (70 g CaCO3/m3).",
                }
            )
            self.append_exchange(NaHCO3, [], default_acrylamide_uncertainty)

        self.add_sewer_exchanges()
        self.add_WWTP_exchanges()
        self.add_sludge()
        self.add_1m3_water()
        self.add_WWTP_water_emissions()
        self.WWTP_air_emissions()

        # TODO Add grit

class DirectDischarge_ecoSpold(WWecoSpoldGenerator):
    """WWecoSpoldGenerator specific to untreated fraction"""

    def __init__(self, root_dir, **kwargs):
        self.root_dir = root_dir
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
        self.generate_comment(
            'generalComment',
            (
                    default_general_comment_untreated_0 +  sewer_estimation_text(self.tool_use_type)
            )
        )
        self.generate_comment('timePeriodComment', default_time_period_comment_untreated)
        self.generate_comment('geographyComment', default_geography_comment_untreated)
        if not hasattr(self, 'used_WHO_region'):
            xls = os.path.join(self.root_dir, 'resources', 'untreated_fraction.xlsx')
            direct_discharge_df = pd.read_excel(xls, sheet_name="ecoinvent", header=0, index_col=0)
            self.used_WHO_region = direct_discharge_df.loc[self.geography, 'used_WHO_region']
        self.generate_representativeness(
            default_representativeness_untreated_1,
            default_representativeness_untreated_2(self.used_WHO_region),
            100,
        )
        ref_exc_dict = {
            'data': {'comment': ref_exchange_comment_untreated,},
            'PV':{
              'amount': self.PV['value'] * self.untreated_fraction,
              'uncertainty': default_PV_uncertainty_untreated,
              'comment': generate_default_PV_comment_untreated(self.PV, self.untreated_fraction),
                },
            'properties': all_ww_props(self.WW_properties, self.COD_TOC_ratio, self.fraction_C_fossil, self.MD),
            }

        self.generate_reference_exchange(ref_exc_dict)
        total_untreated_release_data = self.total_untreated_release()

        for ef in total_untreated_release_data:
            self.append_exchange(ef[0], ef[1], ef[2])
        self.add_1m3_water()
        self.add_sewer_exchanges()

