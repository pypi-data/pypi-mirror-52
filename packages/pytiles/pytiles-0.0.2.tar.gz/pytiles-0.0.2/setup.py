from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version", "r") as vh:
    version=vh.read()

setup(
    name='pytiles',
    author="Kobe De Decker",
    author_email="kobededecker@gmail.com",
    description="python OGC WMS server",
    long_description=long_description,
    version=version,
    packages=find_packages(),
    install_requires=["rasterio"],
    url="",
    entry_points="""
        [console_scripts]
        pytiles=pytiles.pytiles:pytilesc
    """,
    license='MIT',
)