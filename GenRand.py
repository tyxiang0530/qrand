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
data_df, data_settings = cd.clean_csv("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\qrand\\data\\1115_fixed\\enclose\\encloserun1.csv")
data_df.head()
# %%
def calibrate_poisson(df_in, channel_num):
    po.get_poisson_midpt(data_df, 1)
    
# %%
