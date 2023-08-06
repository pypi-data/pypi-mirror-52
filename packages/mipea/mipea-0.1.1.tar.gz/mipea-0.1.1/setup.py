from setuptools import setup, Extension

from distutils import ccompiler, sysconfig
from distutils.errors import CompileError, LinkError

from tempfile import TemporaryDirectory
import os
import sys

# check if the mipea C library is installed
code = """#include <mipea/gpio.h>
int main(void){if (gpio_map() < 0)return 1;gpio_unmap();return 0;}"""

print("checking for mipea... ", end="")
with TemporaryDirectory() as tmpdir:
    cfile = os.path.join(tmpdir, "test.c")
    binfile = os.path.join(tmpdir, "test")

    with open(cfile, "w") as f:
        f.write(code)

    compiler = ccompiler.new_compiler()
    sysconfig.customize_compiler(compiler)

    try:
        compiler.link(
            ccompiler.CCompiler.EXECUTABLE,
            compiler.compile([cfile], tmpdir),
            binfile,
            libraries = ["mipea"]
        )
    except (CompileError, LinkError) as e:
        print("error")
        print("ERROR:", str(e))
        print("""
The mipea C library is probably not installed, the library can be installed
from the source distribution or the repository accessible from:
    https://github.com/jasLogic/mipea
If the library is installed and there is still an error please open an issue
on GitHub:
    https://github.com/jasLogic/mipea/issues
        """)
        sys.exit()
    else:
        print("ok")

# write README.md to long_description
with open("README.md") as f:
    long_description = f.read()

# modules
gpio = Extension(
    "mipea.gpio",
    sources = ["mipea/gpiomodule.c"],
    libraries = ["mipea"],
    language = "c"
)

setup(
    # information
    name = "mipea",
    version = "0.1.1",
    description = "lightning fast peripheral access on the Raspberry Pi using a mipea wrapper written in C",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = "c peripheral access Raspberry Pi mipea gpio",
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

    # data
    include_package_data = True,

    # build
    packages = ["mipea"],
    ext_modules = [gpio],
)
