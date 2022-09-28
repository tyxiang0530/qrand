# %%
import CleanData as cd
import DataExplore as de
import PoissonOps as po
from importlib import reload
import os
from jinja2 import Environment, FileSystemLoader
import time

reload(de)
reload(po)
reload(cd)

# %%
def gen_report(csv_in):
    input_filename = csv_in.split('\\')[-1].split('.')[0]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    env = Environment(loader=FileSystemLoader('C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\qrand\\'))
    template = env.get_template('report_template.html')
    # deal with file if it already exists
    output_dir = os.path.dirname(csv_in)
    output_dir = output_dir + "\\exploratory_report\\" + input_filename 
    os.makedirs(output_dir)

    
    data_df, settings = cd.clean_csv(csv_in)
    hist_abs = de.count_histogram_abs(3, data_df, save = True, outdir = output_dir)
    hist_norm = de.count_histogram_norm(3, data_df, save = True, outdir = output_dir)
    ts_indiv = de.plot_counts_timesteps(data_df, 2, 3, save = True, outdir = output_dir)
    ts_bucket = de.graph_sums(data_df, 2, 3, save = True, outdir = output_dir)
    p_mu, p_cdf, p_pmf, p_outpath = po.get_poisson_var(data_df, 3, outdir = output_dir, save = True)
    p_ecdf = po.simulate_poisson(data_df, 3, outdir = output_dir, save = True)
    
    html = template.render(page_title_text='General Visualizations for Experimental Run',
                           title_text='Photon Statistics for Randomness Trial',
                           description_title ='This report covers basic statistics on photon arrival times, \
                               photon counts, and coincidences. The settings used for this trial are: ' + \
                                   str(settings) + '. The following report was generated at: ' + timestr,
                           test_1='Unnormalized Counts Across Integration Times',
                           image1_loc = hist_abs,
                           description1='The above graph displays the distribution of counts that occur \
                               for each integration timestep (' + str(settings['sample integration time (s)']) + ")",
                           test_2 = 'Normalized Counts Across Integration Times',
                           image2_loc = hist_norm,
                           description2='The above graph displays the distribution of counts that occur for \
                               each integration timestep (' + str(settings['sample integration time (s)']) + ") \
                                   normalized between 0 and 1",
                           test_3 = 'Photon Counts Over all Integration Timesteps',
                           image3_loc = ts_indiv,
                           description3 = 'The amount of photons we count at each integration timestep',
                           test_4 = 'Photon Counts Over all Bucketed Integration Timesteps',
                           image4_loc = ts_bucket,
                           description4 = 'The total amount of photons we count at a summation of integration timesteps',
                           test_5 = 'ECDF Tests',
                           image5_loc = p_ecdf,
                           description5 = 'A graphical measure of how close our counts are to a Poissonian distribution',
                           test_6 = 'Fitted Poissonian PMF and CDF',
                           image6_loc = p_outpath,
                           description6 = 'The probability mass function and cumulative distribution function \
                               for a Poissonian fitted to the data'
    )
    with open(output_dir + '\\data_exploration_report_' + input_filename + '.html', 'w') as f:
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
gen_report("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0922_runs\\no_bs_down_convert_1.csv")
# main("C:\\Users\\tyxia\\OneDrive - Pomona College\\Pomona\\randomness_proj\\data\\xiang_0922_runs\\no_bs_down_convert_1.csv")
# %%
