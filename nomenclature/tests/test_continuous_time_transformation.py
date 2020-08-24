import pandas as pd
from pyam import IamDataFrame
from nomenclature import time_to_year_subannual
from nomenclature import validate
import pyam as pyam


TEST_DF = pd.DataFrame([
    ['model_a', 'scen_a', 'Europe', 'Primary Energy', 'EJ/yr',
     '2015-01-01T00:00:00+01:00', 11231.088],
],
    columns=['model', 'scenario', 'region',
             'variable', 'unit', 'time', 'value'])
df = IamDataFrame(TEST_DF)


def test_transformation_IamDataFrame():
    # test transformation (cast) from IamDataFrame
    to_test = time_to_year_subannual(df).as_pandas()
    assert (to_test['year'][0]==2015 and to_test['subannual'][0]=='01-01 00:00:00+01:00')

def test_subannual_entry():
    assert validate(df)




