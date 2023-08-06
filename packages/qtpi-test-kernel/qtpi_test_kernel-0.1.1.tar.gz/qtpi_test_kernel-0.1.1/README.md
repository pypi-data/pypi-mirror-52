_kernel
===========

``qtpi_test_kernel`` is an example of a modified Jupyter kernel python wrapper to 
enable inputs written in Qtpi quantum language. This repository complements the 
documentation on wrapper kernels here:  

http://jupyter-client.readthedocs.io/en/latest/wrapperkernels.html

Installation
------------
1. User has to ensure that Python language is installed on the machine. 
2. User has to install package manager :
``pip`` in case of Python 2 or ``pip3``in case of Python 3.

3. Here are 2 options which depends on the previous installation -

To install ``qtpi_test_kernel`` from PyPI using ``Python 2``::

    pip install qtpi_test_kernel
    python -m qtpi_test_kernel.install
    

To install ``qtpi_test_kernel`` from PyPI using ``Python 3``::

    pip3 install qtpi_test_kernel
    python3 -m qtpi_test_kernel.install

Using the Qtpi kernel
---------------------
**Notebook**: The *New* menu in the notebook should show an option for an Qtpi notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel qtpi`` to
their command line arguments.
