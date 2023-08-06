import numpy as np
import scipy.stats

from .model import BestResults


def posterior_mode(best_out: BestResults,
                   variable_name: str):
    """Calculate the posterior mode of a variable

    Parameters
    ----------
    best_out : BestResults
        The result of the analysis.
    variable_name : string
        The name of the variable whose posterior mode is to be calculated.

    Returns
    -------
    float
        The posterior mode.
    """
    sample_vec = best_out.trace[variable_name]

    # calculate mode using kernel density estimate
    kernel = scipy.stats.gaussian_kde(sample_vec)

    bw = kernel.covariance_factor()
    cut = 3 * bw
    x_low = np.min(sample_vec) - cut * bw
    x_high = np.max(sample_vec) + cut * bw
    n = 512
    x = np.linspace(x_low, x_high, n)
    vals = kernel.evaluate(x)
    max_idx = np.argmax(vals)
    mode_val = x[max_idx]

    return mode_val
