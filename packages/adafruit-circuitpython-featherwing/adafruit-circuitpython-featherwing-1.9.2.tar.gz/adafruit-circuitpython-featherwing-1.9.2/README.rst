
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-featherwing/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/featherwing/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_FeatherWing.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_FeatherWing
    :alt: Build Status

This library provides FeatherWing specific classes for those that require a significant amount of
initialization.

Dependencies
=============
These drivers depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `INA219 <https://github.com/adafruit/Adafruit_CircuitPython_INA219>`_
* `Seesaw <https://github.com/adafruit/Adafruit_CircuitPython_seesaw>`_
* `HT16K33 <https://github.com/adafruit/Adafruit_CircuitPython_HT16K33>`_
* `DotStar <https://github.com/adafruit/Adafruit_CircuitPython_DotStar>`_
* `NeoPixel <https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel>`_
* `DS3231 <https://github.com/adafruit/Adafruit_CircuitPython_DS3231>`_
* `ST7735R <https://github.com/adafruit/Adafruit_CircuitPython_ST7735R>`_
* `ADXL34x <https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x>`_
* `ADT7410 <https://github.com/adafruit/Adafruit_CircuitPython_ADT7410>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_ and highly recommended over
installing each one.

Installing from PyPI
--------------------

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-featherwing/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-featherwing

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-featherwing

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-featherwing

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_featherwing/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-featherwing --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
