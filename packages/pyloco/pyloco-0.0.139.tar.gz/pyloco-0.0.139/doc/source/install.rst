..  -*- coding: utf-8 -*-

.. _Installation:

Installation
==================================

To install pyloco, first open a terminal and run shell command(s) as explained
below. ">>>" in example boxes means a command prompt. Your terminal may show
different prompt.

Obviously, you need to have a version of Python installed on your computer.
pyloco supports Python version 2.7 and 3.5 and later. pyloco is tested on
Windows, macOS, and Linux.

New installation
----------------

pyloco is a pure Python program. As usual, we can use pip to install pyloco like below

.. code-block:: bash

    >>> pip install --user pyloco
    >>> pyloco --version
    pyloco 0.1.0

I used "- -user" option to install pyloco to the user site. If you are using virtual
environment, it would be safe to remove "- -user" option. In case that you want to 
install pyloco to the system site, remove "- -user" option too.


Upgrading pyloco
----------------

If pyloco is already installed, you can upgrade pyloco using following command.

.. code-block:: bash

    >>> pip install -U pyloco
    >>> pyloco --version
    pyloco 0.2.0


Installing pyloco task
-----------------------

pyloco is an application platform on that you can build and run Python 
application, or task in pyloco terms. You can also use pyloco to install
a pyloco task from a pyloco task repository as shown below.

.. code-block:: bash

    >>> pyloco install yourtask
    >>> pyloco <yourtask> -h 
    <yourtask> version X.X.X

Please visit :ref:`pylocorepo` to see what tasks are available.

To see a list of tasks installed on your computer, please use following command.

.. code-block:: bash

    >>> pyloco -l

What to do next 
---------------

* :ref:`pylocorepo`
* :ref:`Tutorials`
* :ref:`Examples`
* :ref:`Pyloco commands`
* :ref:`API Reference`

