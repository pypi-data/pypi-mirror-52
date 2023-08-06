..  -*- coding: utf-8 -*-

.. _intro:

pyloco_ : Python Microapplication Framework
=============================================

.. only:: html

    :Release: |version|
..    :Date: |today|

.. warning::

    This version of pyloco is not for public users.
    Please expect changes in pyloco features. Some features explained
    in this document may not be available without notice.

pyloco is a framework for building, executing, and sharing microapplications.

Microapplication can be easily composed of other microapplications, which enables
incremental and loosely-coupled software development by nature. In essence,
microapplication is an application-version of microservice_ development technique.

One of key principles in pyloco is to view "using" an application is a type of
application development. A good example of this view would be Unix-pipe. With
Unix-pipe, a "power" user effectively creates a new application in a command line.

.. code-block:: bash

    >>> ls -l | wc -l
    19

In above example, a line of command lists files and subdirectories in current directory,
and counts the number of them. Only the last result is displayed on screen. By combining
multiple Unix utilities similar to this example, user can do lots of administration tasks
quickly as well as intuitively. 

Following the spirit of Unix-pipe, pyloco supports an extended version of Unix-pipe as
shown in following example.

.. code-block:: bash

    >>> pyloco 
    19

.. unix pipe-like usage
.. simple task creation
.. simple task extension
.. simple task ...


Let's try an example of typical pyloco way of application assembly.

.. code-block:: bash

    >>> pyloco docx2table my.docx -- table2xlsx -o table.xlsx

.. note:

    Visit `docx2xlsx`_ for a complete tutorial.

In above example, pyloco assembles two pyloco applications
(docx2table and table2xlsx) with "- -" (pyloco pipe), and lets the
newly assembled application work on "my.docx" to produce "table.xlsx"
as if there exists an assembled application from the beginning.

pyloco provides programmers with not only typical features that mature
application frameworks generally do, but also unique features that together
achieve a long-sought goal of software reuse.

* Strict and multi-level, but optional, type checking
* Customized index server for "programming by searching"
* Multi-language support in one source
* Unified and multi-purpose application package
* Websocket-enabled web application framework
* Standard features for high-quality applications

    * command-line interface
    * unit-testing
    * logging
    * multi-processing
    * document generation

.. toctree::
    :hidden:
    :maxdepth: 1

    getting-started
    install 
    tutorials/index
    examples/index
    commands/index
    task-design
    reference/index
    task-repository


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _pyloco: https://www.pyloco.net
.. _microservices: https://en.wikipedia.org/wiki/Microservices

