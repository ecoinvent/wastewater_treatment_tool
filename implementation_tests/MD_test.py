import os


########################################################################
# Arguments
########################################################################

# Root directory, where all files and code will be found
root_dir = r'C:\mypy\code\wastewater_treatment_tool'

########################################################################
# Function
########################################################################

if __name__ is '__main__':
    os.chdir(root_dir)
    from pycode import load_MD

    load_MD(root_dir)
            
    assert os.path.isfile(os.path.join(root_dir, 'MasterData', 'MD.pkl')), "MD.pkl was not saved"
    assert os.path.isfile(os.path.join(root_dir, 'MasterData', 'xlsx', 'MasterData_fields.xlsx')), "MasterData_fields.xlsx was not saved"
    print("Test passed")