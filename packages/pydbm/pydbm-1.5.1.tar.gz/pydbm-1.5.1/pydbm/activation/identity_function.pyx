# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as np
from pydbm.activation.interface.activating_function_interface import ActivatingFunctionInterface
ctypedef np.float64_t DOUBLE_t


class IdentityFunction(ActivatingFunctionInterface):
    '''
    Identity function.
    '''

    def activate(self, np.ndarray x):
        '''
        Activate and extract feature points in forward propagation.

        Args:
            x   `np.ndarray` of observed data points.

        Returns:
            `np.ndarray` of the activated feature points.
        '''
        if self.batch_norm is not None:
            x = self.batch_norm.forward_propagation(x)

        return x

    def derivative(self, np.ndarray y):
        '''
        Derivative and extract delta in back propagation.

        Args:
            y:  `np.ndarray` of delta.

        Returns:
            `np.ndarray` of delta.
        '''
        if self.batch_norm is not None:
            y = self.batch_norm.back_propagation(y)

        return y

    def forward(self, np.ndarray x):
        '''
        Forward propagation but not retain the activation.

        Args:
            x   `np.ndarray` of observed data points.

        Returns:
            The result.
        '''
        return x

    def backward(self, np.ndarray y):
        '''
        Back propagation but not operate the activation.

        Args:
            y:  `np.ndarray` of delta.

        Returns:
            The result.
        '''
        return y
