#!/usr/bin/env python

# Copyright 2019 David Garcia
# See LICENSE for details.

__author__ = "David Garcia <dvid@usal.es>"

import pandas as pd
from os import walk
from copy import deepcopy


def fix_month_format(element):
    """
    This function converts the abbreviation of a Spanish month into its corresponding month number.

    Args:
        element (:obj:`str`): name of the month in Spanish. Abbreviation of the first 3 letters.

    Returns:
        :obj:`str`: The function returns the corresponding number as string.
    """

    meses = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'sept': 8,
             'oct': 8, 'nov': 8, 'dic': 12}
    for word, initial in meses.items():
        element = element.replace(word, '0' + str(initial))
    return element


def fix_date_format(df_, date_format='%d %m %Y %H:%M', date_column_name='hour'):  #podría generalizarse
    """
    This function converts the data column into 'datetime' format.

    Args:
        df_ (:obj:`pandas.DataFrame`): Input dataset.
        date_format (:obj:`str`, optional): format in which the dates are embedded.
        date_column_name (:obj:`str`, optional): name of the column containing the dates.

    Returns:
        :obj:`pandas.DataFrame`: The function returns a dataframe with the date column in datetime format.
    """

    if len(df_[date_column_name][0]) == 33:
        df2 = df_[date_column_name].map(lambda x: fix_month_format(str(x)[5:-11]))
    else:
        print('ERROR: unrecognised date format.\nNo changes are applied.')
        return df_
    df2 = pd.to_datetime(df2, format=date_format)
    # cambio las columnas
    df_ = df_.drop(columns=['hour'])
    df_['date_time'] = df2
    return df_


def load_data(original_path='./concatenado', date_format='%d %m %Y %H:%M', sort_values=True, date_column_name='hour'):
    """
    This function loads information from several files and outputs a single dataset containing all the information.

    Args:
        original_path (:obj:`str`, optional): path where all the files are located.
        date_format (:obj:`str`, optional): format in which the dates are embedded.
        sort_values (:obj:`bool`, optional): sort the values by data or preserve the original order.
        date_column_name (:obj:`str`, optional): name of the column containing the dates.

    Returns:
        :obj:`pandas.DataFrame`:
            The function returns a pandas.DataFrame containing all the loaded data.
    """

    paths = next(walk(original_path))[2]
    files = [[] for _ in range(len(paths))]
    for i in range(len(paths)):
        for (dirpath, dirnames, filenames) in walk(original_path + paths[i]):
            files[i].extend(filenames)
            break
    df = pd.DataFrame()
    for file in paths:
        try:
            df_new = pd.read_csv(original_path + '/' + file, encoding='utf-8',
                                 engine='python', index_col=False)
            df = df.append([df_new], ignore_index=True)
        except Exception as e:
            print(file)
            print(e)
            continue

    df = fix_date_format(df, date_format=date_format, date_column_name=date_column_name)
    if sort_values:
        df = df.sort_values(by=['date_time']).reset_index(drop=True)
    return df


def df_house_sensor(df_, house_number, sensor):
    """
    This function extracts the information of a specific sensor in a certain house from a dataframe.

    Args:
        df_ (:obj:`pandas.DataFrame`): dataframe containing all data.
        house_number (:obj:`int`): number of the house which data is getting extracted.
        sensor (:obj:`int` or :obj:`str`): name/number of the sensor which data is getting extracted.

    Returns:
        :obj:`pandas.DataFrame`:
            The function returns a dataframe containing the data of a specific sensor in a certain house.
    """

    df_grouped = df_.groupby(['house', 'sensor'])
    df_dates = pd.DataFrame(df_grouped['date_time'].apply(list).values.tolist(), index=df_grouped.groups)
    df_weights = pd.DataFrame(df_grouped['value'].apply(list).values.tolist(), index=df_grouped.groups)

    df_dates.columns = df_dates.columns * 2
    df_weights.columns = df_weights.columns * 2 + 1

    res = pd.concat([df_dates, df_weights], axis=1).sort_index(1)

    if type(sensor) == str:
        df_one_row = res.loc[str(house_number)].T[sensor].values
    else:
        df_one_row = res.loc[str(house_number)].iloc[sensor].values
    date_time = [df_one_row[i] for i in range(len(df_one_row)) if i % 2 == 0]
    values = [df_one_row[i] for i in range(len(df_one_row)) if i % 2 == 1]

    return pd.DataFrame({'date_time': date_time, 'values': values})


def adapt_frequency(df_, new_frequency=60, start_date=None, end_date=None, time_column_name='date_time'):
    """
    This function changes the refresh frequency of a dataframe.

    Args:
        df_ (:obj:`pandas.DataFrame`): dataframes of all houses.
        new_frequency (:obj:`int`, optional): refresh frequency in minutes of the output.
        start_date (:obj:`datetime`, optional): left extreme of the selected time interval.
        end_date (:obj:`datetime`, optional): right extreme of the selected time interval.
        time_column_name (:obj:`str`, optional): name of the column containing the time information.

    Returns:
        :obj:`pandas.DataFrame`: The function returns a pandas dataframe with the selected refresh frequency.
    """

    if not start_date:
        start_date = df_.dropna().date_time[0]
    if not end_date:
        end_date = df_.dropna().date_time.values[-1]
    new_range = pd.date_range(start_date, end_date, freq=str(new_frequency) + 'min')
    df_new_range = pd.DataFrame(data=new_range, columns=[time_column_name])
    df_new_range['0'] = ''

    new_df = pd.concat([df_, df_new_range], sort=True).sort_values(by=time_column_name)
    return new_df.interpolate().dropna().drop(['0'], axis=1).set_index(time_column_name)  # PODRIA SER MULTIHILO


def get_df_house(df_, house_number, frequency=60, time_column_name='date_time'):
    """
    This function extracts the dataframe of a specific house from a general dataframe.

    Args:
        df_ (:obj:`pandas.DataFrame`): dataframes of all houses.
        house_number (:obj:`str`): number of the selected house.
        frequency (:obj:`int`, optional): refresh frequency in minutes of the output.
        time_column_name (:obj:`str`, optional): name of the column containing the time information.

    Returns:
        :obj:`pandas.DataFrame`: The function returns a pandas dataframe with all the information of the selected house.
    """

    if str(house_number) not in df_.casa.unique():
        return 'House data not available'
    sensors = df_[df_.casa == str(house_number)].sensor.unique()
    house_df = pd.DataFrame()
    start_date = df_[df_.casa == str(house_number)].dropna()[time_column_name].iloc[0]
    end_date = df_[df_.casa == str(house_number)].dropna()[time_column_name].iloc[-1]
    for sensor_ in sensors:
        sensor_df = adapt_frequency(df_house_sensor(df_, house_number, sensor_), frequency, start_date, end_date)
        sensor_df.columns = [sensor_]
        house_df = pd.concat([sensor_df, house_df], axis=1)
    return house_df.dropna()


def write_df_all_houses(df_, output_path='.//', frequency=60):
    """
    This function writes in a csv the dataframes of all houses.

    Args:
        df_ (:obj:`pandas.DataFrame`): dataframes of all houses.
        output_path (:obj:`str`, optional): relative output path.
        frequency (:obj:`int`, optional): refresh frequency in minutes of the output.

    Returns:
        :obj:`bool`: The function returns True if the operation is successful.
    """

    for house_number in df_['house'].unique():
        df_house = get_df_house(df_, house_number, frequency)
        df_house.to_csv(output_path + 'house_' + str(house_number) + '.csv')

    return True


def fix_empty_weeks(df_, column):
    """
    This function fulfills the empty gaps found in a dataset.

    Args:
        df_ (:obj:`pandas.DataFrame`): Input dataset.
        column (:obj:`int`): column's position (as number in the dataframe).

    Returns:
        :obj:`bool`: The function returns the fixed dataframe.
    """

    original_df = deepcopy(df_)

    # hago la media de la primera columna, y completo con ella
    mean = original_df['value'].mean()  # debería hacer la media o la mediana????!?

    for i in range(len(original_df.date_time) - 1):
        if abs(original_df.date_time[i].day - original_df.date_time[i + 1].day) > 1:
            start_date = original_df.date_time[i]
            end_date = original_df.date_time[i + 1]
            # escribo la media en los valores mal interpolados
            df_.loc[(df_.index > start_date) & (df_.index < end_date), column] = mean
    return df_
