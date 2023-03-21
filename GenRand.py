# %%
import CleanData as cd
import DataExplore as de
import PoissonOps as po
from importlib import reload
import os
import time

# %%
reload(de)
reload(po)
reload(cd)

# %%
dir = "data\\1129_bs_in_nofilter\\"
file = dir + "run1.csv"
# %%
data_df, data_settings = cd.clean_csv(file)
data_df.head()
data_df['Ch 5'].sum()
# %%
def calibrate_poisson(df_in, channel_num):
    po.get_poisson_midpt(data_df, 1)
    
# %%
