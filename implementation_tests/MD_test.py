import os
import sys 

os.chdir(r'..')
root_dir = os.getcwd()
sys.path.append(root_dir)

from pycode import load_MD

load_MD(root_dir)
        
assert os.path.isfile(os.path.join(root_dir, 'MasterData', 'MD.pkl')), "MD.pkl was not saved"
assert os.path.isfile(os.path.join(root_dir, 'MasterData', 'xlsx', 'MasterData_fields.xlsx')), "MasterData_fields.xlsx was not saved"
print("Test passed")