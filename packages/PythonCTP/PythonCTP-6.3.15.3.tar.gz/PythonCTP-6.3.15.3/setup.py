import codecs
import os
import sys
import setuptools

try:
    from setuptools import setup
except:
    from distutils.core import setup
  
  
NAME = "PythonCTP"
 
DESCRIPTION = "This is the Python CTP API for trading domestic Futures."
  
LONG_DESCRIPTION = ""
  
KEYWORDS = "CTP Python API"
  
AUTHOR = "jingse"
  
AUTHOR_EMAIL = "pjjing@foxmail.com"

URL = "https://github.com/nicai0609/Python-CTPAPI"
  
VERSION = "6.3.15.3"

LICENSE = "MIT"
  
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    install_requires=[
    ''],
    python_requires='>=3.7.2',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
)