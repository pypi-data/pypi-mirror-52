# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='entoolkit',
    version='0.0.15',
    description='Epanet Toolkit Wrapper for Python',
    long_description=open('./README.md', encoding="utf8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/andresgciamtez/entoolkit',
    author='Andrés García Martínez',
    author_email='ppnoptimizer@gmail.com',   
    packages=['entoolkit'],
    include_package_data=True,             
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent"
		]
	)
