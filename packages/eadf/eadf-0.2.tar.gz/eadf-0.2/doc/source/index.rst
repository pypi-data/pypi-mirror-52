.. EADF documentation master file, created by
   sphinx-quickstart on Mon Aug 19 13:54:30 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Modelling Antenna Arrays with the EADF
======================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

.. automodule:: eadf

.. toctree::
   :maxdepth: -1
   :hidden:

   class

.. toctree::
   :maxdepth: -1
   :hidden:

   arrays

.. toctree::
   :maxdepth: -1
   :hidden:

   core

.. toctree::
   :maxdepth: -1
   :hidden:

   importers

.. toctree::
   :maxdepth: -1
   :hidden:

   plotting


Features
--------

This package allows to **import** measurement data that represents beam patterns of
antenna arrays, you can **export** these to a more convenient format. It handles
**interpolation** along the frequencies the antenna array was excited with and can also
deal with irregularly sampled beampatterns, so it can **interpolate** along
azimuth and co-elevation. Moreover one can **compress** beampatterns by truncating
their representation in the spatial Fourier domain.

Performance
-----------

Since this package is mainly for academic purposes, we do not aim at the highest
level of optimization. Instead we try to provide clean, readable and nicely
structured code. Algorithmic optimizations are always welcome, if they are
sufficiently motivated and documented in the implementation or some publication.

Moreover we have found out that for most purposes it is sufficient to just use
the `Intel Python Distribution <https://software.intel.com/en-us/distribution-for-python>`_,
which can be installed and used alongside any conventional CPython distribution. It is
automatically optimized for modern CPU instruction sets. For instance Numpy operations are
implemented using SIMD and SMP, which would require a huge manual effort to replicate.
For example putting the following into a file

>>> import eadf.arrays
>>> import eadf.core
>>> A = eadf.arrays.generateStackedUCA(11, 3, 1.5, 0.5)
>>> arrAzi, arrEle = eadf.core.anglesToGrid(
>>>     *eadf.core.sampleAngles(240, 120)
>>> )
>>> A.sample(arrAzi, arrEle, 1)

and changing nothing but the Python executable, yields the following:

>>> [user@pc EADF]$ time python/intelpython3 profiler.py
>>> real	0m51,424s/0m6,250s
>>> user	0m49,874s/0m8,469s
>>> sys	    0m0,485s/0m2,842s

Note that in this example we evaluate the beampattern at 28800 distinct
angular locations.

References
----------

*Efficient antenna description for MIMO channel modelling and estimation*, M. Landmann, G. Del Galdo; 7th European Conference on Wireless Technology; Amsterdam; 2004; `IEEE Link <https://ieeexplore.ieee.org/document/1394809>`_

*Geometry-based Channel Modeling for Multi-User MIMO Systems and Applications*, G. Del Galdo; Dissertation, Research Reports from the Communications Research Laboratory at TU Ilmenau; Ilmenau; 2007 `Download <https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00014957/ilm1-2007000136.pdf>`_

*Limitations of Experimental Channel Characterisation*, M. Landmann; Dissertation; Ilmenau; 2008 `Download <https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00015967/ilm1-2008000090.pdf>`_
