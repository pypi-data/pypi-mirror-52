
"""
[TITLE]
Author: Mei Yong
Updated Date: Sat Sep 21 15:28:52 2019

"""


"""
import pandas as pd
df = pd.read_csv(r"C:\Users\shaom\Desktop\Machine_Learning\House_Prices\train.csv")


### If column is a date column, convert it to datetime format
for column in sfPermitsClean:
    if 'date' in column:
        sfPermitsClean[column] = pd.to_datetime(sfPermitsClean[column], errors='coerce')
        
        ### Formatting datetime
import datetime
ex_date_1 = "01-03-2019"
ex_date_2 = datetime.datetime.strptime(ex_date_1, "%d-%m-%Y")






# Number of distinct categorical values
#    dictinct_val_dict = {column: df[column].value_counts().count() \
                         for column in df if df[column].dtype in ['object'] }
    
    
"""
"""
        Regex Cheatsheet
        https://www.rexegg.com/regex-quickstart.html
        Regex Basics
        https://www.w3schools.com/python/python_regex.asp
        Re Documentation
        https://docs.python.org/3/library/re.html
        Regex Stackoverflow example
        https://stackoverflow.com/questions/11171045/python-regular-expression-example
        """
        
        """
        
        ### Analyse each cell value and label as either a string, numeric then count up the groups
        col = df['accounts_lastmadeupdate']
        
        
        ### Warning should be string/numeric
        
        ### Remove NaNs
        col.dropna(inplace=True)
        
        ### Convert to strings
        col = col.astype(str)
        
        ### Regex to check and label if numeric or string
        import re
        for value in col:
            x = re.search(r"(\d+)", col)
        
        test = re.search(r"(\d+)", '14274')
        print(test.groups()[0])
        
        
        test = re.match(r"\d+", '14274')
        
        ### Count up the labels and group
        
        ### If more than 1 group, output 'Warning: Mixed types {'string':10%, 'numeric':90%}
        
        ### Note the most commonly occuring label
        
        ### If most values look like numerics BUT the auto-detected type is string, then warning should be numeric
        
        ### If most values look like strings BUT the auto-detected type is numeric, then warning should be string (this will likely never be triggered)
        
        
        
        
        
        
                
        ### ID check
        ### Check for sequential score
        ### Check for repeated value score - mask then group then average where zero is means more repeated values and one means less repeated values and closer to zero is more likely to be an ID
        ### Check for Benford's law - basically if the values start with the same number or set of numbers
            
        ### y/n check
        ### Convert to string (keep the NaNs)
        ### Check for common y/n values
            
        ### Date check
        ### Remove NaNs
        ### Convert to string
        ### Check regex and label
        ### Count up the labels
        ### If >60% date then date warning

"""
        