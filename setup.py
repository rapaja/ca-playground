"""CA-PLAYGROUND setup module."""

from setuptools import setup, find_namespace_packages
import pathlib

project_dir = pathlib.Path(__file__).parent.resolve()
long_description = (project_dir / "README.md").read_text(encoding="utf-8")


def read_package_version():
    """Read package version from the root '__init__.py' file."""
    with open(project_dir / "ca_playground/__init__.py", "r") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                delimiter = '"' if '"' in line else "'"
                return line.split(delimiter)[1]


setup(
    name="CA Playground",
    version=read_package_version(),
    description="CA Playground.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rapaja/ca-playground",
    author="Milan R. Rapaić | Kabinet 505",
    packages=find_namespace_packages(include=["ca_playground.*"]),
    install_requires=[],
)
