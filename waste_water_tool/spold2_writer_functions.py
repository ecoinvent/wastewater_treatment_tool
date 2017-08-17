# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import os, uuid, numpy, pandas
from pickle import dump, load
from lxml import objectify
from copy import copy

# Taking care of pandas version issues in unpickling...
import pandas
import sys
#sys.modules['pandas.indexes'] = pandas.core.indexes

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

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))

class GenericObject:
    def __init__(self, d, object_type):
        self.template_name = '%s_2.xml' % object_type
        assert type(d) == dict
        for key, value in d.items():
            setattr(self, key, value)

def make_uuid(l):
    if type(l) == str:
        l = [l]
    else:
        assert type(l) in [list, set, tuple]
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, ''.join(l)))

def recursive_rendering(e, env, result_folder, result_filename):
    if type(e) == GenericObject:
        template = env.get_template(e.template_name)
        attr_list = set([a for a in dir(e) if '__' not in a])
        attr_list.difference_update(set(['render', 'template_name']))
        rendered = {attribute: recursive_rendering(getattr(e, attribute), 
             env, result_folder, result_filename) for attribute in attr_list}
        rendered = template.render(**rendered)
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

def add_path_in_list(l, path):
    return [os.path.join(path, filename) for filename in l]

def folder_and_file_list(dirpath, add_path = False):
    #returns the list of files and folders in a folder
    folders = []
    files = []
    for filename in os.listdir(dirpath):
        if '~' not in filename:
            if os.path.isdir(os.path.join(dirpath, filename)):
                folders.append(filename)
            else:
                files.append(filename)
    if add_path:
        files = add_path_in_list(files, dirpath)
        folders = add_path_in_list(folders, dirpath)
    return folders, files

def find_current_MD_path():
    folder = r'C://'
    folders, files = folder_and_file_list(folder)
    found = False
    if 'Users' in folders:
        folder = os.path.join(folder, 'Users')
        folders, files = folder_and_file_list(folder, add_path = True)
        for folder in folders:
            folder = os.path.join(folder, 'Documents', 'ecoinvent')
            if os.path.exists(folder):
                found = True
                break
            else:
                pass
            
    if not found:
        raise ValueError('not successful in finding the master data folder')
    else:
        folder = os.path.join(folder, 'EcoEditor', 'xml', 'MasterData', 'Production')
    return folder

def build_file_list(dirpath, extension = None, add_path = False):
    '''returns a list of filenames inside the specified path, excluding other folders, 
    temporary files, and filtering for extensions if specified'''
    
    if extension == None:
        filelist = [filename for filename in os.listdir(dirpath) 
            if not os.path.isdir(os.path.join(dirpath, filename)) and '~' not in filename]
    elif type(extension) == list:
        filelist = [filename for filename in os.listdir(dirpath) 
            if not os.path.isdir(os.path.join(dirpath, filename))
            and filename.split('.')[-1].lower() in extension and '~' not in filename]
    else:
        filelist = [filename for filename in os.listdir(dirpath) 
            if not os.path.isdir(os.path.join(dirpath, filename))
            and filename.split('.')[-1].lower() == extension and '~' not in filename]
    if add_path:
        filelist = add_path_in_list(filelist, dirpath)
    return filelist

def find_youngest(files):
    #accepts a list of files (including path)
    #check which one is the youngest based on last save timestamp
    t = 0.
    for f in files:
        t_ = os.path.getmtime(f)
        if t_ > t:
            youngest = copy(f)
            t = copy(t_)
    return youngest, t

def get_current_MD(master_data_folder=None, pkl_folder=None, return_MD=False):
    '''Generate a dictionary `MD` with keys=names of the master data files and
       values=pandas dataframes with all elements and attributes
       Will only generate `MD` if such a dictionary does not already exist
       or if the existing MD is older than any of the Master data files.
       If paths to master_data_folder, pkl_folder are not passed as arguments,
       the function will look for them where it expects them to be found.
    '''       
    # Find the age of the youngest current MD file
    if master_data_folder is None:
        master_data_folder = find_current_MD_path()
    filelist = build_file_list(master_data_folder,
                               extension = 'xml',
                               add_path = True)
    youngest, t_MD = find_youngest(filelist)
    
    # Find the age of the pkl
    if pkl_folder is None:
        pkl_folder = os.path.join(root_dir, 'pkl')
    filelist = build_file_list(pkl_folder)
    
    # Determine whether an update of the existing MD is necessary
    update = True
    if 'MD.pkl' in filelist:
        existing_MD = os.path.join(pkl_folder, 'MD.pkl')
        t_pkl = os.path.getmtime(existing_MD)
        update = t_MD > t_pkl
    if update:
        # No MD or MD older than current master data: time to update!
        md_fields_xls = os.path.join(
                root_dir,
                'documentation',
                'MasterData_fields.xlsx')
        MD = build_MD(md_fields_xls,
                      master_data_folder,
                      pickle_dump_folder=pkl_folder,
                      xls_dump_folder=os.path.join(
                              root_dir,
                              'documentation')
                      )
    else:
        MD = pkl_load(pkl_folder, 'MD')
    if return_MD:
        return MD
    else:
        return None
    

def pkl_dump(folder, variable_name, variable, feedback = False):
    '''helper function for saving files in pkl'''
    
    filename = os.path.join(folder, variable_name + '.pkl')
    file = open(filename, 'wb')
    dump(variable, file)
    file.close()
    if feedback:
        print('created "%s" in %s' % (variable_name + '.pkl', folder))

def pkl_load(folder, variable_name):
    
    filename = os.path.join(folder, str(variable_name) + '.pkl')
    file = open(filename, 'rb')
    v = load(file)
    file.close()
    
    return v

def is_empty(e):
    '''Checks if "e" is of certain values that usually mean that no info is available'''
    
    if type(e) in [float, numpy.float, numpy.float64, numpy.float16, numpy.float32, numpy.float_]:
        test = e in [numpy.nan, numpy.NaN] or numpy.isnan(e)
    else:
        test = e in ['', None, [], set(), dict()]
    
    return test

def build_MD(md_fields_xls=None,
             master_data_folder=None,
             pickle_dump_folder=None,
             xls_dump_folder=None):
    MD = {}
    if master_data_folder is None:
        master_data_folder = find_current_MD_path()
    if md_fields_xls is None:
        md_fields_xls = os.path.join(
                root_dir,
                'documentation',
                'MasterData_fields.xlsx'
                )
    MD_fields = pandas.read_excel(md_fields_xls, 'fields')
    MD_tags = pandas.read_excel(md_fields_xls, 'tags').set_index('file')
    properties = {}
    grouped = MD_fields.groupby('file')
    for filename, group in grouped:
        if 'Exchange' in filename:
            properties[filename] = []
        df = []
        with open(os.path.join(master_data_folder, '%s.xml' % filename), encoding = 'utf8') as f:
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
        if 'id' not in properties[filename]:
            1/0
    MD, properties = join_info(MD, properties)
    filename = 'ExchangeActivityIndex.xml'
    filelist = build_file_list(master_data_folder, 'xml')
    if filename in filelist:
        with open(os.path.join(master_data_folder, filename), encoding='utf8') as f:
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
        
    if xls_dump_folder is not None:
        to_excel(xls_dump_folder, MD)
    # Set useful indexes in MD for future queries
    MD = set_MD_indexes(MD)
    if pickle_dump_folder is not None:
        pkl_dump(pickle_dump_folder, 'MD', MD)

    return MD

def list_to_df(l, index_start = 0):
    '''Takes a list of dictionaries, makes a data frame.
       Option to start index not at zero.'''
    
    d = {i + index_start: l[i] for i in range(len(l))}
    d = pandas.DataFrame(d).transpose()
    
    return d

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
    MD[f] = pandas.concat([MD[f], df])
    
    
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

def to_excel(excel_folder, MD):
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
    dataframe_to_excel(excel_folder, filename, dfs, feedback = True)
    return None

def dataframe_to_excel(folder, filename, dfs, read_me = False, feedback = False):
    '''function to take care of aggregating sheets, freeze pane and meta info'''
    
    writer = pandas.ExcelWriter(os.path.join(folder, filename), engine='xlsxwriter')
    
    #maybe a read me sheet
    if read_me != False:
        assert type(read_me) == list
        df = []
        for e in read_me:
            assert type(e) in (list, tuple)
            df.append(dict(zip([i for i in range(len(e))], e)))
        df = list_to_df(df)
        columns = [i for i in range(len(df.columns))]
        df.to_excel(writer, 'read me', columns = columns, 
                    index = False, merge_cells = False, header = False)
    
    #save all df with their columns
    for df, sheet_name, columns in dfs:
        #validate the types of elements
        assert type(df) in [type(pandas.DataFrame()), list]
        if type(df) == list:
            #in case it was forgotten to transform from list to dataframe
            df = list_to_df(df)
        assert type(sheet_name) == str
        assert type(columns) in (tuple, list)

        #check if all columns asked to be displayed in columns are present in the dataframe
        missing = set(columns).difference(set(df.columns))
        if len(missing):
            print('The data frame for sheet "%s" should contain the following columns:' % sheet_name)
            for m in missing:
                print(m)
            raise NotImplementedError

        #add the sheet to the writer
        sheet_name = remove_forbiden_in_tabname(sheet_name)
        df.to_excel(writer, sheet_name, columns = columns, 
                    index = False, merge_cells = False)
    
    #freeze panes and filters
    for sht_name in writer.sheets:
        if sht_name != 'read me':
            ws = writer.sheets[sht_name]
            #ws.auto_filter.ref = 'A1:%s%s' % (get_column_letter(ws.dim_colmax), ws.dim_rowmax-1)
            #ws.auto_filter.add_filter_column(0, dfs[writer.sheets.index(sht_name)][1])
            ws.freeze_panes(1,0)
    
    #save and close
    writer.save()
    writer.close()

    #give feedback if asked
    if feedback:
        print('"%s" ready in %s' % (filename, folder))
        print('')

def remove_forbiden_in_tabname(s):
    #truncates tab names in excel sheet if too long and removes forbiden characters

    limit = 31
    for before, after in [('/', '_'), 
            ('<', 'smaller than'), 
            ('>', 'larger than')]:
        s = s.replace(before, after)
    if len(s) > limit:
        s = s[:limit]

    return s

def set_MD_indexes(MD):
    print('setting MD indices')
    indexes = {
        'Geographies': ['shortname'], 
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
    for tab, index in indexes.items():
        if tab == 'Companies':
            MD[tab] = MD[tab][MD[tab]['name'].notnull()]
        MD[tab] = MD[tab].set_index(index, drop=True).sort_index(axis=0)
        MD[tab].sort_index(axis=1, inplace=True)
    return MD


def append_exchange(exc, #exchange dictionary, see detail below
                    dataset, #dataset to append exchange to
                    MD, #master data dictionary of dataframes
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
                                                 'pedigreeMatrix': [x,x,x,x,x]
                                                 }
    PV_uncertainty
    """
    # Add unitId to exchange
    exc['unitId'] = MD['Units'].loc[exc['unitName'], 'id']

    # Add IntermediateExchange to MD if new:
    if exc['group'] in ['ReferenceProduct', 'ByProduct', 'FromTechnosphere'] \
        and exc['name'] not in MD['IntermediateExchanges'].index:
        dataset, MD = new_intermediate_exchange(dataset, MD, exc)
    # Generate UUID for exchange. New UUID for each exchange/dataset combination
    l = [dataset[field] for field in ['activityName',
                                      'geography',
                                      'startDate',
                                      'endDate']
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
        sel = MD['ElementaryExchanges'].loc[ee]
        if isinstance(sel, pandas.DataFrame):
            if len(sel) > 1:
                raise ValueError('Multiple MD entries corresponding to %s, %s, %s' % ee)
            sel = sel.iloc[0]
        exc['elementaryExchangeId'] = sel['id']
        exc['exchangeType'] = 'elementaryExchange'
        exc['subcompartmentId'] = MD['Compartments'].loc[ee[1:], 'subcompartmentId']
        exc['groupCode'] = 4
        if ee in MD['ElementaryExchanges prop.'].index:
            property_sel = MD['ElementaryExchanges prop.'].loc[ee]
        else:
            property_sel = pandas.DataFrame()
   
    else: # If intermediateExchange
        sel = MD['IntermediateExchanges'].loc[exc['name']]
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
        if exc['name'] in MD['IntermediateExchanges prop.'].index:
            property_sel = MD['IntermediateExchanges prop.'].loc[exc['name']]
        else:
            property_sel = pandas.DataFrame()
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
    dataset, exc = add_property(dataset, exc, properties, MD)
    
    if uncertainty:
        exc = add_uncertainty(exc, uncertainty['pedigreeMatrix'], 
            uncertainty['variance'])
    if PV_uncertainty:
        exc = add_uncertainty(exc, PV_uncertainty['pedigreeMatrix'], 
            PV_uncertainty['variance'], PV = True)
    dataset[exc['group']].append(GenericObject(exc, 'Exchange'))
    return dataset, MD

def create_empty_uncertainty():
    empty_fields = ['minValue', 'mostLikelyValue', 'maxValue', 'standardDeviation95', 'comment']
    return {f: None for f in empty_fields}

def add_uncertainty(o, pedigreeMatrix, variance, PV = False):
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
    o[unc['field']] = GenericObject(unc, 'TUncertainty')
    return o

def new_intermediate_exchange(dataset, MD, exc):
    fields = ['name', 'unitName', 'casNumber', 'comment', 'unitId']
    to_add = {field: exc[field] for field in fields}
    to_add['id'] = make_uuid(exc['name'])
    tab = 'IntermediateExchanges'
    #add entry to user MD
    if tab not in dataset:
        dataset[tab] = []
    dataset[tab].append(GenericObject(to_add, tab))
    #add entry to MD
    new_entry = list_to_df([to_add]).set_index('name')
    MD['IntermediateExchanges'] = pandas.concat([MD[tab], new_entry])
    
    return dataset, MD

def create_empty_dataset():
    ''' Create an empty 'dataset' dictionary with all the right keys.
    '''    
    
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
    
    #TEMP???
    # mandatory values.  Data entry will be from the current user
    # and active authorship will have to be accepted.    

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

def add_property(dataset, exc, properties, MD):
    exc['properties'] = []
    for property_name, amount, unit, comment, unc in properties:
        p = create_empty_property()
        p['name'] = property_name
        if property_name in MD['Properties'].index:
            sel = MD['Properties'].loc[property_name]
            p['propertyId'] = sel['id']
            if not is_empty(sel['unitName']):
                assert unit == sel['unitName'], "{}, {}, {}".format(property_name, unit, sel['unitName'])
                p['unitName'] = unit
                p['unitId'] = MD['Units'].loc[p['unitName'], 'id']
        else:
            p['propertyId'] = make_uuid(property_name)
            p['unitName'] = unit
            p['unitId'] = MD['Units'].loc[p['unitName'], 'id']
            print("going to create new property")
            dataset['Properties'].append(GenericObject(p,
                                        'TProperty'
                                        ))
        p['amount'] = amount
        p['comment'] = comment
        if not is_empty(unc):
            p = add_uncertainty(p, unc['pedigreeMatrix'], unc['variance'])
        exc['properties'].append(GenericObject(p, 'TProperty'))
    return dataset, exc

def create_empty_property():
    empty_fields = ['propertyContextId', 'unitContextId', 'isDefiningValue', 
        'isCalculatedAmount', 'sourceId', 'sourceContextId', 
        'sourceIdOverwrittenByChild', 'sourceYear', 'sourceFirstAuthor', 
        'mathematicalRelation', 'variableName', 'uncertainty', 'comment']
    return {field: None for field in empty_fields}


def create_WWT_activity_name(WW_type, technology, capacity):
    if WW_type == 'average':
        WW_type_str = ", average"
    else:
        WW_type_str = " {}".format(WW_type)
    
    if technology == 'average':
        technology_str = ""
    else:
        technology_str = "{}, ".format(technology)
    
    if capacity == 'average':
        capacity_str = "average capacity"
    else:
        capacity_str = "capacity {:.1E}l/year".format(capacity).replace('+', '').replace('E0', 'E').replace('.0', '')
    
    return "treatment of wastewater{}, {}{}".format(WW_type_str, technology_str, capacity_str)

def generate_WWT_activity_name(dataset, WW_type, technology, capacity):
    name = create_WWT_activity_name(WW_type, technology, capacity)
    dataset.update({'activityName': name,
                    'WW_type': WW_type})


def generate_activityNameId(dataset, MD):
    ''' Return activityNameId from MD or create one
    '''
    
    if dataset['activityName'] in MD['ActivityNames'].index:
        dataset.update({'activityNameId':
            MD['ActivityNames'].loc[dataset['activityName'], 'id']
                        })
    else:
        print("new name {} identified, generating new UUID".format(
                dataset['activityName']))
        activityNameId = make_uuid(dataset['activityName'])
        #creating a new user masterdata entry
        d = {'id': activityNameId, 
             'name': dataset['activityName']}
        dataset.update({'activityNameId' : activityNameId,
                        'ActivityNames': [GenericObject(d, 'ActivityNames')]
                        })
        
def generate_geography(dataset, MD, geography):
    dataset.update({'geography': geography,
                    'geographyId': 
                        MD['Geographies'].loc[geography, 'id']
                        })

def generate_time_period(dataset, start, end):
    dataset.update({'startDate':start,
                    'endDate':end})

def generate_dataset_id(dataset):
    '''the activityName, geography, startDate and endDate need to be
        defined first'''
    l = [dataset['activityName'], dataset['geography'], dataset['startDate'], dataset['endDate']]
    dataset.update({'id':make_uuid(l)})

def generate_technology_level(dataset, level_as_string):
    level_string_to_int = {
            'Undefined':0,
            'New':1,
            'Modern':2,
            'Current':3,
            'Old':4,
            'Outdated':5
            }
    dataset.update({
            'technologyLevel':level_string_to_int[level_as_string],
            })

def generate_activity_boundary_text(dataset,
                                    includedActivitiesStartText,
                                    includedActivitiesEndText_last,
                                    includedActivitiesEndText_included,
                                    includedActivitiesEndText_excluded):
    dataset.update({'includedActivitiesStart': includedActivitiesStartText,
                    'includedActivitiesEnd': "{} {} {}".format(
                            includedActivitiesEndText_last,
                            includedActivitiesEndText_included,
                            includedActivitiesEndText_excluded)
                    })

def generate_comment(dataset, comment_type, list_of_string_comments):
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
    dataset.update({
            comment_type:GenericObject(d, 'TTextAndImage')
            })

def  generate_representativeness(dataset,
                                 samplingProcedure_text='',
                                 extrapolations_text='',
                                 percent=None):
    assert all([str(percent).isnumeric(), 0<percent<100]),\
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
         'extrapolations':samplingProcedure_text,
         }
    dataset['modellingAndValidation'] = GenericObject(d,
                                            'ModellingAndValidation'
                                            )

def generate_activityIndex(dataset):
    d = {'id': dataset['id'], 
         'activityNameId': dataset['activityNameId'],
         'geographyId': dataset['geographyId'],
         'startDate': dataset['startDate'],
         'endDate': dataset['endDate'],
         'specialActivityType': dataset['specialActivityType'],
         'systemModelId': '8b738ea0-f89e-4627-8679-433616064e82',
         }
    dataset['ActivityIndex'] = [GenericObject(d, 'ActivityIndex')]

def get_WW_properties(xls=None):
    # From excel for now
    if xls==None:
        xls = os.path.join(root_dir, 'Documentation', 'WW_properties.xlsx')
    return pandas.read_excel(xls, sheet_name='Sheet1', index_col=1)

def convert_WW_prop_to_list(df):
    #(property_name, amount, unit, comment, uncertainty)
    return [(i,
             df.loc[i, 'Amount'],
             df.loc[i, 'unitName'],
             df.loc[i, 'comment'],
             {
                 'variance': df.loc[i, 'Variance'],
                 'pedigreeMatrix': [
                     df.loc[i, 'pedigree1'],
                     df.loc[i, 'pedigree2'],
                     df.loc[i, 'pedigree3'],
                     df.loc[i, 'pedigree4'],
                     df.loc[i, 'pedigree5'],
                 ]
             }
            ) for i in df.index]

        
def generate_reference_exchange(dataset,
                              exc_comment,
                              PV,
                              PV_comment,
                              PV_uncertainty,
                              MD):
    exc = create_empty_exchange()
    if dataset['WW_type']=='average':
        name = 'wastewater, average'
    else:
        name = 'wastewater, {}'.format(dataset['WW_type'])
        
    exc.update({
            'group': 'ReferenceProduct',
            'unitName': 'm3',
            'amount': -1.,
            'productionVolumeAmount': PV,
            'productionVolumeComment': PV_comment, 
           'comment': exc_comment, 
           'name': name,
           })
    
    # Replace this by function to retreive properties from tool
    properties = convert_WW_prop_to_list(get_WW_properties()) 
    dataset, MD = append_exchange(exc,
                                  dataset,
                                  MD,
                                  properties = properties,
                                  uncertainty = None,
                                  PV_uncertainty = PV_uncertainty)
    return dataset, MD

def generate_reference_exchange(dataset,
                              exc_comment,
                              PV,
                              PV_comment,
                              PV_uncertainty,
                              MD):
    exc = create_empty_exchange()
    if dataset['WW_type']=='average':
        name = 'wastewater, average'
    else:
        name = 'wastewater, {}'.format(dataset['WW_type'])
        
    exc.update({
            'group': 'ReferenceProduct',
            'unitName': 'm3',
            'amount': -1.,
            'productionVolumeAmount': PV,
            'productionVolumeComment': PV_comment, 
           'comment': exc_comment, 
           'name': name,
           })
    
    # Replace this by function to retreive properties from tool
    properties = convert_WW_prop_to_list(get_WW_properties()) 
    dataset, MD = append_exchange(exc,
                                  dataset,
                                  MD,
                                  properties = properties,
                                  uncertainty = None,
                                  PV_uncertainty = PV_uncertainty)
    return dataset, MD

def add_grit(dataset,
             grit_amount,
             WW_discharged_without_treatment,
             grit_plastic_ratio,
             grit_biomass_ratio,
             grit_uncertainty,
             grit_plastics_comment,
             grit_biomass_comment,
             PV,
             MD):
    # plastic
    exc = create_empty_exchange()
    exc.update({'group': 'ByProduct', 
           'name': 'waste plastic, mixture', 
           'unitName': 'kg', 
           'amount': grit_amount * grit_plastic_ratio * (1-WW_discharged_without_treatment), 
           'productionVolumeAmount': PV*grit_amount * grit_plastic_ratio * (1-WW_discharged_without_treatment), 
           'productionVolumeComment': 'Calculated based on the amount and the total volume of wastewater discharged', 
           'comment': grit_plastics_comment, 
           })
    uncertainty = grit_uncertainty
    dataset, MD = append_exchange(exc, dataset, MD, 
        properties = [], uncertainty = uncertainty)
    # biomass
    exc = create_empty_exchange()
    exc.update({'group': 'ByProduct', 
           'name': 'waste graphical paper', 
           'unitName': 'kg',
           'amount': grit_amount * grit_biomass_ratio * (1-WW_discharged_without_treatment), 
           'productionVolumeAmount': PV*grit_amount * grit_biomass_ratio * (1-WW_discharged_without_treatment), 
           'productionVolumeComment': 'Calculated based on the amount and the total volume of wastewater discharged', 
           'comment': grit_biomass_comment, 
           })
    uncertainty = grit_uncertainty
    dataset, MD = append_exchange(exc, dataset, MD, 
        properties = [], uncertainty = uncertainty)
    return dataset



def generate_ecoSpold2(dataset, template_path, filename, dump_folder):
    dataset['has_userMD'] = False
    for field in ['ActivityNames', 'Sources', 'activityIndexEntry', 'Persons', 'IntermediateExchanges']:
        if field in dataset and len(dataset[field]) > 0:
            dataset['has_userMD'] = True
            break
    dataset['exchanges'] = []
    for group in ['ReferenceProduct', 'ByProduct', 'FromTechnosphere', 'FromEnvironment', 'ToEnvironment']:
    #groups need to appear in a specific order
        dataset['exchanges'].extend(dataset[group])

    dataset = GenericObject(dataset, 'Dataset')
    #loading the template environment
    
    env = Environment(loader=FileSystemLoader(template_path), 
                      keep_trailing_newline = True, 
                      lstrip_blocks = True, 
                      trim_blocks = True)
    rendered = recursive_rendering(dataset, env, dump_folder, filename)

"""

#filling with exchanges
#ReferenceProduct example

PV_uncertainty = {'variance': .003, 'pedigreeMatrix': [1, 2, 1, 1, 1]}
dataset, MD = append_exchange(exc, dataset, MD, 
    properties = properties, PV_uncertainty = PV_uncertainty)

#ByProduct example
exc = create_empty_exchange()
exc.update({'group': 'ByProduct', 
       'name': 'sludge from dinosaur zoo', 
       'unitName': 'kg', 
       'amount': 0.4, 
       'productionVolumeAmount': 8000., 
       'productionVolumeComment': 'production volume comment', 
       'comment': 'exchange comment', 
       })
uncertainty = {'variance': .005, 'pedigreeMatrix': [1, 2, 1, 1, 5]}
dataset, MD = append_exchange(exc, dataset, MD, 
    properties = properties, uncertainty = uncertainty)

#FromEnvironment example
exc = create_empty_exchange()
exc.update({'group': 'FromEnvironment', 
       'name': 'Oxygen', 
       'compartment': 'natural resource', 
       'subcompartment': 'in air', 
       'unitName': 'kg', 
       'amount': 0.002, 
       'comment': 'exchange comment', 
       })
dataset, MD = append_exchange(exc, dataset, MD)

#ToEnvironment example
exc = create_empty_exchange()
exc.update({'group': 'ToEnvironment', 
       'name': 'Carbon dioxide, fossil', 
       'compartment': 'air', 
       'subcompartment': 'unspecified', 
       'unitName': 'kg', 
       'amount': 0.02, 
       'comment': 'exchange comment', 
       })
dataset, MD = append_exchange(exc, dataset, MD)

#FromTechnosphere example
exc = create_empty_exchange()
exc.update({'group': 'FromTechnosphere', 
       'name': 'electricity, medium voltage', 
       'unitName': 'kWh', 
       'amount': 2.3, 
       'comment': 'exchange comment', 
       })
dataset, MD = append_exchange(exc, dataset, MD)
dataset['exchanges'] = []
for group in ['ReferenceProduct', 'ByProduct', 'FromTechnosphere', 'FromEnvironment', 'ToEnvironment']:
    #groups need to appear in a specific order
    dataset['exchanges'].extend(dataset[group])

#do the new exchange property in MD? Issue #3

dataset['has_userMD'] = False
for field in ['ActivityNames', 'Sources', 'activityIndexEntry', 'Persons', 'IntermediateExchanges']:
    if field in dataset and len(dataset[field]) > 0:
        dataset['has_userMD'] = 'oui'
        break
    
result_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'result_folder')
result_filename = 'test.spold'
dataset = GenericObject(dataset, 'Dataset')
#loading the template environment
template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_path), 
                  keep_trailing_newline = True, 
                  lstrip_blocks = True, 
                  trim_blocks = True)
rendered = recursive_rendering(dataset, env, result_folder, result_filename)
"""

