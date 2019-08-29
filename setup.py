#!usr/bin/env python

from setuptools import setup, find_packages

setup(name="kcimc",
	version="0.1",
	description="Test for pip install git+",
	url="https://github.com/kylemcdonald/python-utils",
   install_requires=["numpy", "python-opencv", "subprocess", "os", "Pillow", "shutil", "sys", "multiprocessing", "collections", "iterutils", "time"],
	packages=find_packages(),
	)