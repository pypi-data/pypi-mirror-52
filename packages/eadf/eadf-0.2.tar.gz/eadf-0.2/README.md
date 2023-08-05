[![Build Status](https://travis-ci.com/EMS-TU-Ilmenau/EADF.svg?branch=master)](https://travis-ci.com/EMS-TU-Ilmenau/EADF)
[![Documentation Status](https://readthedocs.org/projects/eadf/badge/?version=latest)](https://eadf.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/EMS-TU-Ilmenau/EADF/branch/master/graph/badge.svg)](https://codecov.io/gh/EMS-TU-Ilmenau/EADF)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/35012a6466c84592ba6d6bca146440e1)](https://www.codacy.com/app/SebastianSemper/EADF?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=EMS-TU-Ilmenau/EADF&amp;utm_campaign=Badge_Grade)
[![PyPI license](https://img.shields.io/pypi/l/eadf.svg)](https://pypi.python.org/pypi/eadf/)
[![PyPI format](https://img.shields.io/pypi/format/eadf.svg)](https://pypi.python.org/pypi/eadf/)
[![PyPI implementation](https://img.shields.io/pypi/implementation/eadf.svg)](https://pypi.python.org/pypi/eadf/)
[![PyPI version fury.io](https://badge.fury.io/py/eadf.svg)](https://pypi.python.org/pypi/eadf/)
[![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

## Motivation

Geometry-based MIMO channel modelling and a high-resolution parameter estimation are applications in which a precise description of the radiation pattern of the antenna arrays is required. In this package we implement an efficient representation of the polarimetric antenna response, which we refer to as the Effective Aperture Distribution Function (EADF). High-resolution parameter estimation are applications in which this reduced description permits us to efficiently interpolate the beam pattern to gather the antenna response for an arbitrary direction in azimuth and elevation. Moreover, the EADF provides a continuous description of the array manifold and its derivatives with respect to azimuth and elevation. The latter is valuable for the performance evaluation of an antenna array as well as for gradient-based parameter estimation techniques.

## Instructions

### Installation

Currently we simply have a source only distribution setup. To install the latest tagged release just use `pip install eadf`. Otherwise you can simply run
`pip install -e . --user` in your local git clone to get a development setup running.

### Documentation

We also have recent documentation on [readthedocs](https://eadf.rtfd.io). Locally you can build it your git clone via `python setup.py build_sphinx -E`.

## References

*Efficient antenna description for MIMO channel modelling and estimation*, M. Landmann, G. Del Galdo; 7th European Conference on Wireless Technology; Amsterdam; 2004; [IEEE Link](https://ieeexplore.ieee.org/document/1394809)

*Geometry-based Channel Modeling for Multi-User MIMO Systems and Applications*, G. Del Galdo; Dissertation, Research Reports from the Communications Research Laboratory at TU Ilmenau; Ilmenau; 2007; [Download](https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00014957/ilm1-2007000136.pdf)

*Limitations of Experimental Channel Characterisation*, M. Landmann; Dissertation; Ilmenau; 2008; [Download](https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00015967/ilm1-2008000090.pdf)
