# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import os, uuid, numpy, pandas
from pickle import dump, load
from lxml import objectify
from copy import copy

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

def get_current_MD():
    #find the age of the youngest current MD file
    master_data_folder = find_current_MD_path()
    filelist = build_file_list(master_data_folder, extension = 'xml', add_path = True)
    youngest, t_MD = find_youngest(filelist)
    #find the age of the pkl
    pkl_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pkl')
    filelist = build_file_list(pkl_folder)
    update = True
    if 'MD.pkl' in filelist:
        filelist = [os.path.join(pkl_folder, 'MD.pkl')]
        youngest, t_pkl = find_youngest(filelist)
        update = t_MD > t_pkl
    if update:
        #current MD more recent or missing: time to update!
        version = 'CIRAIG'
        system_model = 'Undefined'
        dummy = ''
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'documentation')
        build_MD(folder, version, system_model, dummy, master_data_folder = master_data_folder)
    MD = pkl_load(pkl_folder, 'MD')
    return MD
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

def build_MD(folder, version, system_model, basepath, master_data_folder = ''):
    print('reading master data from %s' % folder)
    MD = {}
    if master_data_folder == '':
        master_data_folder = os.path.join(folder, 'MasterData')
    p = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
        'documentation', 'MasterData_fields.xlsx')
    MD_fields = pandas.read_excel(p, 'fields')
    MD_tags = pandas.read_excel(p, 'tags').set_index('file')
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
        
    MD = to_excel(folder, MD, properties)
    folder = os.path.join(os.path.dirname(folder), 'pkl')
    pkl_dump(folder, 'MD', MD)

def list_to_df(l, index_start = 0):
    '''takes a list of dictionaries, makes a data frame.  Option to start index not at zero.'''
    
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

def to_excel(excel_folder, MD, properties = []):
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
    print('creating MasterData.xlsx in %s' % excel_folder)
    dfs = []
    for tab, columns in excel_columns.items():
        if 'prop.' not in tab:
            dfs.append((MD[tab], tab, columns))
        else:
            new_tab = tab.replace(' prop.', '')
            dfs.append((properties[new_tab], tab, excel_columns[tab]))
            MD[tab] = properties[new_tab].copy()
    filename = 'MasterData.xlsx'
    dataframe_to_excel(excel_folder, filename, dfs, feedback = True)
    
    return MD

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
        assert isinstance(df, pandas.DataFrame) or isinstance(df, list)
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

def fix_MD_index(MD):
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
        MD[tab] = MD[tab].set_index(index).sortlevel(level=0)
    return MD

def append_exchange(exc, dataset, MD, properties = [], 
        uncertainty = {}, PV_uncertainty = {}):
    exc['unitId'] = MD['Units'].loc[exc['unitName'], 'id']
    if exc['name'] not in MD['IntermediateExchanges'].index:
        dataset, MD = new_exchange(dataset, MD, exc)
    l = [dataset[field] for field in ['activityName', 'geography', 'startDate', 'endDate']]
    l.extend(str(exc[field]) for field in ['name', 'compartment', 'subcompartment'])
    exc['id'] = make_uuid(l)
    if 'From' in exc['group']:
        exc['groupType'] = 'inputGroup'
    else:
        exc['groupType'] = 'outputGroup'
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
    else:
        sel = MD['IntermediateExchanges'].loc[exc['name']]
        exc['intermediateExchangeId'] = sel['id']
        exc['exchangeType'] = 'intermediateExchange'
        if exc['group'] == 'ReferenceProduct':
            exc['groupCode'] = 0
        elif exc['group'] == 'FromTechnosphere':
            exc['groupCode'] = 5
        elif exc['group'] == 'ByProduct':
            exc['groupCode'] = 2
        else:
            raise ValueError('"%s" is not a valid group' % exc['group'])
        if exc['name'] in MD['ElementaryExchanges prop.'].index:
            property_sel = MD['ElementaryExchanges prop.'].loc[exc['name']]
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
                properties.append((p['propertyName'], p['amount'], '', None))
    exc = add_property(exc, properties, MD)
    
    if len(uncertainty) > 0:
        exc = add_uncertainty(exc, uncertainty['pedigreeMatrix'], 
            uncertainty['variance'])
    if len(PV_uncertainty) > 0:
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

def new_exchange(dataset, MD, exc):
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
    dataset = {}
    #mandatory fixed values
    dataset['activityDataset'] = 'activityDataset'
    dataset['inheritanceDepth'] = 0
    dataset['type'] = 1
    dataset['specialActivityType'] = 0
    dataset['isDataValidForEntirePeriod'] = 'true'
    dataset['macroEconomicScenarioName'] = 'Business-as-Usual'
    dataset['macroEconomicScenarioId'] = 'd9f57f0a-a01f-42eb-a57b-8f18d6635801'
    #mandatory values fixed to None (will not show in the rendered template)
    empty_fields = ['parentActivityId', 'parentActivityContextId', 'energyValues', 
        'masterAllocationPropertyId', 'masterAllocationPropertyIdOverwrittenByChild', 
        'activityNameContextId', 'geographyContextId', 'macroEconomicScenarioContextId', 
        'macroEconomicScenarioContextId', 'originalActivityDataset', 'macroEconomicScenarioComment']
    dataset.update({f: None for f in empty_fields})
    for group in ['ReferenceProduct', 'ByProduct', 'FromTechnosphere', 'FromEnvironment', 'ToEnvironment']:
        dataset[group] = []
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

def add_property(exc, properties, MD):
    exc['properties'] = []
    for property_name, amount, comment, unc in properties:
        p = create_empty_property()
        p['name'] = property_name
        p['amount'] = amount
        p['comment'] = comment
        sel = MD['Properties'].loc[property_name]
        p['propertyId'] = sel['id']
        if not is_empty(sel['unitName']):
            p['unitName'] = sel['unitName']
            p['unitId'] = MD['Units'].loc[p['unitName'], 'id']
        if not is_empty(unc):
            p = add_uncertainty(p, unc['pedigreeMatrix'], unc['variance'])
        exc['properties'].append(GenericObject(p, 'TProperty'))
    return exc

def create_empty_property():
    empty_fields = ['propertyContextId', 'unitContextId', 'isDefiningValue', 
        'isCalculatedAmount', 'sourceId', 'sourceContextId', 
        'sourceIdOverwrittenByChild', 'sourceYear', 'sourceFirstAuthor', 
        'mathematicalRelation', 'variableName', 'uncertainty', 'comment']
    return {field: None for field in empty_fields}

#loading the template environment
template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_path), 
                  keep_trailing_newline = True, 
                  lstrip_blocks = True, 
                  trim_blocks = True)

#loading MD and fix the index
MD = get_current_MD() 
MD = fix_MD_index(MD)

#creating a dummy example
#start by create an empty dataset
dataset = create_empty_dataset()
#activityName by user
dataset['activityName'] = 'treatment of wastewater, from dinosaur zoo'
#activityNameId in MD or from the activityName
if dataset['activityName'] in MD['ActivityNames'].index:
    dataset['activityNameId'] = MD['ActivityNames'].loc[dataset['activityName'], 'id']
else:
    dataset['activityNameId'] = make_uuid(dataset['activityName'])
    field = 'ActivityNames'
    #creating a new user masterdata entry
    d = {'id': dataset['activityNameId'], 
         'name': dataset['activityName']}
    dataset[field] = [GenericObject(d, field)]
#geography by user, uuid in MD
geography = 'GLO'
dataset.update({'geography': geography, 
    'geographyId': MD['Geographies'].loc[geography, 'id']})
#start and end date by user
dataset['startDate'] = '2014-01-01'
dataset['endDate'] = '2015-12-31'
#id of the dataset from concat of 4 informations
l = [dataset['activityName'], dataset['geography'], dataset['startDate'], dataset['endDate']]
dataset['id'] = make_uuid(l)
#technology level by user
dataset['technologyLevel'] = 3
#facultative values by user
dataset['synonyms'] = ['Jurassic Park', 'waste water treatment', 'WWT']
dataset['includedActivitiesStart'] = 'Treatment of waste water, collected from dinosaur cages.'
dataset['includedActivitiesEnd'] = 'Includes the production of sludge.  '
dataset['tag'] = ['tag1', 'tag2']

#multiple comment objects, filled by user
object_type = 'TTextAndImage'
for field in ['allocationComment', 'generalComment', 'geographyComment', 
              'technologyComment', 'timePeriodComment']:
    d = {'comments_original': ['%s%s' % (field, i) for i in range(3)]}
    dataset[field] = GenericObject(d, object_type)

#administrative info
field = 'modellingAndValidation'
object_type = 'ModellingAndValidation'
#mandatory values
d = {'systemModelId': '8b738ea0-f89e-4627-8679-433616064e82', 
     'systemModelContextId': None, 
     'percent': None, 
     'systemModelName': 'Undefined', 
     'reviews': None, 
     }
#variable fields filled by user
d['samplingProcedure'] = 'sampling procedure comment here'
d['extrapolations'] = 'extrapolations comment here'
dataset[field] = GenericObject(d, object_type)

field = 'dataEntryBy'
object_type = 'DataEntryBy'
#mandatory values.  Data entry will be from the current user and active authorship will have to be accepted.
d = {'personContextId': None, 
     'isActiveAuthor': 'false', 
     'personId': '788d0176-a69c-4de0-a5d3-259866b6b100', 
     'personName': '[Current User]', 
     'personEmail': 'no@email.com'
     }
dataset[field] = GenericObject(d, object_type)

object_type = 'DataGeneratorAndPublication'
field = 'dataGeneratorAndPublication'
#mandatory values
d = {'isCopyrightProtected': 'true', 
     'accessRestrictedTo': 1, 
     'dataPublishedIn': 0}
empty_fields = ['personContextId', 'publishedSourceContextId', 'publishedSourceIdOverwrittenByChild', 
  'companyContextId', 'companyIdOverwrittenByChild', 'publishedSourceId', 'companyCode', 
  'publishedSourceYear', 'publishedSourceFirstAuthor', 'pageNumbers', 'companyId']
d.update({f: None for f in empty_fields})
#variable fields: depends on the user
d['personName'] = 'Pascal Lesage'
if d['personName'] in MD['Persons'].index:
    sel = MD['Persons'].loc[d['personName']]
    d['personId'] = sel['id']
    d['personEmail'] = sel['email']
else:
    d['personId'] =  make_uuid(d['personName'])
    d['personEmail'] = 'person_email@gmail.com'
    d['companyName'] = 'Jurassic consultant Inc.'
    #add to MD: Issue #2
    #add to userMD: Issue #2
    if d['companyName'] not in MD['Companies'].index:
        #add to MD: Issue #2
        #add to userMD: Issue #2
        pass

dataset[field] = GenericObject(d, object_type)

object_type = 'FileAttribute'
field = 'fileAttributes'
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
dataset[field] = GenericObject(d, object_type)

object_type = 'TClassification'
field = 'classifications'
#mandatory values
d = {'classificationSystem': 'ISIC rev.4 ecoinvent', 
     'classificationValue': '3700:Sewerage', 
     }
d['classificationId'] = MD['Classifications'].loc[
    (d['classificationSystem'], d['classificationValue']), 'classificationValueId']
empty_fields = ['classificationContextId']
d.update({f: None for f in empty_fields})
dataset[field] = [GenericObject(d, object_type)]

#new activity index entry for user master data
field = 'ActivityIndex'
d = {'id': dataset['id'], 
     'activityNameId': dataset['activityNameId'], 
    'geographyId': dataset['geographyId'], 
    'startDate': dataset['startDate'], 
    'endDate': dataset['endDate'], 
    'specialActivityType': dataset['specialActivityType'], 
    'systemModelId': dataset['modellingAndValidation'].systemModelId, 
    }
dataset[field] = [GenericObject(d, field)]

#filling with exchanges
#ReferenceProduct example
exc = create_empty_exchange()
exc.update({'group': 'ReferenceProduct', 
       'name': 'wastewater, from dinosaur zoo', 
       'unitName': 'm3', 
       'amount': -1., 
       'productionVolumeAmount': 20000., 
       'productionVolumeComment': 'production volume comment', 
       'comment': 'exchange comment', 
       })
properties = [#(property_name, amount, comment, uncertainty)
    ('iron content', .002, 'iron comment', {'variance': .006, 'pedigreeMatrix': [1, 2, 3, 5, 4]}), 
    ('manganese content', .001, 'manganese comment', None), 
    ('arsenic content', .004, 'arseinc comment', None), 
    ('cobalt content', .005, 'cobalt comment', None)
    ]
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
rendered = recursive_rendering(dataset, env, result_folder, result_filename)