import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="didyoumean3",
    version="0.1.2",
    description="\"Did You Mean?\" suggestions for your Python3 projects.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PLNech/didyoumean3",
    author="PLNech",
    author_email="github+didyoumean@plnech.fr",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["bs4"],
    entry_points={
        "console_scripts": [
            "didyoumean=didyoumean.__main__:main",
        ]
    },
)