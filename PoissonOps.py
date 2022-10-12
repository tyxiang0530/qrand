# %%
import CleanData as cd
from importlib import reload
from scipy.stats import poisson
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import DataExplore as de
import math
from scipy.special import factorial

reload(cd)
reload(de)
# %%
def fit_poisson(k, lamb):
    '''poisson function, parameter lamb is the fit parameter'''
    return poisson.pmf(k, lamb)

# %% Simple ecdf function
def ecdf(data):
    sx = np.sort(data)
    n = sx.size
    sy = np.arange(1,n+1)/n
    return sx,sy

def simulate_poisson(data_in, channel, outdir = None, save = False):
    channel_string = 'Ch ' + str(channel)
    data_np = data_in[channel_string].to_numpy()
    fig, ax = plt.subplots(figsize=(6,4))
    # CDF for observed data
    ecdf_x,ecdf_y = ecdf(data_np)
    ax.step(ecdf_x,ecdf_y,color='red',label='ECDF',
            linewidth=3,zorder=3)

    # CDF for hypothetical poisson
    pcdf_x = np.arange(data_np.min(),data_np.max()+1)
    pcdf_y = 1 - poisson.cdf(data_np.mean(),pcdf_x)
    ax.step(pcdf_x,pcdf_y, color='k',linewidth=3,
            label=f'Poisson {data_np.mean():.1f}',zorder=2)

    # Random variates of same size as data_np
    for i in range(10):
        randp = poisson.rvs(data_np.mean(),size=len(data_np))
        rcdf_x,rcdf_y = ecdf(randp)
        if i == 0:
            ax.step(rcdf_x,rcdf_y, color='grey',
                    label=f'Simulated Poisson',zorder=1)
        else:
            ax.step(rcdf_x,rcdf_y, color='grey',alpha=0.35,zorder=3)

    ax.legend(loc='upper left')
    plt.title("Measures of Poissonian Fit for Channel" + str(channel))
    if save == True:
        fname = "poisson_closeness" + str(channel) + ".png"
        outpath = outdir + "\\" + fname
        plt.savefig(outpath)
        plt.show()
        return fname
    
    plt.show()
    
# %%
def lill_poisson(data_in, channel,sim=10000,seed=10):
    channel_string = 'Ch ' + str(channel)
    channel_counts = data_in[channel_string].to_numpy()
    n = len(channel_counts)
    nu = np.arange(1.0,n+1)/n
    nm = np.arange(0.0,n)/n
    # Fit parameters
    m = channel_counts.mean()
    fp = poisson(m) # frozen Poisson
    # in function for KS stat
    
    def ks(obs):
        x = np.sort(obs)
        cv = fp.cdf(x)
        Dp = (nu - cv).max()
        Dm = (cv - nm).max()
        return np.max([Dp,Dm])
    
    # KS stat observed
    ks_obs = ks(channel_counts)
    # Generate simulation
    np.random.seed(seed)
    sa = np.zeros(sim)
    for i in range(sim):
        s = fp.rvs(n)
        sa[i] = ks(s)
    # calculate p-value
    p_val = np.append(sa,ks_obs).argsort()[-1]/sim
    print(f'KS Stat: {ks_obs:0.2f}, p-value {p_val:0.2f}')

    return ks_obs, p_val, sa

# %%
def chi_squared(obs, channel):
    channel_string = 'Ch ' + str(channel)
    channel_counts = obs[channel_string]
    channel_counts['quantile'] = poisson.cdf(obs.mean(),obs)
    channel_counts['quin'] = np.floor(channel_counts['quantile']/0.2)

    obs_counts = channel_counts['quin'].value_counts()
    exp_counts = len(obs)/5
    chi_stat = ((obs_counts - exp_counts)**2/exp_counts).sum()

# %%
def get_poisson_var(data_np, channel_in, outdir = None, save = False):
    counts = data_np['Ch ' + str(channel_in)]
    mu = counts.mean()
    x = np.arange(0, 100, 1)
    poisson_pmf = poisson.pmf(x, mu)
    poisson_cdf = poisson.cdf(x, mu)
    plt.plot(x, poisson_pmf, ms=8, label='poisson pmf')
    plt.plot(x, poisson_cdf, label = 'poisson cdf')
    plt.legend()
    plt.title("Fitted Poissonian PMF and CDF for Channel" + str(channel_in))
    
    if save:
        fname = "poiss_pmf_cdf_" + str(channel_in) + ".png"
        outpath = outdir + "\\" + fname
        plt.savefig(outpath)
        plt.show()
        
        return mu, poisson_cdf, poisson_pmf, fname
    plt.show()
    
    return mu, poisson_cdf, poisson_pmf, fname
# %%
def get_midpt(poisson_cdf):
    for idx in range(0, len(poisson_cdf)):
        if math.isclose(poisson_cdf[idx], float(0.5), abs_tol=1e-2):
            return(idx)
        
# %%
def get_poisson_midpt(data_np, channel_in):
    mu, poisson_cdf, poisson_pmf = get_poisson_var(data_np, channel_in)
    return get_midpt(poisson_cdf)

