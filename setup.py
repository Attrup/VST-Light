from setuptools import setup

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="VSTLight",
    version="0.1.0",
    description="Python package for seamless control of network-compatible "
    + "VLP light controllers from VS Technology.",
    long_description=readme,
    url="https://github.com/Attrup/VST-Light",
    author="Jonas Attrup",
    author_email="attrup.jonas@gmail.com",
    license=license,
    package_dir={"": "src"},
    packages=["VSTLight"],
)
