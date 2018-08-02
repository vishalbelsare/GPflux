# Copyright (C) PROWLER.io 2018 - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential


from typing import List, Optional

import gpflow
import numpy as np

from .. import init
from ..convolution import ConvKernel, InducingPatch
from .layers import GPLayer


def _check_input_output_shape(input_shape, output_shape, patch_size):
    width_check = (input_shape[0] - patch_size[0] + 1 == output_shape[0])
    height_check = (input_shape[1] - patch_size[1] + 1 == output_shape[1])
    return width_check and height_check


class ConvLayer(GPLayer):

    def __init__(self,
                 input_shape: List,
                 output_shape: List,
                 number_inducing: int,
                 patch_size: List, *,
                 stride: int = 1,
                 num_filters: int = 1,
                 q_mu: Optional[np.ndarray] = None,
                 q_sqrt: Optional[np.ndarray] = None,
                 mean_function: Optional[gpflow.mean_functions.MeanFunction] = None,
                 base_kernel_class: type = gpflow.kernels.RBF,
                 inducing_patches_initializer=init.NormalInitializer()):
        """
        This layer constructs a convolutional GP layer.
        :input_shape: tuple
            shape of the input images, W x H
        :param patch_size: tuple
            Shape of the patches (a.k.a kernel_size of filter_size)
        :param number_inducing: int
            Number of inducing patches, M

        Optional:
        :param stride: int
            An integer specifying the strides of the convolution along the height and width.
        :param num_filters: int
            Number of filters in the convolution
        :param q_mu and q_sqrt: np.ndarrays
            Variatial posterior parameterisation.
        :param inducing_patches_initializer: init.Initializer.
            Instance of the class `init.Initializer` that initializes the inducing patches.
        """
        assert num_filters == 1 and stride == 1  # TODO

        if not _check_input_output_shape(input_shape, output_shape, patch_size):
            print("input_shape: ", input_shape)
            print("output_shape: ", output_shape)
            print("patch_size: ", patch_size)
            raise ValueError("The input, output and patch size are inconsistent in the ConvLayer. "
                             "The correct dimension should be: output = input - patch_size + 1.")

        # inducing patches
        inducing_patch_shape = [number_inducing, *patch_size]  # tuple with values: M x w x h
        init_patches = inducing_patches_initializer(inducing_patch_shape)  # M x w x h
        inducing_patches = InducingPatch(init_patches)

        base_kernel = base_kernel_class(np.prod(patch_size))  # TODO: we are using the default kernel hyps
        conv_kernel = ConvKernel(base_kernel, input_shape, patch_size, colour_channels=1)  # TODO add colour

        super().__init__(conv_kernel, inducing_patches, num_latents=1,
                         q_mu=q_mu, q_sqrt=q_sqrt, mean_function=mean_function)

        self.base_kernel_class = base_kernel_class
        self.patch_size= patch_size

    def __str__(self):
        desc = "\n\t+ Conv: patch {}".format(self.patch_size)
        desc += " base_kern {}".format(self.base_kernel_class.__name__)
        return super().__str__() + desc
