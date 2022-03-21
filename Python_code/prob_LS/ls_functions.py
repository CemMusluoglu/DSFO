import numpy as np
from scipy import linalg as LA


# This module implements the functions related to the LS problem.
#
# Author: Cem Musluoglu, KU Leuven, Department of Electrical Engineering (ESAT), STADIUS Center for Dynamical Systems,
# Signal Processing and Data Analytics
# Correspondence: cemates.musluoglu@esat.kuleuven.be

def ls_solver(prob_params, data):
    """Solve the LS problem min E[||d(t) - X.T @ y(t)||**2]."""
    Y = data['Y_list'][0]
    D = data['Glob_Const_list'][0]

    N = prob_params['nbsamples']

    Ryy = Y @ Y.T / N
    Ryy = (Ryy + Ryy.T) / 2
    Ryd = Y @ D.T / N

    X_star = np.linalg.inv(Ryy) @ Ryd

    return X_star


def ls_eval(X, data):
    """Evaluate the LS objective E[||d(t) - X.T @ y(t)||**2]."""
    Y = data['Y_list'][0]
    D = data['Glob_Const_list'][0]
    N = np.size(Y, 1)

    Ryy = Y @ Y.T / N
    Ryy = (Ryy + Ryy.T) / 2
    Rdd = D @ D.T / N
    Rdd = (Rdd + Rdd.T) / 2
    Ryd = Y @ D.T / N

    f = np.trace(X.T @ Ryy @ X) + 2 * np.trace(X.T @ Ryd) + np.trace(Rdd)

    return f


def create_data(nbsensors, nbsamples, Q):
    """Create data for the LS problem."""
    rng = np.random.default_rng()

    signalvar = 0.5
    noisepower = 0.1
    nbsources = Q
    offset = 0.5

    D = rng.normal(loc=0, scale=np.sqrt(signalvar), size=(nbsources, nbsamples))
    A = rng.uniform(low=-offset, high=offset, size=(nbsensors, nbsources))
    noise = rng.normal(loc=0, scale=np.sqrt(noisepower), size=(nbsensors, nbsamples))

    Y = A @ D + noise

    return Y, D
