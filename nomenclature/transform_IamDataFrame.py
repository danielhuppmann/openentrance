from pyam import IamDataFrame


def time_to_year_subannual(pyam_df):
    # generate pandas dataframe from IamDataFrame class
    pandas_df = pyam_df.as_pandas()
    
    # save time column (i.e., 2015-01-01T00:00:00+01:00) 
    # as 'year' (2015) and 'subannual' (01-01T00:00:00+01:00) column
    years=[]
    subannual=[]
    
    for index, row in pandas_df.iterrows():
        years.append(row['time'].year)
        subannual.append(str(row['time']).
                         replace(str(row['time'].year)+'-',''))
    pandas_df['year']=years
    pandas_df['subannual']=subannual
        
    # clean dataframe from invalid columns
    valid_columns = ['model', 'scenario', 'region', 
          'variable', 'unit', 'value', 'year', 'subannual']
    for c in pandas_df.columns:
        if c not in valid_columns:
            pandas_df.pop(c)
    
    return IamDataFrame(pandas_df)



    
    
    

























