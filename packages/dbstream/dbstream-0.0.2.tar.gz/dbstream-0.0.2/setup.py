import os
import setuptools
from pip._internal.req import parse_requirements
from pip._internal.download import PipSession

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())


setuptools.setup(
    name="dbstream",
    version="0.0.2",
    author="Dacker",
    author_email="hello@dacker.co",
    description="A meta package to be connected to several databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dacker-team/dbstream",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[str(requirement.req) for requirement in requirements],
)
