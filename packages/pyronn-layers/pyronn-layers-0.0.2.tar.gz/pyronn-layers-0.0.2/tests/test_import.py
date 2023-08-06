# -*- coding: utf-8 -*-
#
# Copyright © 2019 Stephan Seitz <stephan.seitz@fau.de>
#
# Distributed under terms of the GPLv3 license.

"""

"""
from shutil import copyfile


def test_import():
    import pyronn_layers


def test_compile_pyronn_layers_so():
    import pyronn_layers
    copyfile(pyronn_layers._pyronn_layers_module_file, 'pyronn_layers.so')
