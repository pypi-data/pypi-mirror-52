from setuptools import Command, find_packages, setup
from setup_base import base_kwargs

setup(
    **base_kwargs,
    packages=find_packages(include=["mobikit_utils", "mobikit_utils.query_builder"]),
    install_requires=[]
)
