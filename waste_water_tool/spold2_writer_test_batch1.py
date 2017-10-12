""" 
WWT-ecoinvent - Batch 1 of functions for generating ecoSPold files

Covers:
    - Getting master data dictionary (MD), required at multiple places
    - empty dataset creation
    - creation of Activity Index
"""

"""
4
Get master data dictionary (MD), required at different points in the code.
MD is a dictionary, with values = Pandas dataframes.
"""
MD = get_current_MD(return_MD=True)

"""
6.1
Create the empty dataset
    - Function: create_empty_dataset
    - Arguments: None
    - Pending points:
        - DataGeneratorAndPublication section should refer to model author (i.e. you)
"""
treatment_dataset = create_empty_dataset()

"""
6.2.1
Add name to dataset
    - Function: generate_WWT_activity_name
    - Arguments:
        - dataset: dataset created above to which we are appending the name
        - WW_type: source of the wastewater. From tool. Allowed values: from X production, OR average.
        - technology: specific technology, or "average". From tool.
        - capacity: in liters per year (e.g. 5e9). From tool.
    User inputs:
        - WW_type (str)
        - technology (str, from drop-down)
        - capacity: float, from drop-down
        
"""
WW_type = "from steel production" #from tool
technology = "average" #from tool
capacity = 5e9 #from tool

treatment_dataset = generate_WWT_activity_name(treatment_dataset, WW_type, technology, capacity)

"""
6.2.2
Add ID to dataset
Use ActivityNameID if the activity name already exists, else generate a new ActivityNameID.
    - Function: generate_activityNameId
    - Arguments: dataset, MD
    - User input: None
"""
generate_activityNameId(treatment_dataset, MD)

"""
6.2.3
Add geography for dataset
    - Function: generate_geography
    - Arguments:
        - dataset
        - MD
        - Geography short name.
    - User input:
        - Geography
            - Note that the user should probably provide the LONG name. 
              Therefore, a long_name:short_name dictionary is required 
              (or function could be changed to use long name as argument)
            - The user should specify the geography from a dropdown list.
            - The dropdown list should be based on the masterdata
"""
geography = "GLO" #from tool. Short name. Change to long name?
generate_geography(treatment_dataset, MD, geography)

"""
6.2.4
TimePeriod
Used to specify the period for which the dataset is valid.
Date format: YYYY-MM-DD
To be discussed: User input could be simplified, asking only for years and filling in day and months ourselves.
    - Function: generate_time_period
    - Arguments:
        - dataset
        - start: YYYY-MM-DD
        - end: YYYY-MM-DD
    - User input: 
        - Start, end. 
        - Possibly simplify by asking only years. 
        - Use dropdown or calendar to minimize mistakes?
"""
start_date = '1995-01-31'
end_date= '2020-12-31'
generate_time_period(treatment_dataset, start=start_date, end=end_date)

"""
6.2.5
Dataset ID
    - Function: generate_dataset_id
    - Argument: dataset
    - User input: None
"""
generate_dataset_id(treatment_dataset)

"""
6.2.6
Adding all index values to dataset:
    - Function: generate_activityIndex
    - Arguments: dataset
    - User input: None
"""
generate_activityIndex(treatment_dataset)