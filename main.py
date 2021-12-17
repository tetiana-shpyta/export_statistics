from datetime import datetime as dt
import requests
import pandas as pd
import data_preparation
import filtration


CURRENT_YEAR = dt.today().year
PREV_YEAR = CURRENT_YEAR - 1
EXCLUDED_MONTH = 1
COLS_TO_SAVE = ['State', 'HS Code 2',
                'Year', 'Month', 'Export']
COLS_TYPES = {'Export': 'float',
              'HS Code 2': 'int',
              'HS Code 4 slice': 'int'}
EXPORT_FLOAT = 'Export float'
HS_CODES_DICT = {'HS Code 2 int': {'агропромислова продукція': list(range(1, 25)),
                                   'мінеральна продукція': [25, 26, 27],
                                   'машинобудування': list(range(83, 91)),
                                   'меблі': [94],
                                   'фарма': [30],
                                   'одяг і взуття': [61, 62, 64, 65],
                                   'хімікати': list(range(28, 39))
                                   },
                 'HS Code 4 slice int': {'кондитерська продукція': [1704, 1806, 1905],
                                         'косметика': list(range(3302, 3309)) + [3401]
                                         },
                 'HS Code 6 int': {}}
BIL_USD = 1000000000


def read_from_url_to_df(url):
    """
    Getting data from the given url, splitting response text by '\r\n'
    and separating column names and data to create df.

    Args:
        url (str): web address to get data from.

    Returns:
        DataFrame.

    """
    response = requests.get(url)
    replaced = response.text.replace(', ', '')
    splitted = replaced.split('\r\n')
    del splitted[-1]  # empty string
    splitted_cols = [string.split(',') for string in splitted]
    splitted_cols_names = splitted_cols[0]  # EMPTY
    del splitted_cols[0]

    df = pd.DataFrame(data=splitted_cols, columns=splitted_cols_names)
    return df


def get_year_results(data, year):
    """
    Creating empty lists, calculating sum of export for every industry,
    adding to empty lists, creating df

    Args:
        data (dict): {sources: df}
        year :

    Returns:
        DataFrame

    """
    result_index_names = list()
    result_export_sum = list()
    for name, corr_df in data.items():
        export_sum = corr_df[EXPORT_FLOAT].sum() / BIL_USD
        result_index_names.append(name)
        result_export_sum.append(export_sum)
    export_df = pd.DataFrame({year: result_export_sum},
                             index=result_index_names)
    return export_df


def year_calculations(url, year):
    """
    Getting ready df from url, cleaning and preparing it,
    using filters to calculate every industry sum of export,
    creating df

    Args:
        url: web address to get data from
        year:

    Returns:
        DataFrame

    """
    read_df = read_from_url_to_df(url)
    clean_df = data_preparation.df_dropping(read_df, COLS_TO_SAVE.copy())
    prepared_df = data_preparation.typify_col(clean_df, COLS_TYPES)

    result_dfs_dict = filtration.complete_dfs(prepared_df, HS_CODES_DICT)
    result_dfs_dict['загальний'] = prepared_df

    export_year_df = get_year_results(result_dfs_dict, year)
    return export_year_df


def calculate_delta(curr_year_df, prev_year_df):
    """
    Joining df with current and previous year results,
    calculating delta: dividing current year result by the result of previous year,
    minus 1, multiplying by 100,
    dropping df with previous year results

    Args:
        curr_year_df:
        prev_year_df:

    Returns:
        DataFrame


    """
    two_years_df = curr_year_df.join(prev_year_df, how='inner')
    two_years_df['delta (%)'] = ((two_years_df[CURRENT_YEAR]
                                  / two_years_df[PREV_YEAR]) - 1) * 100
    temp_df = two_years_df.rename(columns={CURRENT_YEAR:
                                               f'{CURRENT_YEAR} (млрд USD)'})
    delta_df = temp_df.drop(PREV_YEAR, axis=1)
    return delta_df


if __name__ == '__main__':


    print('Hello! Let\'s start!')
    months_quantity = int(input('Please, input number of months: ')) + EXCLUDED_MONTH

    curr_url = ('https://open-api.customs.gov.ua/api/external_trade_data/EN'
                f'?dateRange=01.{CURRENT_YEAR}-{months_quantity}.{CURRENT_YEAR}'
                '&currency=USD&timeInterval=month&groupBy=state%2CUKTZED2%2CUKTZED4'
                '&indicators=export')
    prev_year_url = ('https://open-api.customs.gov.ua/api/external_trade_data/EN'
                     f'?dateRange=01.{PREV_YEAR}-{months_quantity}.{PREV_YEAR}'
                     '&currency=USD&timeInterval=month&groupBy=state'
                     '%2CUKTZED2%2CUKTZED4&indicators=export')

    curr_year_result_df = year_calculations(curr_url, CURRENT_YEAR)
    prev_year_result_df = year_calculations(prev_year_url, PREV_YEAR)

    result_df = calculate_delta(curr_year_result_df, prev_year_result_df)
    print(result_df)
