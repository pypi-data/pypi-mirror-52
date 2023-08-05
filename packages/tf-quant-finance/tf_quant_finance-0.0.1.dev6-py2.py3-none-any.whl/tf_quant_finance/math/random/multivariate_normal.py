# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python2, python3
"""Functions to generate random numbers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import enum
import tensorflow as tf
import tensorflow_probability as tfp


@enum.unique
class RandomType(enum.Enum):
  PSEUDO = 0  # The standard Tensorflow random generator.
  STATELESS = 1  # The stateless Tensorflow random generator.
  HALTON = 2  # The standard Halton sequence.
  HALTON_RANDOMIZED = 3  # The randomized Halton sequence.
  SOBOL = 4  # The standard Sobol sequence.


def multivariate_normal(sample_shape,
                        mean=None,
                        covariance_matrix=None,
                        scale_matrix=None,
                        random_type=None,
                        validate_args=False,
                        seed=None,
                        name=None):
  """Generates draws from a multivariate Normal distribution.

  Draws samples from the multivariate Normal distribution on `R^k` with the
  supplied mean and covariance parameters. Allows generating either
  (pseudo) random or quasi-random draws based on the `random_type` parameter.

  ## Example:

  ```python

  # A single batch example.
  sample_shape = [10]  # Generates 10 draws.
  mean = [0.1, 0.2]  # The mean of the distribution. A single batch.
  covariance = [[1.0, 0.1], [0.1, 0.9]]
  # Produces a Tensor of shape [10, 2] containing 10 samples from the
  # 2 dimensional normal. The draws are generated using the standard random
  # number generator in TF.
  sample = multivariate_normal(sample_shape, mean=mean,
                               covariance_matrix=covariance,
                               random_type=RandomType.PSEUDO)

  # Produces a Tensor of shape [10, 2] containing 10 samples from the
  # 2 dimensional normal. Here the draws are generated using the stateless
  # random number generator. Note that a seed parameter is required and may
  # not be omitted. For the fixed seed, the same numbers will be produced
  # regardless of the rest of the graph or across independent sessions.
  sample_stateless = multivariate_normal(sample_shape, mean=mean,
                                         covariance_matrix=covariance,
                                         random_type=RandomType.STATELESS,
                                         seed=1234)

  # A multi-batch example. We can simultaneously draw from more than one
  # set of parameters similarly to the behaviour in tensorflow distributions
  # library.
  sample_shape = [5, 4]  # Twenty samples arranged as a 5x4 matrix.
  means = [[1.0, -1.0], [0.0, 2.0],[0.3, 1.4]]  # A batch of three mean vectors.
  # This demonstrates the broadcasting of the parameters. While we have
  # a batch of 3 mean vectors, we supply only one covariance matrix. This means
  # that three distributions have different means but the same covariance.
  covariances = [[1.0, 0.1], [0.1, 1.0]]

  # Produces a Tensor of shape [5, 4, 3, 2] containing 20 samples from the
  # batch of 3 bivariate normals.
  sample_batch = multivariate_normal(sample_shape, mean=means,
                                     covariance_matrix=covariance)

  Args:
    sample_shape: Rank 1 `Tensor` of positive `int32`s. Should specify a valid
      shape for a `Tensor`. The shape of the samples to be drawn.
    mean: Real `Tensor` of rank at least 1 or None. The shape of the `Tensor` is
      interpreted as `batch_shape + [k]` where `k` is the dimension of domain.
      The mean value(s) of the distribution(s) to draw from.
      Default value: None which is mapped to a zero mean vector.
    covariance_matrix: Real `Tensor` of rank at least 2 or None. Symmetric
      positive definite `Tensor` of  same `dtype` as `mean`. The strict upper
      triangle of `covariance_matrix` is ignored, so if `covariance_matrix` is
      not symmetric no error will be raised (unless `validate_args is True`).
      `covariance_matrix` has shape `batch_shape + [k, k]` where `b >= 0` and
      `k` is the event size.
      Default value: None which is mapped to the identity covariance.
    scale_matrix: Real `Tensor` of rank at least 2 or None. If supplied, it
      should be positive definite `Tensor` of same `dtype` as `mean`. The
      covariance matrix is related to the scale matrix by `covariance =
      scale_matrix * Transpose(scale_matrix)`.
      Default value: None which corresponds to an identity covariance matrix.
    random_type: Enum value of `RandomType`. The type of draw to generate.
      Default value: None which is mapped to `RandomType.PSEUDO`.
    validate_args: Python `bool`. When `True`, distribution parameters are
      checked for validity despite possibly degrading runtime performance. When
      `False` invalid inputs may silently render incorrect outputs.
      Default value: False.
    seed: Seed for the random number generator. The seed is only relevant if
      `random_type` is one of `[PSEUDO, STATELESS, HALTON_RANDOMIZED]`. For
      `PSEUDO`, the seed should be a Python integer. For the other two options,
      the seed may either be a Python integer or a tuple of Python integers.
    name: Python `str` name prefixed to Ops created by this class.
      Default value: None which is mapped to the default name
        'multivariate_normal'.

  Returns:
    samples: A `Tensor` of shape `sample_shape + batch_shape + [k]`. The draws
      from the multivariate normal distribution.

  Raises:
    ValueError:
      (a) If all of `mean`, `covariance_matrix` and `scale_matrix` are None.
      (b) If both `covariance_matrix` and `scale_matrix` are specified.
    NotImplementedError: If `random_type` is not RandomType.PSEUDO.
  """
  random_type = RandomType.PSEUDO if random_type is None else random_type
  # TODO: Implement the other random types.
  if random_type != RandomType.PSEUDO:
    raise NotImplementedError('Only RandomType.PSEUDO is supported currently.')

  if mean is None and covariance_matrix is None and scale_matrix is None:
    raise ValueError('At least one of mean, covariance_matrix or scale_matrix'
                     ' must be specified.')

  if covariance_matrix is not None and scale_matrix is not None:
    raise ValueError('Only one of covariance matrix or scale matrix'
                     ' must be specified')

  with tf.name_scope(
      name,
      default_name='multivariate_normal',
      values=[sample_shape, mean, covariance_matrix, scale_matrix]):

    return _mvnormal_pseudo(
        sample_shape,
        mean,
        covariance_matrix=covariance_matrix,
        scale_matrix=scale_matrix,
        validate_args=validate_args,
        seed=seed)


def _mvnormal_pseudo(sample_shape,
                     mean,
                     covariance_matrix=None,
                     scale_matrix=None,
                     validate_args=False,
                     seed=None):
  """Returns normal draws using the tfp multivariate normal distribution."""
  if scale_matrix is not None:
    distribution = tfp.distributions.MultivariateNormalLinearOperator(
        loc=mean,
        scale=tf.linalg.LinearOperatorFullMatrix(scale_matrix),
        validate_args=validate_args)
  else:
    distribution = tfp.distributions.MultivariateNormalFullCovariance(
        loc=mean,
        covariance_matrix=covariance_matrix,
        validate_args=validate_args)
  return distribution.sample(sample_shape, seed=seed)
