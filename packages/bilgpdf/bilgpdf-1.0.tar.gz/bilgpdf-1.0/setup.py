import setuptools
from pathlib import Path

setuptools.setup(
    name = "bilgpdf",
    version= 1.0,
    long_description = Path("informations\\README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"])
)