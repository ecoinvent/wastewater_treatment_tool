import os
from pickle import dump, load
import pandas as pd
import numpy as np
from copy import copy
    
    
def pkl_dump(dump_dir, obj_name, obj, feedback = False):
    '''helper function for saving files in pickle'''
    
    filename = os.path.join(dump_dir, obj_name + '.pkl')
    file = open(filename, 'wb')
    dump(obj, file)
    file.close()
    if feedback:
        print('created {} in {}'.format(obj_name + '.pkl', dump_dir))
    return None
        
def pkl_load(load_dir, obj_name):
    '''helper function for loading pickle files'''
    filename = os.path.join(load_dir, str(obj_name) + '.pkl')
    file = open(filename, 'rb')
    obj = load(file)
    file.close()
    return obj

        
def list_to_df(l, index_start = 0):
    '''Takes a list of dictionaries, makes a data frame.
       Option to start index not at zero.'''
    
    d = {i + index_start: l[i] for i in range(len(l))}
    d = pd.DataFrame(d).transpose()
    
    return d
    
def is_empty(e):
    '''Checks if "e" is of certain values that usually mean that no info is available'''
    
    if type(e) in [float, np.float, np.float64, np.float16, np.float32, np.float_]:
        test = e in [np.nan, np.NaN] or np.isnan(e)
    else:
        test = e in ['', None, [], set(), dict()]
    
    return test
    
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
    
    
def dataframe_to_excel(folder, filename, dfs, read_me=False, feedback=False):
    '''function to take care of aggregating sheets, freeze pane and meta info'''
    
    writer = pd.ExcelWriter(os.path.join(folder, filename), engine='xlsxwriter')
    
    #maybe a read me sheet
    if read_me:
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
        assert type(df) in [type(pd.DataFrame()), list]
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
    
def add_path_in_list(l, path):
    return [os.path.join(path, filename) for filename in l]
