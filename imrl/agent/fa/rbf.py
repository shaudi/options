"""Radial basis function approximator."""

# Third party
import numpy as np
from itertools import product
from scipy.linalg import norm
# First party
from imrl.agent.fa.func_approx import FunctionApproximator


class RBF(FunctionApproximator):
    """Radial basis function approximator. Creates n^d RBF kernels evenly spaced,
    d is the dimensionality of the input space and n is the number of kernels along a single dimension (the resolution)"""

    def __init__(self, dim, resolution, num_actions, beta=40, min_val=0, max_val=1):
        super(RBF, self).__init__(resolution ** dim, num_actions)
        self.dim = dim
        self.min_val = min_val
        self.max_val = max_val
        self.beta = beta

        # Segment the space based on resolution
        segmentation = [np.linspace(min_val, max_val, resolution).tolist()] * dim

        # Generate centers from Cartiesian product of segmentation lists
        centers = product(*segmentation)
        self.centers = [np.asarray(a) for a in centers]

    def _evalulate_kernel(self, c, x):
        """Evaluate an RBF kernel c at a given point x."""
        return np.exp(-self.beta * norm(c - x, 2) ** 2)

    def evaluate(self, s):
        """Compute the feature vector for the given state."""
        assert len(s) == self.dim
        for i in range(len(s)):
            assert self.min_val <= s[i] <= self.max_val
        fv = np.zeros((self.num_features, 1))
        for ci, c in enumerate(self.centers):
            fv[ci] = self._evalulate_kernel(c, s)
        return fv

    def evaluate_state_action(self, s, a):
        """Compute the feature vector for the given state-action pair."""
        assert len(s) == self.dim
        assert a < self.num_actions
        for i in range(len(s)):
            assert self.min_val <= s[i] <= self.max_val
        fv = np.zeros((self.size, 1))
        for ci, c in enumerate(self.centers):
            fv[self.num_features * a + ci] = self._evalulate_kernel(c, s)
        return fv