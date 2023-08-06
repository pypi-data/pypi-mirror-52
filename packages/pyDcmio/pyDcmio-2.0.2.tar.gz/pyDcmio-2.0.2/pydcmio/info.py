#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Current version
version_major = 2
version_minor = 0
version_micro = 2

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(version_major, version_minor, version_micro)

# Expected by setup.py: the status of the project
CLASSIFIERS = ["Development Status :: 5 - Production/Stable",
               "Environment :: Console",
               "Environment :: X11 Applications :: Qt",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering",
               "Topic :: Utilities"]

# Project descriptions
description = """
DICOM managment package.
"""
SUMMARY = """
.. container:: summary-carousel

    pyDcmio is a Python module that can be used to play with DICOM file.
    This package offers:

    * pydcmio_dicomreader: can be use to read specific or registered dicom tags
      recursively.
    * pydcmio_splitseries: can be used to split DICOM files by serie names.
    * pydcmio_dicomanonymizer: can be used to anonymize DICOM files
      (experimental).
    * pydcmio_transcode: can be used to transcode the subject identifiers.
    * pydcmio_dicom2nifti: can be used to convert DICOM files in Nifti format.
"""
long_description = (
    "PYDCMIO: Python DiCoM IO\n\n"
    "[pydcmio] A Python project that provides a wrapping over the 'dcm2nii' "
    "and 'dcm2niix' commands, common tools to read and anonymize DICOM "
    "files, and transcoding features.\n")

# Main setup parameters
NAME = "pyDcmio"
ORGANISATION = "CEA"
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/neurospin/pydcmio"
DOWNLOAD_URL = "https://github.com/neurospin/pydcmio"
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "pyDcmio developers"
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "OS Independent"
ISRELEASE = True
VERSION = __version__
PROVIDES = ["pydcmio"]
REQUIRES = [
    "numpy>=1.6.1",
    "dicom>=0.9",
    "nibabel>=2.0.2",
    "progressbar2>=3.34.3"
]
EXTRA_REQUIRES = {}
SCRIPTS = [
    "pydcmio/scripts/pydcmio_deface_post",
    "pydcmio/scripts/pydcmio_deface_pre",
    "pydcmio/scripts/pydcmio_dicom2nifti",
    "pydcmio/scripts/pydcmio_dicomanonymizer",
    "pydcmio/scripts/pydcmio_dicomreader",
    "pydcmio/scripts/pydcmio_maskface",
    "pydcmio/scripts/pydcmio_nifti2dicom",
    "pydcmio/scripts/pydcmio_rtstruct",
    "pydcmio/scripts/pydcmio_splitseries",
    "pydcmio/scripts/pydcmio_transcode"
]
