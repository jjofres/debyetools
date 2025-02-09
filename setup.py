# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="debyetools",
    version="2.8.2",
    description="Debye approximation implementation for the calculation of thermodynamic properties from ground-state atomistic simulations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://debyetools.readthedocs.io/",
    author="Javier Jofre",
    author_email="javier.jofre@polymtl.ca",
    license="GPLv3",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent"
    ],
    packages=["debyetools", "debyetools.tpropsgui", "debyetools.examples"],
    include_package_data=True,
    install_requires=["numpy", "scipy", "matplotlib", "mpmath", "PySide6", "deap"],
    package_data={
    'debyetools': ['examples/*', 'examples/*/*'],
},
)
