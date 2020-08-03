from pathlib import Path
import logging
import yaml
from pyam import IamDataFrame
from datetime import datetime

# set up logging formatting
logger = logging.getLogger(__name__)
stderr_info_handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
stderr_info_handler.setFormatter(formatter)
logger.addHandler(stderr_info_handler)


# path to nomenclature definitions
DEF_PATH = Path(__file__).parent / 'definitions'


def _parse_yaml(path, file='**/*', ext='.yaml'):
    """Parse `file` in `path` (or all files in subfolders if `file='**/*'`)"""
    dct = {}
    for f in path.glob(f'{file}{ext}'):
        with open(f, 'r', encoding='utf-8') as stream:
            _dct = yaml.safe_load(stream)
            # add `file` attribute to each element in the dictionary
            for key, value in _dct.items():
                value['file'] = str(f)
            dct.update(_dct)
    return dct


variables = _parse_yaml(DEF_PATH / 'variable')
"""Dictionary of variables"""


regions = _parse_yaml(DEF_PATH / 'region')
"""Dictionary of all regions"""


countries = _parse_yaml(DEF_PATH / 'region', 'countries')
"""Dictionary of countries"""


iso_mapping = dict(
    [(countries[c]['iso3'], c) for c in countries]
    + [(countries[c]['iso2'], c) for c in countries]
    # add alternative iso2 codes used by the European Commission to the mapping
    + [(countries[c]['iso2_alt'], c) for c in countries
       if 'iso2_alt' in countries[c]]
)
"""Dictionary of iso2/iso3/alternative-iso2 codes to country names"""


def _add_to(mapping, key, value):
    """Add key-value to mapping"""
    if key not in mapping:
        mapping[key] = value
    elif isinstance(value, list):
        mapping[key] += value
    return mapping[key]


def _create_nuts3_hierarchy():
    """Parse nuts3.yaml and create hierarchical dictionary"""
    hierarchy = dict()
    keys = ['country', 'nuts1', 'nuts2']
    for n3, mapping in _parse_yaml(DEF_PATH / 'region', 'nuts3').items():
        country, n1, n2 = [mapping.get(i) for i in keys]
        country_dict = _add_to(hierarchy, country, {n1: dict()})
        n1_dict = _add_to(country_dict, n1, {n2: list()})
        _add_to(n1_dict, n2, [n3])
    return hierarchy


nuts_hierarchy = _create_nuts3_hierarchy()
"""Hierarchical dictionary of nuts region classification"""


subannual = _parse_yaml(DEF_PATH / 'subannual')
"""Dictionary of subannual timeslices"""


def validate(df):
    """Validate that all columns of a dataframe follow the nomenclature

    Parameters
    ----------
    df : path to file, pandas.DataFrame, pyam.IamDataFrame (or castable object)
        A timeseries dataframe following the common data format

    Returns
    -------
    bool
        Return `True` if all column entries in `df` are valid
        or `False` otherwise
    """
    if not isinstance(df, IamDataFrame):
        df = IamDataFrame(df)
    success = True

    # set up list of dimension (columns) to validate (`subannual` is optional)
    cols = [
        ('region', regions, 's'),
        ('variable', variables, 's')
    ]

    # add 'subannual' (wide format) or 'time' (long format) to list to validate
    if 'subannual' in df.data.columns:
        cols.append(('subannual', subannual, ' timeslices'))
        # get (one) year from columns to validate datetime
        year = df.data.year[0]
    elif 'time' in df.data.columns:
        cols.append(('time', time, 'timeslices'))



    # iterate over dimensions and perform validation
    msg = 'The following {} are not defined in the nomenclature:\n    {}'
    for col, codelist, ext in cols:
        invalid = [c for c in df.data[col].unique() if c not in codelist]

        # check the entries in the invalid list related to directional data
        if col == 'region':
            invalid = [i for i in invalid if not _validate_directional(i)]

        if col == 'subannual':
            invalid = [c for c in df.data[col] if not _get_timestamp_for_subannual(c, year)]

        if col == 'time':
            invalid = [c for c in df.data[col] if not _validate_time_column(c)]

        # check if any entries in the column are invalid and write to log
        if invalid:
            success = False
            logger.warning(msg.format(col + ext, invalid))

    return success


def _validate_directional(x):
    """Utility function to check whether region-to-region code is valid"""
    x = x.split('>')
    return len(x) == 2 and all([i in regions for i in x])

def _get_timestamp_for_subannual(a, year):
    try:
        month = a[0:2]
        a = a.split('-')[1]
        day = a[0:2]
        if 'T' in a:
            timestamp = a.split('T')[1].split('+')[0]
            hour = timestamp.split(':')[0]
            minute = timestamp.split(':')[1]
            second = 0
            if timestamp.count(':') == 2:
                second = timestamp.split(':')[2]
        else:
            hour = minute = second = 0

        if '+' + a.split('+')[1] == '+01:00':
            ts = datetime(int(year), int(month), int(day), int(hour),
                          int(minute), int(second))
            return isinstance(ts, datetime)
        else:
            return False
    except Exception:
        return False

def _validate_time_column(timestamp):
    return isinstance(timestamp, datetime)


