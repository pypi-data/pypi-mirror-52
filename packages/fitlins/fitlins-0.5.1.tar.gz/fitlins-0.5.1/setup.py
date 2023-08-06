#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" fitlins setup script """
from setuptools import setup

if __name__ == '__main__':
    """ Install entry-point """
    import versioneer
    from fitlins.__about__ import __version__, DOWNLOAD_URL

    cmdclass = versioneer.get_cmdclass()

    setup(
        name='fitlins',
        version=__version__,
        cmdclass=cmdclass,
        download_url=DOWNLOAD_URL,
    )
