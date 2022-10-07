"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages

setup(
    name="snAIk",
    version="2.1.0",
    packages=find_packages(where="."),
    python_requires="==3.10.6",
    install_requires=[
        "numpy",
        "pygame",
        "pandas",
        "sagemaker",
        "sklearn",
        "tensorflow"
    ]
)