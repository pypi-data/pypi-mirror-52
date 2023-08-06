# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Sqreen Python Native Module"""
import ctypes
import logging
import os
import sys

import pkg_resources

from .__about__ import __version__

LOGGER = logging.getLogger(__name__)


class C_PWVersion(ctypes.Structure):

    _fields_ = [
        ("major", ctypes.c_uint16),
        ("minor", ctypes.c_uint16),
        ("patch", ctypes.c_uint16)
    ]

    def as_tuple(self):
        """Return the version as a tuple."""
        return int(self.major), int(self.minor), int(self.patch)


def load_library(name):
    """Load a native library located in this module."""

    if os.name == "posix" and sys.platform == "darwin":
        ext = ".dylib"
    elif sys.platform == "win32":
        ext = ".dll"
    else:
        ext = ".so"
    fn = pkg_resources.resource_filename("sq_native", name + ext)
    if fn is None:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        fn = os.path.join(root_dir, name + ext)

    LOGGER.debug("Loading %s", fn)
    return ctypes.cdll.LoadLibrary(fn)


def get_major_version():
    """Return the major version of the binding."""
    return int(__version__.split(".")[0])


NOT_LOADED = object()
lib = NOT_LOADED


def get_lib():
    """Get an instance of the sqreen library."""
    global lib

    if lib is None or lib is NOT_LOADED:
        lib = load_library("libSqreen")
        lib.powerwaf_getVersion.argstype = []
        lib.powerwaf_getVersion.restype = C_PWVersion

        lib_version = lib.powerwaf_getVersion().major
        binding_version = get_major_version()
        if lib_version != binding_version:
            raise RuntimeError("Native library version mismatch: {} != {}"
                               .format(lib_version, binding_version))

    return lib


__all__ = ["load_library", "get_lib"]
