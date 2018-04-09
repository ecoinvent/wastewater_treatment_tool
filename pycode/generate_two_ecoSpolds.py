import os
import sys
from pycode  import DirectDischarge_ecoSpold, WWT_ecoSpold
from pycode import defaults

def main(root_dir, **args):
    untreated = DirectDischarge_ecoSpold(root_dir, **args)
    treated = WWT_ecoSpold(root_dir, **args)
    return {
        'untreated': DirectDischarge_ecoSpold.generate_ecoSpold2(),
        'treated': WWT_ecoSpold.generate_ecoSpold2(),
    }

if __name__ == '__main__':
    os.chdir(r'..')
    root_dir = os.getcwd()
    sys.path.append(root_dir)
    main(root_dir, **args)