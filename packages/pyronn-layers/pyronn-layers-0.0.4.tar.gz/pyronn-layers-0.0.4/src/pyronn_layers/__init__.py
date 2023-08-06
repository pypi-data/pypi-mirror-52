# -*- coding: utf-8 -*-
import glob
import os.path

import pystencils_autodiff.tensorflow_jit
import tensorflow as tf
from pkg_resources import DistributionNotFound, get_distribution

import pyronn_layers

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'pyronn-layers'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound


_pyronn_layers_dir = os.path.join(os.path.dirname(__file__), 'PYRO-NN-Layers')
_pyronn_layers_sources = glob.glob(os.path.join(_pyronn_layers_dir, '*.cc'))

assert _pyronn_layers_sources, "Could not find the source files of PYRO-NN-Layers.\n" \
    "Did you check out the Git submodule (`git submodule update --init --recursive`)?"


_pyronn_layers_module_file = pystencils_autodiff.tensorflow_jit.compile_sources_and_load(
    [],
    _pyronn_layers_sources,
    additional_compile_flags=['-I' + _pyronn_layers_dir, '-DGOOGLE_CUDA'],
    compile_only=True)  # TODO: msvc! \D
_pyronn_layers_module = tf.load_op_library(_pyronn_layers_module_file)

for obj in dir(_pyronn_layers_module):
    setattr(pyronn_layers, obj, getattr(_pyronn_layers_module, obj))
