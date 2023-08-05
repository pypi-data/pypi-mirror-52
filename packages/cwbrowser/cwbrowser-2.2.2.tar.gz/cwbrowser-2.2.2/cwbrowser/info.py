##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2018
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# cwbrowser current version
_version_major = 2
_version_minor = 2
_version_micro = 2


# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(
    _version_major, _version_minor, _version_micro)

# Expected by setup.py: the status of the project
CLASSIFIERS = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities"]

# Project descriptions
description = "Python package to request CubicWeb services."
SUMMARY = """
.. container:: summary-carousel

    CWBrowser is a Python module to **access data in a CubicWeb service** that
    offers:

    * a common API to send a request and if requested retrived the image data.
    * a common API to deal with genomic measures stored in PLINK format.
"""
long_description = """
=========
CWBrowser
=========

Python package to request CubicWeb services in order to get:

* eCRF data.
* imaging data: T1, T2, dMRI, fMRI, ...
* genotype data.
* processed data: FreeSurfer, MrTrix3, FSL, SPM, ...
"""

# Main setup parameters
NAME = "cwbrowser"
ORGANISATION = "CEA"
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/neurospin/rql_download.git"
DOWNLOAD_URL = "https://github.com/neurospin/rql_download.git"
LICENSE = "CeCILLB"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "{0} - {1}".format(MAINTAINER, MAINTAINER_EMAIL)
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "OS Independent"
VERSION = __version__
PROVIDES = ["cwbrowser"]
REQUIRES = [
    "paramiko>=2.6",
    "requests>=2.21"
]
EXTRA_REQUIRES = {}
