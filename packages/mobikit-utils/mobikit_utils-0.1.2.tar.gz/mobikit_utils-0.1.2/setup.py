from setuptools import Command, find_packages, setup
from setup_base import base_kwargs

setup(
    packages=find_packages(),
    install_requires=[
        "numpy~=1.16.2",
        "pandas~=0.24.2",
        "pytest~=4.4.1",
        "geopandas~=0.5.0",
        "geopy~=1.19.0",
        "psycopg2-binary~=2.8.2",
    ],
)
