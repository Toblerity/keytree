from setuptools import setup, find_packages

version = "1.1.0"

try:
    desc = open("README.rst", "r").read()
except Exception:
    desc = ""

setup(
    name="keytree",
    version=version,
    description="KML utilities for the ElementTree API",
    long_description=desc,
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="KML etree ElementTree",
    author="Sean Gillies",
    author_email="sean.gillies@gmail.com",
    url="https://github.com/Toblerity/keytree",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
)
