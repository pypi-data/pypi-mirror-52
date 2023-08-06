..  -*- coding: utf-8 -*-

.. _Getting-started:

Getting-started
==================================

pyloco is an application framework written in Python. Its primary goal is to
help programmers to quickly build high-quality Python applications, or *tasks*
in pyloco terms. pyloco is inspired by Unix pipe and Unix commands, which are
arguably the most successful component-based programming model thus far. 

Before running examples in this page, please make sure that pyloco is
installed on your computer. You can run following pyloco command in a terminal
to verify pyloco installation. Please visit :ref:`Installation` for more information
about pyloco installation.

.. code-block:: bash

    >>> pyloco --version
    pyloco 0.1.0


First look
----------

Many pyloco tasks are already available online. One of them
is csvreadwrite that wraps Python csv standard library for easy use.

We will first install the pre-built csvreadwrite and run it using pyloco. Next,
we will build our-own csvreadwrite and upload it to Pyloco task repository for
sharing it with the world.

Installing pyloco task is as easy as following command.

.. code-block:: bash

    >>> pyloco install csvreadwrite

.. note::

    You can see a list of pyloco tasks available on your computer by running
    "pyloco -l" command in your terminal.

Let's create a simple data file in csv format. You may use a text editor to 
create the file.

.. code-block:: html
    :linenos:
    :caption: data.csv

    1,2,3
    2,3,4

Or you may use following command if you are on Linux.

.. code-block:: bash

    >>> printf '1,2,3\n4,5,6\n' > data.csv

Sometimes a delimiter in csv file causes confusion because not all csv files use
comma(,) as a delimiter as we used in data.csv. Let's generate a new csv
file with a different delimiter, say, space( ).

.. code-block:: bash

    >>> pyloco csvreadwrite data.csv --out-delimiter ' '
    1 2 3
    2 3 4

csvreadwrite has more features that make it easy to deal with csv file. Try
to run "pyloco csvreadwrite -h" or "pyloco help csvreadwrite" to see more
information about it. For now, let's move our focus to the way how to create
a pyloco task like csvreadwrite.

The simplest pyloco task
------------------------

Open your favorite text editor and copy following code in a file of
"csvreadwrite_v1.py".

.. code-block:: python
    :linenos:
    :name: csvreadwrite_v1 
    :caption: csvreadwrite_v1.py

    from pyloco import Task

    class CsvReadWrite(Task):

        def perform(self, targs):

            pass

Python code in "csvreadwrite_v1.py" shows a simplest pyloco task. Let's dig a
little with the code. Line 1 imports "Task" class from pyloco.
As shown in line 3, all pyloco tasks should
inherit from "Task". The only method that all pyloco task should implement is
"perform" method as shown in line 5. "targs" in line 5 delivers your-provided
command-line arguments to pyloco task. While the code is simple, the task is
already capable of many things such as command-line interface, :ref:`logging`,
:ref:`unittesting`,and :ref:`multiprocessing`, etc.

Above simple code have nothing to do with csv read/write. So, let's add csv
read/write logic using Python csv standard library as shown below.

Handling command-line arguments
-------------------------------

.. code-block:: python
    :linenos:
    :name: csvreadwrite_v2
    :caption: csvreadwrite_v2.py

    # -*- coding: utf-8 -*-
    """simple csv reader and writer"""

    import csv
    from pyloco import Task

    class CsvReadWrite(Task):

        def __init__(self, parent):

            self.add_data_argument("data", help="input csv file")

            self.add_option_argument("-o", "--output",
                                     help="output csv file")
            self.add_option_argument("--in-delimiter", default=",",
                                     help="input csv delimiter")
            self.add_option_argument("--out-delimiter", default=",",
                                     help="output csv delimiter")

        def perform(self, targs):

            with open(targs.data, "r", newline="") as csvin:
                reader = csv.reader(csvin, delimiter=targs.in_delimiter)

                if targs.output:
                    with open(targs.output, "w", newline="") as csvout:
                        writer = csv.writer(csvout, delimiter=targs.out_delimiter)

                        for row in reader:
                            writer.writerow(row)
                else:
                    for row in reader:
                        print(targs.out_delimiter.join(row))


"csvreadwrite_v2.py" can read user input file, change delimiter, and save
the modified data into a new csv file. To focus on the  usage of pyloco,
let's ignore csv-specific part of code. There is a new method of "__init__"
between line 9 and line 18. Four function calls of "add_data_argument" and
"add_option_argument" are added to register positional and optional command
line arguments. As you may be noticed, the two functions have almost identical
argument syntax to "add_argument" function in Python argparse standard
library. Usage of parsed arguments ("data", "output", "in_delimiter", and
"out_delimiter") are also the same to that of argparse.

Following command shows that delimiter is changed form "," to " ".

.. code-block:: bash

    >>> pyloco csvreadwrite_v2 data.csv --out-delimiter ' '
    1 2 3
    2 3 4

All pyloco task has typical features that high-quality software might have.
For examle following command shows help message of "csvreadwrite_v2.py" on
screen. To see what other features that "csvreadwrite_v2.py" already has,
please visit :ref:`logging`, :ref:`multiprocessing`, and :ref:`webapp`, etc.

.. code-block:: bash

    >>> pyloco csvreadwrite_v2.py -h

.. note:

    For verbose help, please run "pyloco csvreadwrite_v1.py --verbose" or
    "pyloco help csvreadwrite_v1.py"

::

    usage: pyloco CsvReadWrite [-h] [-o OUTPUT] [--in-delimiter IN_DELIMITER]
                               [--out-delimiter OUT_DELIMITER]
                               [--general-arguments]
                               data 
     
    positional arguments:
      data                  input csv file

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            output csv file
      --in-delimiter IN_DELIMITER
                            input csv delimiter
      --out-delimiter OUT_DELIMITER
                            output csv delimiter
      --general-arguments   Task-common arguments. Use --verbose to see a list of
                            general arguments


Assembling pyloco tasks
-------------------------------

Probably, the most distinct pyloco feature is that it can assemble multiple
pyloco tasks to build a larger task. Following example demonstrates
how easy to assemble pyloco tasks.

.. code-block:: python
    :linenos:
    :name: csvreadwrite_v3
    :caption: csvreadwrite_v3.py
    :emphasize-lines: 20, 24, 34, 38, 41

    # -*- coding: utf-8 -*-
    """simple csv reader and writer"""

    import csv
    from pyloco import Task

    class CsvReadWrite(Task):

        def __init__(self, parent):

            self.add_data_argument("data", help="input csv file")

            self.add_option_argument("-o", "--output",
                                     help="output csv file")
            self.add_option_argument("--in-delimiter", default=",",
                                     help="input csv delimiter")
            self.add_option_argument("--out-delimiter", default=",",
                                     help="output csv delimiter")

            self.register_forward("data", help="data to be forwarded to next task")

        def perform(self, targs):

            outdata = []

            with open(targs.data, "r", newline="") as csvin:
                reader = csv.reader(csvin, delimiter=targs.in_delimiter)

                if targs.output:
                    with open(targs.output, "w", newline="") as csvout:
                        writer = csv.writer(csvout, delimiter=targs.out_delimiter)

                        for row in reader:
                            outdata.append(row)
                            writer.writerow(row)
                else:
                    for row in reader:
                        outdata.append(row)
                        print(targs.out_delimiter.join(row))
                        
            self.add_forward(data=outdata)

A different color is used to emphasize new lines from v3. Important lines are line
20 and line 41. At line 20, the name of "data" is registered as forward-item,
which means that some data with the name of "data" will be *forwarded* to
next task. At line 41, actual data in "outdata" variable is binded to the
forwarded name of "data". In short, *forwarding* means: "pick a variable and
send it to next task." It is pyloco convention to use the name of "data" for
key input argument and forward data.

What is a good thing about this additional effort of forwarding?
It's substantial! Now a pyloco task has in-pipe (through command-line argument)
and out-pipe (through forwarding) that let data flow through between other
pyloco tasks. In fact, command-line argument in pyloco supports any Python
data type including user-defined objects such as class or function.

.. code-block:: bash

    >>> pyloco csvreadwrite_v3.py my.csv -- matplot

.. note::

    "matplot" is another pyloco task that wraps the famous matplotlib
    Python library. It can be installed on your computer by running
    "pyloco install matplottask" command on terminal.

<image of plot>


Uploading a pyloco task
-------------------------------

To make it easy to share your pyloco task with others, pyloco has its own
repository to keep those task. In addition, the repository
provides various services on top of core indexing capabililty.

* custom index server fully integrated with pyloco
* powerful task search engine that uses task meta-data
* auto-generated/customizable documentation per every task
* simple github-like version control
* built-in continuous integration test
* per-user promotion page

All the services listed above are freely available when you run a simple pyloco
command similar to following example. But first, please visit :ref:`pylocorepo` and
create a free account if you don't have your account yet on the server before uploading.

.. code-block:: bash

    >>> pyloco upload csvreadwrite_v3.py
    username:
    password:

.. note::

    Chances are somebody already uses the name of your pyloco task. In the case,
    please use "-n" options to give a new distribution name to your task similar
    to "pyloco upload <your pyloco task> -n '<new name>'".


What to do next
---------------

* `Task repository`_
* :ref:`Installation`
* :ref:`Tutorials`
* :ref:`Examples`
* :ref:`Pyloco commands`
* :ref:`API Reference`

.. _Task Repository: https://pyloco.org
