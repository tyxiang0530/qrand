import numpy as np
import CleanData as CD

def get_Racc(integration_time, channel_1, channel_2, tau):
    tau_c = 2 * tau
    total_1_counts = np.sum(channel_1)
    total_2_counts = np.sum(channel_2)
    total_time_1 = integration_time * channel_1.shape[0]
    total_time_2 = integration_time * channel_2.shape[0]
    R1 = total_1_counts / total_time_1
    R2 = total_2_counts / total_time_2

    return tau_c * R1 * R2
def get_alpha(integration_time, channel_1, channel_2, CC, tau):
    Racc = get_Racc(integration_time, channel_1, channel_2, tau)
    total_CC = np.sum(CC)
    total_time_cc = integration_time * CC.shape[0]
    Rc = total_CC / total_time_cc
    return Rc / Racc


def file_to_alpha(file_in, pulsewidth):
    pulse_widths = {"short": 1e-8, "medium": 1.4e-8, "long": 1.8e-8, "instrument": 2.5e-8}
    df, settings = CD.clean_csv(file_in)
    integration_time = settings['sample integration time (s)']

    alpha = get_alpha(integration_time, df['Ch 1'], df['Ch 2'], df['Ch 4'], pulse_widths[pulsewidth])
    return alpha
    