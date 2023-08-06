import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="spongebot",
    version="0.1.0",
    description="Monitor a directory for new files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SirSolim/spongebot",
    author="Nicolas Forstner",
    author_email="nicolasforstner@yahoo.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["spongebot"],
    include_package_data=True,
    install_requires=[],
)