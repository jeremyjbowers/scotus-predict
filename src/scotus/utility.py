''''
@author Michael J Bommarito II; michael@bommaritollc.com
@date 20140430

Utility methods for transforming/parsing features or outputs.
'''

# Imports
import dateutil
import numpy
import pandas

# SCOTUS imports
from scotus.constants import *

# Now load justice feature data
justice_metadata = pandas.DataFrame.from_csv('data/justice_list.csv')
justice_metadata.columns = ['justice', 'justiceName', 'gender', 'year_of_birth', 'party_president', 'segal_cover']

"""
Utility methods
"""
def get_date(x):
    try:
        return dateutil.parser.parse(str(x)).date()
    except:
        return None

def get_month(x):
    try:
        return x.month
    except:
        return None

def get_gender(justice):
    return justice_metadata[justice_metadata['justice'] == justice]['gender'][0]

def get_year_of_birth(justice):
    return justice_metadata[justice_metadata['justice'] == justice]['year_of_birth'][0]

def get_party_president(justice):
    return justice_metadata[justice_metadata['justice'] == justice]['party_president'][0]

def get_segal_cover(justice):
    return justice_metadata[justice_metadata['justice'] == justice]['segal_cover'][0]

def map_party(value):
    if value in party_map_data:
        return party_map_data[value]
    else:
        return None

def map_circuit(value):
    if value in court_circuit_map:
        return court_circuit_map[value]
    else:
        return None

def get_year_from_docket(docket):
    return int(docket.split('-')[0])

def get_justice_name(justice):
    if justice in justice_name_map:
        return justice_name_map[justice]
    else:
        return None


"""
Data slicing methods.
"""
def get_data_before_term(term, data):
    term_index = data['term'] < term
    return data[term_index].copy()

def get_data_through_term(term, data):
    term_index = data['term'] <= term
    return data[term_index].copy()

def get_data_before_date(date, data):
    date_index = data['dateDecision'] <= date
    return data[date_index].copy()

def get_data_through_date(date, data):
    date_index = data['dateDecision'] <= date
    return data[date_index].copy()

def get_data_by_condition(value, column, data):
    return data.ix[data[column] == value].copy()

def get_means(data, column, label, windows=[None], include_std=False, include_count=False):
    direction_data = {}

    # Iterate over all windows
    for window in windows:
        if window == None:
            direction_data['{0}_mean'.format(label)] = data[column].shift(1).mean()

            if include_std:
                direction_data['{0}_std'.format(label)] = data[column].shift(1).std()

        else:
            try:
                direction_data['{0}_mean_{1}'.format(label, window)] = pandas.rolling_mean(data[column].shift(1), window).tail(1).tolist().pop()
            except:
                direction_data['{0}_mean_{1}'.format(label, window)] = numpy.nan

            if include_std:
                try:
                    direction_data['{0}_std_{1}'.format(label, window)] = pandas.rolling_std(data[column].shift(1), window).tail(1).tolist().pop()
                except:
                    direction_data['{0}_std_{1}'.format(label, window)] = numpy.nan

    if include_count:
        direction_data['{0}_count'.format(label)] = data.shape[0]

    return direction_data