# %%
import CleanData as cd
import DataExplore as de
import PoissonOps as po
from importlib import reload

reload(de)
reload(po)
reload(cd)

# %%
def main(csv_in):
    outpath = "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\poiss_test_binary.json"
    data_df, settings = cd.clean_csv(csv_in)
    counts = de.count_histogram_rough(3, data_df)
    de.count_histogram_norm(3, data_df)
    de.plot_counts_timesteps(data_df, 2, 3)
    de.graph_sums(data_df, 2, 3)
    
    po.get_poisson_var(data_df, 3)
    poiss_mid = po.get_poisson_midpt(data_df, 3)
    cd.format_for_tests(data_df, 3, 'poiss', '', poiss_mid)
# lill_poisson(data_df, 3)
# format_for_tests(data_df, "3", "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0915_initialtests\\run_1_binary.json")

# %%
main("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0922_runs")