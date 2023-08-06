
"""
Hello Atlas
* Data profiling

Author: Mei Yong
Updated date: 2019-09-21


	WIP Ideas
    * Distinct values
	* YesNo
	* Categorical
	* Mixed types based on regex
	* ID check
		- sequential score
		- Check for repeated value score - mask then group then average where zero is means more repeated values and one means less repeated values and closer to zero is more likely to be an ID
		-Check for Benford's law - basically if the values start with the same number or set of numbers
     * y/n check
        - Convert to string (keep the NaNs)
        - Check for common y/n values
	* Date check
        - Remove NaNs
        - Convert to string
        - Check regex and label
        - Count up the labels
        - If >60% date then date warning
	* Treat dates
		- split into year, month, day
		- days between current date and column date
		- convert to weekday, weekend, holidays
	* If high cardinality, check if can bucket smaller cats into other
	* Skew & should be log. must be positive. can add 1 to data to positive
	* If column should be split/pivoted
	* Only few different numbers which are actually categories
	* Treatments for time series data


"""

# Simple function for testing package installation and function calling
def say_hello(name):
	print(f"Hello {name}")
	
################################################################################


# Function that profiles a df
def df_profiling(df, nulls_threshold=50.0, zeroes_threshold=50.0, cardinality_threshold=50.0):
    '''
    Input(s):
        1) df - dataframe to analyse
        2) nulls_threshold - int - default 50. Adds warning if >50% nulls
        3) zeroes_threshold - int - default 50. Adds warning if >50% zeroes for numerical dtype columns
        4) cardinality_threshold - int - default 50. Adds warning if >50% nulls for categorical dtype columns
    Output(s):
        1) Dataframe with statistics and data quality warnings about the input df
    '''

    import pandas as pd
    import numpy as np
    
    rowcount = df.shape[0]
    
    # Datatype
    dtype_dict = {column : df[column].dtype.name for column in df}
    
    # Number of not-nulls
    count_dict = {column : df[column].count() for column in df}
    
    # Number of nulls
    null_dict_n = {column : df[column].isnull().sum() for column in df}
    
    # Percentage of nulls
    null_dict_p = {column : round(df[column].isnull().sum() / rowcount * 100, 2) for column in df}
    
    # Number of distinct categorical values
    dictinct_val_dict = {column: df[column].value_counts().count() \
                         for column in df if df[column].dtype in ['object'] }
    
    # Percentage of distinct categorical values
    cardinality_dict = {column: round(df[column].value_counts().count() / rowcount * 100 , 2) \
                         for column in df if df[column].dtype in ['object'] }
    
    # Number of zeroes
    zeroes_dict_n = {column : (df[column]==0).sum() \
                         for column in df if df[column].dtype in ['int64','float64'] }
    # Percentage of zeroes
    zeroes_dict_p = {column : round((df[column]==0).sum() / rowcount * 100, 2) \
                         for column in df if df[column].dtype in ['int64','float64'] }
    
    # Mean numerical value
    mean_dict = {column : df[column].mean() \
                         for column in df if df[column].dtype in ['int64','float64'] }
    
    # Min numerical value
    min_dict = {column : df[column].min() \
                         for column in df if df[column].dtype in ['int64','float64'] }
    
    # Quartile 1 - 25%
    q1_dict = {column : np.percentile(df[column], 25) \
                         for column in df if df[column].dtype in ['int64','float64'] }
    # Quartile 2 - 50%
    q2_dict = {column : np.percentile(df[column], 50) \
                         for column in df if df[column].dtype in ['int64','float64'] }
    # Quartile 3 - 75%
    q3_dict = {column : np.percentile(df[column], 75) \
                         for column in df if df[column].dtype in ['int64','float64'] }
    
    # Max numerical value
    max_dict = {column : df[column].max() \
                         for column in df if df[column].dtype in ['int64','float64'] }
    
    # Outliers
    
    
    # DQ Warnings
    warning_null_dict = {key: 1 for key,value in null_dict_p.items() if value >= nulls_threshold }
    warning_zeroes_dict = {key: 1 for key,value in zeroes_dict_p.items() if value >= zeroes_threshold }
    warning_cardinality_dict = {key: 1 for key,value in cardinality_dict.items() if value >= cardinality_threshold }
    warning_one_distinct_dict = {key: 1 for key,value in dictinct_val_dict.items() if value == 1 }
    
    warning_df = pd.DataFrame([
                                warning_null_dict
                                ,warning_zeroes_dict
                                ,warning_cardinality_dict
                                ,warning_one_distinct_dict
                                ]
                                , index = ['Nulls','Zeroes','Cardinality','Only_1_distinct']   
                                )
    
    final_warnings_list = []
    for column in warning_df:
        column_warnings = []
        if warning_df.loc['Nulls' , column] == 1:
            column_warnings.append('High_null_percentage')
        if warning_df.loc['Zeroes' , column] == 1:
            column_warnings.append('High_zeroes_percentage')
        if warning_df.loc['Cardinality' , column] == 1:
            column_warnings.append('High_cardinality')
        if warning_df.loc['Only_1_distinct' , column] == 1:
            column_warnings.append('Only_1_unique_value')
        final_warnings_list.append(column_warnings)
        
    final_warnings_dict = dict(zip(warning_df.columns , final_warnings_list))
            
            
    
    df_profile = pd.DataFrame([
                        dtype_dict
                        ,count_dict
                        ,null_dict_n
                        ,null_dict_p
                        ,dictinct_val_dict
                        ,cardinality_dict
                        ,zeroes_dict_n
                        ,zeroes_dict_p
                        ,mean_dict
                        ,min_dict
                        ,q1_dict
                        ,q2_dict
                        ,q3_dict
                        ,max_dict
                        #outliers
                        ,final_warnings_dict
                        ]
                        , index = ['Dtype','Count','Null(n)','Null(p)','Distinct_Values','Cardinality',
                                   'Zeroes(n)','Zeroes(p)','Mean','Min','Q1','Q2','Q3','Max','DQ_Warnings']       
                        )
    
    return df_profile


###################################################################################################

### To enable this module to be called from another Python file
    
if __name__ == '__main__':
    say_hello()
    df_profiling()


