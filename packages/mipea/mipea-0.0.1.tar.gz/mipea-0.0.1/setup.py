from setuptools import setup, Extension

with open("README.md") as f:
    long_description = f.read()

gpio = Extension(
    "mipea.gpio",
    sources = ["mipea/gpiomodule.c"],
    libraries = ["mipea"],
    language = "c"
)

setup(
    name = "mipea",
    version = "0.0.1",
    description = "lightning fast peripheral access on the Raspberry Pi using a mipea wrapper written in C",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = "c peripheral access Raspberry Pi mipea",
    author = "jasLogic",
    author_email = "jaslo@jaslogic.tech",
    url = "https://github.com/jasLogic/mipeapy",
    project_urls = {
        "Bug Tracker": "https://github.com/jasLogic/mipeapy/issues",
        "Source Code": "https://github.com/jasLogic/mipeapy",
        "Download": "https://github.com/jasLogic/mipeapy/releases"
    },
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: C",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware"
    ],

    packages = ["mipea"],
    ext_modules = [gpio],
)
