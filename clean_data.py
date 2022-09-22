# %%
from distutils.command.clean import clean
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from matplotlib.ticker import MultipleLocator
# %%
test_path = "C:\\Users\\tyxia\\OneDrive - Pomona College\Pomona\\randomness_proj\\data\\xiang_0915_initialtests\\run_1.csv"
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
    data_df = data_df.drop(['Entry number', 'Ch 4', 'Ch 5', 'Ch 6', 'Ch 7', 'Ch 8'], axis = 1)
    data_df.to_csv(csv_in.split('.cs')[0] + '_clean.csv')
    
    return data_df, settings_dict
# %%
def plot_counts_timesteps(clean_df_in, channel_1, channel_2):
    data_df = clean_df_in
    x_vals = np.arange(0, len(data_df), 1)
    channel_string_1 = 'Ch ' + str(channel_1)
    channel_string_2 = 'Ch ' + str(channel_2)

    fsize = 15
    tsize = 18
    lsize = 10
    tdir = 'in'
    major = 5.0
    minor = 3.0
    style = 'default'

    plt.style.use(style)
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = fsize
    plt.rcParams['legend.fontsize'] = lsize
    plt.rcParams['xtick.direction'] = tdir
    plt.rcParams['ytick.direction'] = tdir
    plt.rcParams['xtick.major.size'] = major
    plt.rcParams['xtick.minor.size'] = minor
    plt.rcParams['ytick.major.size'] = major
    plt.rcParams['ytick.minor.size'] = minor

    xsize = 10
    ysize = 5


    plt.figure(figsize=(xsize, ysize))
    plt.scatter(x_vals[0:50], 
                data_df[channel_string_1][0:50], 
                label = channel_string_1 + " counts")
    plt.scatter(x_vals[0:50], 
                data_df[channel_string_2][0:50], 
                label = channel_string_2 + " counts")
    plt.title("Photon Counts Over Integration Timesteps.")

    ax = plt.gca()
    # ax.xaxis.set_minor_locator(MultipleLocator(.005))
    # ax.yaxis.set_minor_locator(MultipleLocator(.005))

    plt.xlabel('timestep', labelpad = 10)
    plt.ylabel('photon counts', labelpad = 10)
    plt.legend(loc = 'upper left')
    plt.show()
# %%
def count_histogram(channel, clean_df_in):
    channel_string = 'Ch ' + str(channel)
    data_np = clean_df_in[channel_string].to_numpy()
    counts = np.bincount(data_np)
    
    fig, ax = plt.subplots()
    ax.bar(range(len(counts)), counts, width=0.6, align='center')
    ax.set(xticks=range(10), xlim=[-1, 5])
    ax.set_xlabel("Photon Counts per Timestep")
    ax.set_ylabel("Frequency")
    
    plt.show()
# %%
def graph_sums(data_df, channel_1, channel_2):
    num_bins = 50
    n = int(len(data_df) / num_bins)
    x_vals = np.arange(0, num_bins, 1)
    
    channel_string_1 = 'Ch ' + str(channel_1)
    channel_string_2 = 'Ch ' + str(channel_2)
    
    channel_1_bin = data_df[channel_string_1].groupby(data_df.index // n).sum()
    channel_2_bin = data_df[channel_string_2].groupby(data_df.index // n).sum()

    fsize = 15
    tsize = 18
    lsize = 10
    tdir = 'in'
    major = 5.0
    minor = 3.0
    style = 'default'

    plt.style.use(style)
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = fsize
    plt.rcParams['legend.fontsize'] = lsize
    plt.rcParams['xtick.direction'] = tdir
    plt.rcParams['ytick.direction'] = tdir
    plt.rcParams['xtick.major.size'] = major
    plt.rcParams['xtick.minor.size'] = minor
    plt.rcParams['ytick.major.size'] = major
    plt.rcParams['ytick.minor.size'] = minor

    xsize = 10
    ysize = 5


    plt.figure(figsize=(xsize, ysize))
    plt.scatter(x_vals, 
                channel_1_bin, 
                label = channel_string_1 + " counts")
    plt.scatter(x_vals, 
                channel_2_bin, 
                label = channel_string_2 + " counts")
    plt.title("Photon Counts Over Bucketed Integration Timesteps")

    ax = plt.gca()
    # ax.xaxis.set_minor_locator(MultipleLocator(.005))
    # ax.yaxis.set_minor_locator(MultipleLocator(.005))

    plt.xlabel('timestep buckets', labelpad = 10)
    plt.ylabel('photon counts', labelpad = 10)
    plt.legend(loc = 'upper left')
    plt.show()
    

# %%
def format_for_tests(clean_data, channel_string, output_loc):
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
    if channel_string == '3':
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
                
    if channel_string == '2':
        for index, row in clean_data.iterrows():
            if row['Ch 1'] > 0 and row['Ch 2'] == 0:
                write_arr.append("00")
            elif row['Ch 1'] == 0 and row['Ch 2'] > 0:
                write_arr.append("01")
            else:
                write_arr.append("10")
                
    if channel_string == 'coincidence':
        for index, row in clean_data.iterrows():
            if row['Ch 1'] > 0 and row['Ch 2'] == 0 and row['Ch 3'] == 0:
                write_arr.append("0")
            elif row['Ch 1'] == 0 and row['Ch 2'] > 0 and row['Ch 3'] == 0:
                write_arr.append("1")
    
    # start out by just adding to concatenated string????
    out_string = ""
    for val in write_arr:
        out_string += val
    ascii_out = out_string.encode('ascii')
        
    print("Length of generated number: ", len(out_string))
        
    with open(output_loc, "wb") as outfile:
        outfile.write(ascii_out)
                
    
# %%
data_df, settings = clean_csv(test_path)
plot_counts_timesteps(data_df, 2, 3)
count_histogram(2, data_df)
count_histogram(3, data_df)
graph_sums(data_df, 2, 3)
format_for_tests(data_df, "3", "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0915_initialtests\\run_1_binary.json")
# %%
print(settings)
# %%
data_df.head()
# %%
