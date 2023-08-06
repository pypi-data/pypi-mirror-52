.. image:: https://badge.fury.io/py/pyron-layers.svg
   :target: https://badge.fury.io/py/pyron-layers
   :alt: PyPI version

.. image:: https://i10git.cs.fau.de/seitz/pyronn-layers/badges/master/pipeline.svg 
    :target: https://i10git.cs.fau.de/seitz/pyronn-layers
    :alt: Gitlab CI
    
=============
pyronn-layers
=============


This is a Python wrapper around `PYRO-NN-Layers <https://github.com/csyben/PYRO-NN-Layers>`_.
Install it via

.. code:: bash

   pip install pyronn-layers

Or if you downloaded this `repository <https://github.com/theHamsta/pyronn.layers.git>`

.. code:: bash

   pip install -e .

It uses `pystencils-autodiff <https://github.com/pycodegen/pystencils_autodiff>`_ to automatically compile the C++/CUDA source files.
The code gets automatically recompiled if you make changes to the source files in the folder PYRO-NN-Layers.

If you prefer pre-build versions of PYRO-NN-Layers go to the `Release page of PYRO-NN-Layers <https://github.com/csyben/PYRO-NN-Layers/releases>`_
or download the latest artifacts from our CI (links only working if pipeline badge above is green):

   * `pyronn-layers.so for Ubuntu, tensorflow_gpu-1.14.0-cp37-cp37m-manylinux1_x86_64.whl <https://i10git.cs.fau.de/seitz/pyronn-layers/builds/artifacts/master/download?job=full>`_


Requirements
------------

You have a functioning toolchain for NVCC installed.
`nvcc` must be available in `PATH`.
If compilation fails you can change the selected compiler: http://pycodegen.pages.walberla.net/pystencils/sphinx/configuration.html?highlight=compiler
