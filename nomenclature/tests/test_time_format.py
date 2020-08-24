import pandas as pd
import pyam as pyam 
from nomenclature import validate
from pyam import IamDataFrame


TEST_DF = pd.DataFrame([
    ['model_a', 'scen_a', 'EU27', 'Primary Energy', 'EJ/yr', 1, 6.],
    ['model_a', 'scen_a', 'EU27', 'Primary Energy|Coal', 'EJ/yr', 0.5, 3],
    ['model_a', 'scen_b', 'EU27', 'Primary Energy', 'EJ/yr', 2, 7],
],
    columns=pyam.IAMC_IDX + ['2005-06-17 00:00:00', '2010-07-21 12:00:00'],
)

def test_time_column():
    assert not validate(IamDataFrame(TEST_DF))

