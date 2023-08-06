##########
NDD Test4P
##########

|pipeline| |coverage|

.. |pipeline| image:: https://gitlab.com/ddidier/python-ndd-test4p/badges/master/pipeline.svg
    :target: https://gitlab.com/ddidier/python-ndd-test4p/commits/master
    :alt: Pipeline Status

.. |coverage| image:: https://gitlab.com/ddidier/python-ndd-test4p/badges/master/coverage.svg
    :target: https://gitlab.com/ddidier/python-ndd-test4p/commits/master
    :alt: Coverage Report


Utilities for testing Python code.

Documentation available at https://ddidier.gitlab.io/python-ndd-test4p/.


Requirements
============

- Python 3.6 requires PyYAML >= 3.13
- Python 3.7 requires PyYAML >= 5.1


Development
===========

The Python package manager is `PIP`_.

We strongly suggest that you use `VirtualEnv`_.
You could also use `VirtualEnvWrapper`_.

On Ubuntu 18.04:

.. code-block:: shell

    # install PIP and VirtualEnv
    sudo apt install -y python3-pip python3-venv

    # install VirtualEnvWrapper
    pip3 install virtualenvwrapper
    # you may put the following lines in your .bashrc
    export PATH=$PATH:$HOME/.local/bin
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    source ~/.local/bin/virtualenvwrapper.sh

    # clone the template repository
    git clone https://gitlab.com/ddidier/python-ndd-test4p

    # create and activate a VirtualEnv
    mkvirtualenv --python=python3 python-ndd-test4p
    workon python-ndd-test4p

    # install all the required dependencies
    pip install -e .
    pip install -e .[testing]
    pip install -e .[documenting]
    pip install -e .[distributing]

Test the library within your current environment:

.. code-block:: shell

    python setup.py test

Run the Python linters:

.. code-block:: shell

    pylint src/
    pylint --rcfile=.pylintrc-tests tests/

    flake8 src/
    flake8 --config=.flake8-tests tests/

Test the documentation examples:

.. code-block:: shell

    python setup.py doctest

Generate the documentation:

.. code-block:: shell

    python setup.py docs

Test the library within the supported environments:

.. code-block:: shell

    tox --parallel auto

Generate the Wheels package:

.. code-block:: shell

    python setup.py bdist_wheel


Notes
=====

This project has been set up using PyScaffold 3.2.1.
For details and usage information on PyScaffold see https://pyscaffold.org/.


References
==========

.. _PIP: https://en.wikipedia.org/wiki/Pip_(package_manager)
.. _VirtualEnv: https://virtualenv.pypa.io/
.. _VirtualEnvWrapper: https://virtualenvwrapper.readthedocs.io/

- `PIP`_
- `VirtualEnv`_
- `VirtualEnvWrapper`_
