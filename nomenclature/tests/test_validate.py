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
    assert validate(df.insert("subannual", ['01-01T00:00+01:00'], True))
    assert not validate(df.insert("subannual", ['01-01T00:00+02:00'], True))
    assert not validate(df.insert("subannual", ['20-01T00:00+02:00'], True))
    assert not validate(df.insert("subannual", ['20-01T0000+02:00'], True))


def test_validate_time():
    # test that validation works as expected with 'time' column (long format)
    assert validate(df.insert("time", ['2020-01-01T00:00+01:00'], True))
    assert not validate(df.insert("time", ['0-01-01T00:00+02:00'], True))
    assert not validate(df.insert("time", ['2020-01-01T00:00+02:00'], True))



