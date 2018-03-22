# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import uuid
import numpy as np
import pandas as pd
from lxml import objectify
from copy import copy
from pickle import dump, load
from .ecoSpold_utils import pkl_dump


class WWecoSpoldGenerator:
    """ Class to organize all the data and functions associated with ecoSpold generation.
    
    Is instantiated with data passed from the javascript wastewater treatment tool.
    """
    
    def __init__(self, MD_pickle_fp, *kwargs):
        pass

        

class DirectDischargeEcoSold(WWecoSpoldGenerator):
    def __init__(self):
        pass
        
if __name__ == '__main__':
    my_MD_dir = r'C:\Users\Pascal Lesage\Documents\ecoinvent\EcoEditor\xml\MasterData\Production'
    wwgen = WWecoSpoldGenerator(MD_dir=my_MD_dir)
    print(wwgen.MD_dir)
    