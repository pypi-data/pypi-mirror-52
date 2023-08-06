import numpy as np
import warnings


def onepara(R: np.ndarray) -> np.ndarray:
    """Converts an ill-conditioned correlation matrix
       into well-conditioned matrix with one common
       correlation coefficient

    Parameters:
    -----------
    R : ndarray
        an illconditioned correlation matrix,
        e.g. oxyba.illcond_corrmat

    Return:
    -------
    cmat : ndarray
        DxD matrix with +1 as diagonal elements
        and 1 common coefficient for all other
        relations.
    """
    d = R.shape[0]

    if d < 2:
        raise Exception((
            "More than one variable is required."
            "Supply at least a 2x2 matrix."))

    # the explicit solution
    x = (np.sum(R) + np.trace(R)) / (d**2 - d)

    if x < (-1. / (d - 1)) or x > 1:
        warnings.warn("No analytic solution found x={:.8f}".format(x))
        return None
    else:
        C = np.eye(d)
        C[np.logical_not(C)] = x
        return C
