import pandas as pd
from pyam import IamDataFrame
from transform_IamDataFrame import time_to_year_subannual


TEST_DF = pd.DataFrame([
    ['model_a', 'scen_a', 'Europe', 'Primary Energy', 'EJ/yr', 
     '2015-01-01T00:00+01:00', 11231.088],
],
    columns=['model', 'scenario', 'region', 
             'variable', 'unit', 'time', 'value'])
df = IamDataFrame(TEST_DF)


def test_transformation_IamDataFrame():
    # test transformation (cast) from IamDataFrame
    assert (time_to_year_subannual['year'] == 2015 
            and time_to_year_subannual['subannual'] == '01-01T00:00+01:00')



