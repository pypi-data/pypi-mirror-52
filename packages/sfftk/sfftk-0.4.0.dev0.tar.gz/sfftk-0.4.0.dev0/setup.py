# -*- coding: utf-8 -*-
# setup.py
import sys

from setuptools import setup, find_packages

from sfftk import SFFTK_VERSION

with open('README.rst') as f:
    long_description = f.read()

if sys.version_info[0] > 2:
    setup(
        name="sfftk",
        version=SFFTK_VERSION,
        packages=find_packages(),
        author="Paul K. Korir, PhD",
        author_email="pkorir@ebi.ac.uk, paul.korir@gmail.com",
        description="Toolkit for working with EMDB-SFF and other segmentation file formats",
        long_description=long_description,
        long_description_content_type='text/x-rst; charset=UTF-8',
        url="http://sfftk.readthedocs.io/en/latest/index.html",
        license="Apache License",
        keywords="EMDB-SFF, SFF, segmentation",
        setup_requires=["numpy"],
        install_requires=["ahds==0.2.0.dev0", "lxml", "h5py>2.7.0", "RandomWords", "styled", "mrcfile", "bitarray", "requests",
                          "mock",
                          "numpy-stl", "styled"],
        classifiers=[
            # maturity
            'Development Status :: 2 - Pre-Alpha',
            # environment
            'Environment :: Console',
            # audience
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            # license
            'License :: OSI Approved :: Apache Software License',
            # python version
            'Programming Language :: Python :: 2.7',
        ],
        entry_points={
            'console_scripts': [
                'sff = sfftk.sff:main',
            ]
        },
    )
else:
    setup(
        name="sfftk",
        version=SFFTK_VERSION,
        packages=find_packages(),
        author="Paul K. Korir, PhD",
        author_email="pkorir@ebi.ac.uk, paul.korir@gmail.com",
        description="Toolkit for working with EMDB-SFF and other segmentation file formats",
        long_description=long_description,
        long_description_content_type='text/x-rst; charset=UTF-8',
        url="http://sfftk.readthedocs.io/en/latest/index.html",
        license="Apache License",
        keywords="EMDB-SFF, SFF, segmentation",
        setup_requires=["numpy<1.17"],
        install_requires=["ahds==0.2.0.dev0", "lxml", "h5py>2.7.0", "requests", "bitarray",
                          "numpy-stl", "backports.shutil_get_terminal_size", "mock", "mrcfile",
                          "matplotlib<3.0", "scipy<1.2", "RandomWords", "styled", "networkx<2.3"],
        classifiers=[
            # maturity
            'Development Status :: 2 - Pre-Alpha',
            # environment
            'Environment :: Console',
            # audience
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            # license
            'License :: OSI Approved :: Apache Software License',
            # python version
            'Programming Language :: Python :: 2.7',
        ],
        entry_points={
            'console_scripts': [
                'sff = sfftk.sff:main',
            ]
        },
    )
