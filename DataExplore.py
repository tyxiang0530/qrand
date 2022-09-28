# %%
from distutils.command.clean import clean
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from scipy.stats import poisson
from matplotlib.ticker import MultipleLocator
# %%
def plot_counts_timesteps(clean_df_in, channel_1, channel_2, save = False, outpath = None):
    data_df = clean_df_in
    x_vals = np.arange(0, len(data_df), 1)
    channel_string_1 = 'Ch ' + str(channel_1)
    channel_string_2 = 'Ch ' + str(channel_2)

    fsize = 15
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
    
    if save:
        plt.savefig(outpath)
# %%
def count_histogram_rough(channel, clean_df_in, save = False, outpath = None):
    # adaptable binning and bucketing
    channel_string = 'Ch ' + str(channel)
    data_np = clean_df_in[channel_string].to_numpy()
    counts = np.bincount(data_np)
    bin_start = 0
    bin_finish = len(counts)
    
    for i in range(len(counts)):
        if counts[i] != 0:
            bin_start = i
            
    for i in range(len(counts)-1, -1, -1):
        if counts[i] != 0:
            bin_finish = i + 1
    print(bin_start)
    print(bin_finish)
    fig, ax = plt.subplots()
    ax.bar(range(len(counts)), counts, width=0.6, align='center')
    ax.set(xticks=range(0, 70), xlim=[0, 70])
    ax.set_xlabel("Photon Counts per Timestep (Channel " + str(channel) + ")")
    ax.set_ylabel("Frequency")
    plt.locator_params(axis='x', nbins=20)
    
    plt.show()
    if save:
        plt.savefig(outpath)
        
# %%
def count_histogram_norm(channel, clean_df_in, save = False, outpath = None):
    # adaptable binning and bucketing
    channel_string = 'Ch ' + str(channel)
    data_np = clean_df_in[channel_string].to_numpy()
    total_counts = clean_df_in[channel_string].sum()
    counts = np.bincount(data_np) / total_counts
    bin_start = 0
    bin_finish = len(counts)
    
    for i in range(len(counts)):
        if counts[i] != 0:
            bin_start = i
            
    for i in range(len(counts)-1, -1, -1):
        if counts[i] != 0:
            bin_finish = i + 1
    print(bin_start)
    print(bin_finish)
    fig, ax = plt.subplots()
    ax.bar(range(len(counts)), counts, width=0.6, align='center')
    ax.set(xticks=range(0, 70), xlim=[0, 70])
    ax.set_xlabel("Photon Counts per Timestep (Channel " + str(channel) + ")")
    ax.set_ylabel("Frequency (Normalized)")
    plt.locator_params(axis='x', nbins=20)
    
    plt.show()
    if save:
        plt.savefig(outpath)
# %%
def graph_sums(data_df, channel_1, channel_2, save = False, outpath = None):
    num_bins = 50
    n = int(len(data_df) / num_bins)
    x_vals = np.arange(0, num_bins, 1)
    
    channel_string_1 = 'Ch ' + str(channel_1)
    channel_string_2 = 'Ch ' + str(channel_2)
    
    channel_1_bin = data_df[channel_string_1].groupby(data_df.index // n).sum()
    channel_2_bin = data_df[channel_string_2].groupby(data_df.index // n).sum()

    fsize = 15
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
    
    if save:
        plt.savefig(outpath)