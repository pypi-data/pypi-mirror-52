========
PyCICADA
========

CICADA stands for Calcium Imaging Complete Automated Data Analysis.

It's a Python pipeline aimed for analyzing calcium imaging data.

CICADA is under development. The version published is an alpha version and the documentation is still not complete.
Don't hesitate to contact us if you want more information.

------------
Installation
------------


Install release from PyPI
-------------------------

The Python Package Index (PyPI) is a repository of software for the Python programming language.

To install or update PyCICADA distribution from PyPI simply run:

.. code::

   $ pip install -U pycicada

This will automatically install the following required dependencies:

 #. h5py
 #. numpy
 #. sortedcontainers
 #. shapely
 #. qtpy
 #. Pillow
 #. PyYAML
 #. scanimage-tiff-reader
 #. pyabf
 #. hdf5storage
 #. pathlib
 #. scipy
 #. matplotlib
 #. PyQt5


----------
How to run
----------

To use the GUI directly execute the module :

.. code::
    python -m cicada


-------------
Documentation
-------------

Documentation of PyCICADA can be found `here <https://pycicada.readthedocs.io/>`_.

--------
Contacts
--------

Contacts : 

-------
LICENSE
-------

Copyright (c) 2019 cossart lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
