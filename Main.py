# %%
import CleanData as cd
import DataExplore as de
import PoissonOps as po
from importlib import reload
import os
from jinja2 import Environment, FileSystemLoader
import time

# %%
reload(de)
reload(po)
reload(cd)

# %%
def gen_report(csv_in, title):
    input_filename = csv_in.split('\\')[-1].split('.')[0]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    env = Environment(loader=FileSystemLoader("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\qrand\\"))
    template = env.get_template('report_template.html')
    # deal with file if it already exists
    output_dir = os.path.dirname(csv_in)
    output_dir = output_dir + "\\exploratory_report\\" + input_filename 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data_df, settings = cd.clean_csv(csv_in)
    hist_abs1 = de.count_histogram_abs(3, data_df, save = True, outdir = output_dir)
    hist_norm1 = de.count_histogram_norm(3, data_df, save = True, outdir = output_dir)
    hist_abs2 = de.count_histogram_abs(1, data_df, save = True, outdir = output_dir)
    hist_norm2 = de.count_histogram_norm(1, data_df, save = True, outdir = output_dir)
    ts_indiv = de.plot_counts_timesteps(data_df, 1, 3, save = True, outdir = output_dir)
    ts_bucket = de.graph_sums(data_df, 1, 3, save = True, outdir = output_dir)
    p_mu1, p_cdf1, p_pmf1, p_outpath1 = po.get_poisson_var(data_df, 3, outdir = output_dir, save = True)
    p_mu1, p_cdf1, p_pmf1, p_outpath2 = po.get_poisson_var(data_df, 1, outdir = output_dir, save = True)
    p_ecdf1 = po.simulate_poisson(data_df, 3, outdir = output_dir, save = True)
    p_ecdf2 = po.simulate_poisson(data_df, 1, outdir = output_dir, save = True)
    
    html = template.render(page_title_text='General Visualizations for Experimental Run',
                           title_text='Photon Statistics for Randomness Trial: ' + title,
                           description_title ='This report covers basic statistics on photon arrival times, \
                               photon counts, and coincidences. The settings used for this trial are: ' + \
                                   str(settings) + '. The following report was generated at: ' + timestr,
                           test_1='Unnormalized Counts Across Integration Times',
                           image1_loc = hist_abs1,
                           description1='The above graph displays the distribution of counts that occur \
                               for each integration timestep (' + str(settings['sample integration time (s)']) + ")",
                           test_2='Unnormalized Counts Across Integration Times',
                           image2_loc = hist_abs2,
                           description2='The above graph displays the distribution of counts that occur \
                               for each integration timestep (' + str(settings['sample integration time (s)']) + ")",
                           test_3 = 'Normalized Counts Across Integration Times',
                           image3_loc = hist_norm1,
                           description3='The above graph displays the distribution of counts that occur for \
                               each integration timestep (' + str(settings['sample integration time (s)']) + ") \
                                   normalized between 0 and 1",
                           test_4 = 'Normalized Counts Across Integration Times',
                           image4_loc = hist_norm2,
                           description4='The above graph displays the distribution of counts that occur for \
                               each integration timestep (' + str(settings['sample integration time (s)']) + ") \
                                   normalized between 0 and 1",
                           test_5 = 'Photon Counts Over all Integration Timesteps',
                           image5_loc = ts_indiv,
                           description5 = 'The amount of photons we count at each integration timestep',
                           test_6 = 'Photon Counts Over all Bucketed Integration Timesteps',
                           image6_loc = ts_bucket,
                           description6 = 'The total amount of photons we count at a summation of integration timesteps',
                           test_7 = 'ECDF Tests for the given channel',
                           image7_loc = p_ecdf1,
                           description7 = 'A graphical measure of how close our counts are to a Poissonian distribution',
                           test_8 = 'ECDF Tests for the given channel',
                           image8_loc = p_ecdf2,
                           description8 = 'A graphical measure of how close our counts are to a Poissonian distribution',
                           test_9 = 'Fitted Poissonian PMF and CDF for the given channel',
                           image9_loc = p_outpath1,
                           description9 = 'The probability mass function and cumulative distribution function \
                               for a Poissonian fitted to the data for the given channel',
                           test_10 = 'Fitted Poissonian PMF and CDF for the given channel',
                           image10_loc = p_outpath2,
                           description10 = 'The probability mass function and cumulative distribution function \
                               for a Poissonian fitted to the data for the given channel'
    )
    html_out = output_dir + '\\data_exploration_report_' + input_filename + '.html'
    with open(html_out, 'w') as f:
        f.write(html)

# %%
def main(csv_in):
    outpath = "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0922_runs\\poiss_test_binary.json"
    data_df, settings = cd.clean_csv(csv_in)
    
    po.get_poisson_var(data_df, 3)
    poiss_mid = po.get_poisson_midpt(data_df, 3)
    cd.format_for_tests(data_df, 3, 'poiss', outpath, poiss_mid, 3)
# lill_poisson(data_df, 3)
# format_for_tests(data_df, "3", "C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0915_initialtests\\run_1_binary.json")

# %%
gen_report("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\qrand\\data\\filter_tests\\3_6\\new_filter_bothpoiints_fix_clean.csv", "New Filter Tests")
# main("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0922_runs\\no_bs_down_convert_1.csv")
# %%
data_df, settings = cd.clean_csv("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_1007_robustness_tests\\laser\\change_over_time_test_laser.csv")
ts_bucket = de.graph_sums(data_df, 1, 3, bucket_size = 200)
# %%
