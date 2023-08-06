import os
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(__file__ + "/../")

# The text of the README file
README = HERE + "\\" + "README.md"

with open(README, "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="manolyamailsender",
    version="0.0.2",
    author="Umut Ucok",
    author_email="ucok.umut@gmail.com",
    description="Simple mail sender",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["manolyamailsender"],
)