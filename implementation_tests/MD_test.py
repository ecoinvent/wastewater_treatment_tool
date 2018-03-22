import os


########################################################################
# Arguments
########################################################################

# Root directory, where all files and code will be found
root_dir = r'C:\mypy\code\wastewater_treatment_tool'

# Location where the pickled master data dict (MD) is stored. 
# If it doesn't exist, it will be generated.
MD_pkl_dir = os.path.join(root_dir, 'MasterData')

# Location of directory with master data xml files
MD_xlm_dir = os.path.join(root_dir, 'MasterData', 'XML')

# Location of file "MasterData_fields.xlsx"
MD_fields_xls = os.path.join(root_dir, 'MasterData', 'xlsx', 'MasterData_fields.xlsx')

# Optional, filepath to where an Excel version of the dictionary will be dumped
# Not used by tool, but can be useful to humans during development
MD_xls_dump_dir=os.path.join(root_dir, 'MasterData', 'xlsx')

# Temporary, switch to false for now to avoid being returned an object
# the javascript will not be able to understand
return_MD=False


########################################################################
# Function
########################################################################

if __name__ is '__main__':
    os.chdir(root_dir)
    from pycode import load_MD

    load_MD(MD_pkl_dir, MD_xlm_dir, MD_fields_xls, 
            MD_xls_dump_dir, return_MD=False)
            
    assert os.path.isfile(os.path.join(MD_pkl_dir, 'MD.pkl')), "MD.pkl was not saved"
    assert os.path.isfile(os.path.join(MD_xls_dump_dir, 'MasterData_fields.xlsx')), "MasterData_fields.xlsx was not saved"
    print("Test passed")