import os
import subprocess

from setuptools import find_packages
from setuptools import setup

try:
    from packaging.version import parse as parse_version
except ImportError:
    parse_version = None


REQUIREMENTS = [
    "Click>=7.0,<=8",
    "markdown2>=2.3.8,<2.4",
    "numpy>=1.17.2,<1.18",
    "peewee>=3.10.0,<3.11",
    "Pillow>=6.1.0,<6.2",
    "PyYAML>=5.1.2,<5.2",
]


with open("README.md", "r") as f:
    long_description = f.read()


def version_from_git_tag():
    if parse_version is None:
        return "DEV"
    version = "0.0.1"
    r = subprocess.run(["git", "-C", os.path.dirname(__file__), "tag", "-l"], capture_output=True)
    if not r.returncode:
        tags = [t.replace("release-", "") for t in r.stdout.decode().strip().split("\n")]
        tags.sort(key=lambda v: parse_version(v), reverse=True)
        version = tags[0]
    with open(os.path.join(os.path.dirname(__file__), "rmnl", "htg", "VERSION"), "w") as fp:
        fp.write(version)
    return version


setup(
    author="Roel Meurders",
    author_email="pypi+htg@rmnl.net",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    description="Happy Tree Gallery is a command line utility generating " "static photo galleries.",
    entry_points={"console_scripts": ["htg = rmnl.htg.htg:htg"]},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    keywords="development command line tool photos pictures management " "galleries json",
    license="MIT",
    long_description=long_description,
    maintainer="RMNL",
    name="happy-tree-gallery",
    namespace_packages=["rmnl"],
    packages=find_packages(),
    url="https://gitlab.com/rmnl/htg",
    version=version_from_git_tag(),
    zip_safe=False,
)
