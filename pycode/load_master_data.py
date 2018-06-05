import os
import pandas as pd
from lxml import objectify
from copy import copy
from .utils import *


def load_MD(root_dir, make_excel=False):
    '''Load pickled master data dictionary MD.
    
    Dictionary `MD` keys=names of the master data files and
    values=pandas dataframes with all elements and attributes.'''
    
    MD_pkl_dir = os.path.join(root_dir, 'MasterData')
    update_MD_if_needed(root_dir, make_excel)
    return pkl_load(MD_pkl_dir, 'MD')
    
def update_MD_if_needed(root_dir, make_excel):
    '''Generate a dictionary `MD` with keys=names of the master data files and
       values=pandas dataframes with all elements and attributes
       Will only generate `MD` if such a dictionary does not already exist
       or if the existing MD is older than any of the Master data files.
    '''       
    MD_pkl_dir = os.path.join(root_dir, 'MasterData')
    MD_xml_dir = os.path.join(root_dir, 'MasterData', 'XML')
    MD_fields_xls = os.path.join(root_dir, 'MasterData', 'xlsx', 'MasterData_fields.xlsx')
    MD_xls_dump_dir=os.path.join(root_dir, 'MasterData', 'xlsx')

    # Find the age of the youngest current MD file
    filelist = build_file_list(MD_xml_dir,
                               extension = 'xml',
                               add_path = True)
    youngest, t_MD = find_youngest(filelist)
    
    existing_MD = os.path.join(MD_pkl_dir, 'MD.pkl')
    if not os.path.isfile(existing_MD):
        update = True
    else:
        t_pkl = os.path.getmtime(existing_MD)
        update = t_MD > t_pkl
    if update:
        assert MD_fields_xls, "MD.pkl file outdated, pass argument MD_fields_xls to regenerate"
        print("Master data pkl being updated")
        if make_excel:
            MD_xls_dump_dir = MD_xls_dump_dir
        else:
            MD_xls_dump_dir = None
        MD = build_MD(MD_xml_dir,
                      MD_fields_xls,
                      pickle_dump_dir=MD_pkl_dir,
                      MD_xls_dump_dir=MD_xls_dump_dir,
                      )
    return None


def build_MD(MD_xml_dir, MD_fields_xls, pickle_dump_dir, MD_xls_dump_dir=None):
    """Generate a new pickled master data dictionary.
    
    Used when Master Data is updated. Args:
    **MD_xml_dir**: path to directory with new master data (set of xlm files)
    **MD_fields_xls**: path to MasterData_fields.xlsx
    **pickle_dump_dir**: path to dir where pickled master data dict will be dumped
    **MD_xls_dump_dir**: path to dir where xls version of master data is dumped.
    """
    tag_prefix = '{http://www.EcoInvent.org/EcoSpold02}'
    MD = {}
    validate_master_data_dir(MD_xml_dir)
    
    def store_fields(fields, child, to_add = {}):
        for field_type, field in fields:
            if field_type == 'attribute':
                to_add[field] = child.get(field)
            else:
                if hasattr(child, field):
                    to_add[field] = getattr(child, field).text
                else:
                    to_add[field] = ''
        return to_add    
    
    MD_fields = pd.read_excel(MD_fields_xls, 'fields')
    MD_tags = pd.read_excel(MD_fields_xls, 'tags').set_index('file')
    properties = {}
    for filename, group in MD_fields.groupby('file'):
        if 'Exchange' in filename:
            properties[filename] = []
        df = []
        with open(os.path.join(MD_xml_dir, '{}.xml'.format(filename)), encoding = 'utf8') as f:
            root = objectify.parse(f).getroot()
        fields = list(zip(list(group['field type']), list(group['field name'])))
        if filename == 'Classifications':
            for child in root.iterchildren(tag = tag_prefix + MD_tags.loc[filename, 'tag']):
                for c in child.iterchildren(tag = tag_prefix + 'classificationValue'):
                    to_add = {'classificationSystemId': child.get('id'), 
                              'classificationSystemName': child.name.text}
                    to_add = store_fields(fields, c, to_add = to_add)
                    df.append(copy(to_add))
        elif filename == 'Compartments':
            for child in root.iterchildren(tag = tag_prefix + MD_tags.loc[filename, 'tag']):
                for c in child.iterchildren(tag = tag_prefix + 'subcompartment'):
                    to_add = {'compartmentId': child.get('id'), 
                              'compartmentName': child.name.text, 
                              'subcompartmentId': c.get('id'), 
                                'subcompartmentName': c.name.text, 
                                'comment': c.comment.text}
                    df.append(copy(to_add))
        else:
            for child in root.iterchildren(tag = tag_prefix + MD_tags.loc[filename, 'tag']):
                to_add = store_fields(fields, child, to_add = {})
                if hasattr(child, 'compartment'):
                    to_add['compartment'] = child.compartment.compartment.text
                    to_add['subcompartment'] = child.compartment.subcompartment.text
                df.append(copy(to_add))
                for p in child.iterchildren(tag = tag_prefix + 'property'):
                    to_add_ = copy(to_add)
                    to_add_['propertyId'] = p.get('propertyId')
                    to_add_['amount'] = p.get('amount')
                    if is_empty(to_add_['amount']):
                        to_add_['amount'] = 0.
                    else:
                        to_add_['amount'] = float(to_add_['amount'])
                    properties[filename].append(copy(to_add_))
        MD[filename] = list_to_df(df)
        for col in list(group['field name']):
            if col not in MD[filename]:
                MD[filename][col] = ''
    for filename in properties:
        properties[filename] = list_to_df(properties[filename])
        assert 'id' in properties[filename]
    
    def join_info(MD, properties):
        #add geography to ActivityIndex
        f = 'ActivityIndex'
        MD[f] = MD[f].set_index('geographyId')
        g = 'Geographies'
        t = MD[g].rename(columns = {'id': 'geographyId'})
        t = t.set_index('geographyId')[['shortname']]
        MD[f] = MD[f].join(t).reset_index()
        MD[f] = MD[f].rename(columns = {'shortname': 'geography'})
        
        #add activityName to ActivityIndex
        MD[f] = MD[f].set_index('activityNameId')
        g = 'ActivityNames'
        t = MD[g].rename(columns = {'id': 'activityNameId'})
        t = t.set_index('activityNameId')
        MD[f] = MD[f].join(t).reset_index()
        MD[f] = MD[f].rename(columns = {'name': 'activityName'})
        
        #add system model to ActivityIndex
        MD[f] = MD[f].set_index('systemModelId')
        g = 'SystemModels'
        t = MD[g].rename(columns = {'id': 'systemModelId'})
        t = t.set_index('systemModelId')
        MD[f] = MD[f].join(t).reset_index()
        MD[f] = MD[f].rename(columns = {'shortname': 'systemModelName'})
        
        #arrange Classifications
        f = 'Classifications'
        MD[f] = MD[f].rename(columns = {'name': 'classificationValueName', 
                                        'id': 'classificationValueId'})
        
        #arrange UnitConversions
        f = 'UnitConversions'
        MD[f]['factor'] = MD[f]['factor'].astype(float)
        df = MD[f].copy().rename(columns = {'unitFromName': 'unitToName', 
                                            'unitToName': 'unitFromName'})
        df['factor'] = df['factor'].apply(lambda x: 1./x)
        MD[f] = pd.concat([MD[f], df])
        
        
        #arrange properties
        for f in properties:
            properties[f] = properties[f].set_index('propertyId')
            g = 'Properties'
            properties[f] = properties[f].join(MD[g].set_index('id')[
                ['name', 'unitName']], rsuffix = '_').reset_index()
            del properties[f]['unitName']
            properties[f] = properties[f].rename(columns = {
                'unitName_': 'unitName', 
                'name_': 'propertyName', 
                'index': 'propertyId'})
                
        return MD, properties
    
    MD, properties = join_info(MD, properties)
    filename = 'ExchangeActivityIndex.xml'
    filelist = build_file_list(MD_xml_dir, 'xml')
    if filename in filelist:
        with open(os.path.join(MD_xml_dir, filename), encoding='utf8') as f:
            root = objectify.parse(f).getroot()
        df = []
        for exchangeActivityIndexEntry in root.iterchildren():
            for o in exchangeActivityIndexEntry.output.iterchildren():
                to_add = {'id': exchangeActivityIndexEntry.get('validIntermediateExchangeId'), 
                          'activityIndexEntryId': o.get('activityIndexEntryId')}
                df.append(to_add)
        df = list_to_df(df)
        df = df.set_index('id')
        tab = 'IntermediateExchanges'
        df = df.join(MD[tab].set_index('id')[['name']])
        df = df.reset_index().rename(columns = {'id': 'intermediateExchangeId'})
        tab = 'ActivityIndex'
        df = df.set_index('activityIndexEntryId').join(MD[tab].set_index('id')[['activityName', 'geography', 
                          'startDate', 'endDate']]).reset_index()
        MD['ExchangeActivityIndex'] = df.rename(columns = {'index': 'activityIndexEntryId'})
    
    for field in ['IntermediateExchanges prop.', 'ElementaryExchanges prop.']:
        new_field = field.replace(' prop.', '')
        MD[field] = properties[new_field].copy()
        
    if MD_xls_dump_dir is not None:
        print("Making xlsx version of MasterData in {}".format(MD_xls_dump_dir))
        MD_to_excel(MD_xls_dump_dir, MD)
    
    # Set useful indexes in MD for future queries
    
    def set_MD_indexes(MD):
        indices = {
            'Geographies': ['name'],
            'Units': ['name'],
            'IntermediateExchanges': ['name'], 
            'ElementaryExchanges': ['name', 'compartment', 'subcompartment'], 
            'Compartments': ['compartmentName', 'subcompartmentName'], 
            'Properties': ['name'], 
            'ActivityNames': ['name'], 
            'Classifications': ['classificationSystemName', 'classificationValueName'], 
            'IntermediateExchanges prop.': ['name'], 
            'ElementaryExchanges prop.': ['name', 'compartment', 'subcompartment'], 
            'Persons': ['name'], 
            'Companies': ['name'], 
                   }
        for tab, index in indices.items():
            if tab == 'Companies':
                MD[tab] = MD[tab][MD[tab]['name'].notnull()]
            MD[tab] = MD[tab].set_index(index, drop=True).sort_index(axis=0)
            MD[tab].sort_index(axis=1, inplace=True)
        return MD

    MD = set_MD_indexes(MD)
    pkl_dump(pickle_dump_dir, 'MD', MD)

    return os.path.join(pickle_dump_dir, 'MD.pkl')



def validate_master_data_dir(MD_xml_dir):
    """Ensure existance of master data directory and its contents.
    
    Doesn't return anything, simply stops execution 
    if master data directory is not valid.""" 

    assert os.path.isdir(MD_xml_dir),\
        "Master data folder not present or not correctly defined."
    files_present = os.listdir(MD_xml_dir)
    required_files = [
            'ActivityIndex.xml',
            'ActivityNames.xml',
            'Classifications.xml',
            'Companies.xml',
            'Compartments.xml',
            'Context.xml',
            'DeletedMasterData.xml',
            'ElementaryExchanges.xml',
            'ExchangeActivityIndex.xml',
            'Geographies.xml',
            'IntermediateExchanges.xml',
            'Languages.xml',
            'MacroEconomicScenarios.xml',
            'Parameters.xml',
            'Persons.xml',
            'Properties.xml',
            'Sources.xml',
            'SystemModels.xml',
            'Tags.xml',
            'UnitConversions.xml',
            'Units.xml',
            ]
    missing_files = [file for file in required_files
                     if file not in files_present
                    ]
    assert not missing_files,\
        "Files missing from master data: {}".format(missing_files)
    
def MD_to_excel(fp, MD):
    excel_columns = {
            'ActivityIndex': ['id', 'systemModelName', 'activityName', 'geography', 'startDate', 'endDate', 
                'systemModelId', 'activityNameId', 'specialActivityType'], 
            'IntermediateExchanges': ['id', 'name', 'unitName', 'casNumber', 'comment'], 
            'ElementaryExchanges': ['id', 'name', 'compartment', 'subcompartment', 'unitName', 'casNumber', 'comment'], 
            'Geographies': ['id', 'name', 'shortname', 'uNCode', 'uNRegionCode', 
                'uNSubregionCode', 'latitude', 'longitude'], 
            'Parameters': ['id', 'name', 'unitName', 'unitId', 'defaultVariableName', 'comment'], 
            'ActivityNames': ['id', 'name'], 
            'Classifications': ['classificationSystemId', 'classificationSystemName', 
                'classificationValueId', 'classificationValueName', 'comment'], 
            'Companies': ['id', 'code', 'name', 'website', 'comment'], 
            'Compartments': ['compartmentId', 'compartmentName', 'subcompartmentId', 
                'subcompartmentName', 'comment'], 
            'Languages': ['code', 'comment'], 
            'Persons': ['id', 'name', 'companyId', 'companyName', 'email', 'address', 'telephone', 'telefax'], 
            'Properties': ['id', 'name', 'unitName', 'comment'], 
            'Sources': ['id', 'firstAuthor', 'additionalAuthors', 'title', 'issueNo', 'journal', 'namesOfEditors', 
                'pageNumbers', 'placeOfPublications', 'publisher', 'sourceType', 'titleOfAnthology', 
                'volumeNo', 'year'], 
            'SystemModels': ['id', 'name', 'shortname'], 
            'Tags': ['name', 'comment'], 
            'Units': ['id', 'name', 'comment'], 
            'UnitConversions': ['unitType', 'unitFromName', 'unitToName', 'factor'], 
            'MacroEconomicScenarios': ['id', 'name', 'comment'], 
            'IntermediateExchanges prop.': ['id', 'name', 'propertyId', 'propertyName', 'amount', 'unitName'], 
            'ElementaryExchanges prop.': ['id', 'name', 'propertyId', 'compartment', 'subcompartment', 
                                        'propertyName', 'amount', 'unitName'], 
            'ExchangeActivityIndex': ['intermediateExchangeId', 'activityIndexEntryId', 'name', 
                   'activityName', 'geography', 'startDate', 'endDate']
            }
    dfs = []
    for tab, columns in excel_columns.items():
        dfs.append((MD[tab], tab, columns))
    filename = 'MasterData.xlsx'
    dataframe_to_excel(fp, filename, dfs, feedback = True)
    return None