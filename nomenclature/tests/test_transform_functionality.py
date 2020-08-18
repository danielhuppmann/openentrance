import pandas as pd
from pyam import IamDataFrame
from nomenclature import swap_time_for_subannual


TEST_DF = pd.DataFrame([
    ['model_a', 'scen_a', 'Europe', 'Primary Energy', 'EJ/yr', 
     '2015-01-01T00:00:00+01:00', 11231.088],
],
    columns=['model', 'scenario', 'region', 
             'variable', 'unit', 'time', 'value'])
df = IamDataFrame(TEST_DF)


def test_swap_time_for_subannual():
    # test transforming of IamDataFrame in datetime domain to year + subannual
    obs = swap_time_for_subannual(df)
    assert (obs['year'][0] == 2015 and obs['subannual'][0] == '01-01T00:00+0100')



