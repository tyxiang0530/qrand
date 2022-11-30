# %%
from distutils.command.clean import clean
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from matplotlib.ticker import MultipleLocator

# %%
def clean_csv(csv_in):
    """cleans up the raw input from the CCD and parses out the settings

    Args:
        csv_in (string): the path to your data file

    Returns:
        pandas df, dictionary: your cleaned data and the settings in a dictionary
    """
    settings_df = pd.read_csv(csv_in, nrows = 2, header=None)
    settings_arr = settings_df.to_numpy()
    settings_dict = {}
    for setting_list in settings_arr:
        setting = setting_list[0]
        if 'SAMPLE INTEGRATION' in setting.upper():
            key = 'sample integration time (s)'
            value = float(setting.split(": ")[-1])
            settings_dict[key] = value
        elif 'CLOCK' in setting.upper():
            key = 'clock rate (hz)'
            value = float(setting.split(": ")[-1])
            settings_dict[key] = value
            
    data_df = pd.read_csv(csv_in, skiprows = 3)
    data_df = data_df.drop(['Ch 6', 'Ch 7', 'Ch 8'], axis = 1)
    data_df['Entry number'] = data_df['Entry number'] * settings_dict['sample integration time (s)']
    
    data_df.to_csv(csv_in.split('.cs')[0] + '_clean.csv', index = False)
    
    return data_df, settings_dict

# %%
def format_for_tests(clean_data, format_string, rand_type, output_loc, poiss_mid = 0, poiss_string = None):
    # format 1: 3 channel: 7 bits:
    # channel 1, 2, 3: 000, 001, 010
    # channel 1 + 2: 011
    # channel 2 + 3: 100
    # channel 1 + 3: 101
    # channel 1 + 2 + 3: 110
    
    # format 2: 2 channel
    # channel 1, 2: 00, 01
    # channel 1 + 2, 10
    
    # format 3: 2 channel, if there is coincidence, remove the trial
    # channel 1: 1
    # channel 2: 0
    # if channel 1 + 3 or channel 2 + 3: kill
    write_arr = []
    if rand_type.lower() == 'bs':
        if format_string == '3':
            for index, row in clean_data.iterrows():
                if row['Ch 1'] > 0 and row['Ch 2'] == 0 and row['Ch 3'] == 0:
                    write_arr.append("000")
                elif row['Ch 1'] == 0 and row['Ch 2'] > 0 and row['Ch 3'] == 0:
                    write_arr.append("001")
                elif row['Ch 1'] == 0 and row['Ch 2'] > 0 and row['Ch 3'] == 0:
                    write_arr.append("010")
                elif row['Ch 1'] > 0 and row['Ch 2'] > 0 and row['Ch 3'] == 0:
                    write_arr.append("011")
                elif row['Ch 1'] == 0 and row['Ch 2'] > 0 and row['Ch 3'] > 0:
                    write_arr.append("100")
                elif row['Ch 1'] > 0 and row['Ch 2'] == 0 and row['Ch 3'] > 0:
                    write_arr.append("101")
                else:
                    write_arr.append("110")
                    
        if format_string == '2':
            for index, row in clean_data.iterrows():
                if row['Ch 1'] > 0 and row['Ch 2'] == 0:
                    write_arr.append("00")
                elif row['Ch 1'] == 0 and row['Ch 2'] > 0:
                    write_arr.append("01")
                else:
                    write_arr.append("10")
                    
        if format_string == 'coincidence':
            for index, row in clean_data.iterrows():
                if row['Ch 1'] > 0 and row['Ch 2'] == 0 and row['Ch 3'] == 0:
                    write_arr.append("0")
                elif row['Ch 1'] == 0 and row['Ch 2'] > 0 and row['Ch 3'] == 0:
                    write_arr.append("1")
                    
    elif rand_type.lower() == 'poiss':
        channel = 'Ch ' + str(poiss_string)
        for index, row in clean_data.iterrows():
            if row[channel] > poiss_mid:
                write_arr.append("1")
            else:
                write_arr.append("0")
    # start out by just adding to concatenated string????
    out_string = ""
    for val in write_arr:
        out_string += val
    ascii_out = out_string.encode('ascii')
        
    print("Length of generated number: ", len(out_string))
        
    with open(output_loc, "wb") as outfile:
        outfile.write(ascii_out)
