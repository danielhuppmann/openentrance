import pandas as pd
from pyam import IamDataFrame
from nomenclature import validate


TEST_DF = pd.DataFrame([
    ['model_a', 'scen_a', 'Europe', 'Primary Energy', 'EJ/yr', 1, 6.],
],
    columns=['model', 'scenario', 'region', 'variable', 'unit', 2005, 2010]
)


df = IamDataFrame(TEST_DF)



def test_validate():
    # test simple validation
    assert validate(df)


def test_validate_fail():
    # test that simple validation fails on variable and region dimension
    assert not (validate(df.rename(variable={'Primary Energy': 'foo'})))
    assert not (validate(df.rename(region={'Europe': 'foo'})))


def test_validate_directional():
    # test that validation works as expected with directional data
    assert validate(df.rename(region={'Europe': 'Austria>Germany'}))
    assert not validate(df.rename(region={'Europe': 'Austria>foo'}))

    # test that directional data with more than one `>` fails
    assert not validate(df.rename(region={'Europe': 'Austria>Italy>France'}))


def test_validate_subannual():
    # test that validation works as expected with sub-annual column (wide format)
    DF = pd.DataFrame(["subannual"], columns=['01-01T00:00+01:00'])
    df_test = IamDataFrame(DF)
    df_test = df_test.append(df)
    assert validate(df)
    assert not validate(df.rename(subannual={'01-01T00:00+01:00':'01-01T00:00+02:00'}))
    assert not validate(df.rename(subannual={'01-01T00:00+01:00':'01-01T00:00+02:00'}))
    assert not validate(df.rename(subannual={'01-01T00:00+02:00':'20-01T0000+02:00'}))


def test_validate_time():
    # test that validation works as expected with 'time' column (long format)
    DF = pd.DataFrame(["time"], columns=['2020-01-01T00:00+01:00'])
    df_test = IamDataFrame(DF)
    df = df.append(df_test)
    assert not validate(df)
    assert not validate(df.rename(time={'2020-01-01T00:00+01:00':'2020-01-01T00:00+02:00'}))
    assert validate(df.rename(time={'2020-01-01T00:00+02:00':'2020-01-01T00:00+01:00'}))
    



