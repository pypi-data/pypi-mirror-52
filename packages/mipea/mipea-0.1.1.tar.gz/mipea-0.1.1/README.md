[![GitHub](https://img.shields.io/github/license/jasLogic/mipeapy?color=blue)](https://github.com/jasLogic/mipeapy/blob/master/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jasLogic/mipeapy)](https://github.com/jasLogic/mipeapy/releases/)

# mipeapy: mipea Python wrapper

*Under construction*

This Python module makes use of the [mipea](https://github.com/jasLogic/mipea)
C library to access the peripherals of the Raspberry Pi.
The module is written in C and uses the Python C API.
Most functions are just wrappers to the mipea functions with conversion to
Python objects and some improvements.

Contributions are welcome (especially documentation or examples), please fork
and open a pull request.

Please add an issue if you find any bugs or have ideas for improvements.

Like the mipea C library, there are nearly **no checks performed** to protect
your Pi to archive best performance and because this is a
**library for developers**.
This library is useful to **lay a foundation for other programs or libraries**.

## Installation
You need to install the [mipea](https://github.com/jasLogic/mipea) C library to
use this library, see [README.md](https://github.com/jasLogic/mipea/blob/master/README.md)
for installation instructions.
* PyPI
        ```
        $ pip install mipea
        ```

* Source
        ```
        $ python setup.py install
        ```

## Usage
Look at the [examples](https://github.com/jasLogic/mipeapy/tree/master/examples) for some starting help.
