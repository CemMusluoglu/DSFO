import numpy as np
from numpy import linalg as LA
from pymanopt.manifolds import Sphere
from pymanopt import Problem
from pymanopt.solvers import TrustRegions
import autograd


# This module implements the functions related to the SCQP problem.
#
# Author: Cem Musluoglu, KU Leuven, Department of Electrical Engineering (ESAT), STADIUS Center for Dynamical Systems,
# Signal Processing and Data Analytics
# Correspondence: cemates.musluoglu@esat.kuleuven.be

def scqp_solver(prob_params, data):
    """Solve the SCQP problem min 0.5*E[||X'*y(t)||^2]+trace(X'*B) s.t. trace(X'*Gamma*X)=1."""
    Y = data['Y_list'][0]
    B = data['B_list'][0]
    Gamma = data['Gamma_list'][0]
    nbsamples = prob_params['nbsamples']

    rng = np.random.default_rng()
    M = np.size(Y, 0)
    Q = prob_params['Q']
    X = rng.standard_normal(size=(M, Q))

    manifold = Sphere(np.size(B, 0), np.size(B, 1))

    Ryy = Y @ Y.T / nbsamples
    Ryy = (Ryy + Ryy.T) / 2

    Gamma = (Gamma + Gamma.T) / 2

    L = LA.cholesky(Gamma)
    Ryy_t = LA.inv(L) @ Ryy @ LA.inv(L).T
    Ryy_t = (Ryy_t + Ryy_t.T) / 2
    B_t = LA.inv(L) @ B

    def cost(X):
        return 0.5 * autograd.numpy.trace(X.T @ Ryy_t @ X) + autograd.numpy.trace(X.T @ B_t)

    problem = Problem(manifold=manifold, cost=cost)
    problem.verbosity = 0

    solver = TrustRegions()
    X_star = solver.solve(problem)
    X_star = LA.inv(L.T) @ X_star

    return X_star


def scqp_eval(X, data):
    """Evaluate the SCQP objective 0.5*E[||X'*y(t)||^2]+trace(X'*B)."""
    Y = data['Y_list'][0]
    B = data['B_list'][0]
    N = np.size(Y, 1)

    Ryy = Y @ Y.T / N
    Ryy = (Ryy + Ryy.T) / 2

    f = 0.5 * np.trace(X.T @ Ryy @ X) + np.trace(X.T @ B)

    return f


def create_data(nbsensors, nbsamples, Q):
    """Create data for the SCQP problem."""
    rng = np.random.default_rng()

    Y = rng.standard_normal(size=(nbsensors, nbsamples))
    B = rng.standard_normal(size=(nbsensors, Q))

    return Y, B
