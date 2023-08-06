# generates documentation of pyloco commands
# pyloco commands consist of management tasks and standard tasks


# get a list of builtin-commands
import os
import pydoc
import pyloco.mgmttask
import pyloco.stdtask

index_rst = """..  -*- coding: utf-8 -*-

.. _Pyloco commands:

Pyloco commands
==================================

Pyloco commands are built-in pyloco tasks.

Task management commands
----------------------------------

{mgmttasks}

.. toctree::
    :hidden:
    :maxdepth: 1

{mgmtindices}

Standard task commands
----------------------------------

{stdtasks}

.. toctree::
    :hidden:
    :maxdepth: 1

{stdindices}

"""

here = os.path.dirname(__file__)
outdir = os.path.join(here, "source", "commands")

mgmttasks = []
stdtasks = []
mgmtindices = []
stdindices = []

for name, task in pyloco.mgmttask.mgmt_tasks.items():
    command = "command-%s" % name
    label = ".. _%s:\n\n" % command
    pyloco.perform("help", [name, "-t", "{task_name}", "-n", label, "-o",
                   os.path.join(outdir, name+"-task.rst")])
    oneliner, _ = pydoc.splitdoc(task.__doc__)
    mgmttasks.append("* :ref:`%s<%s>` : %s" % (name, command, oneliner))
    mgmtindices.append(" "*4 + name + "-task")

for name, task in pyloco.stdtask.standard_tasks.items():
    command = "command-%s" % name
    label = ".. _%s:\n\n" % command
    pyloco.perform("help", [name, "-t", "{task_name}", "-n", label, "-o",
                   os.path.join(outdir, name+"-task.rst")])
    oneliner, _ = pydoc.splitdoc(task.__doc__)
    stdtasks.append("* :ref:`%s<%s>` : %s" % (name, command, oneliner))
    stdindices.append(" "*4 + name + "-task")

with open(os.path.join(outdir, "index.rst"), "w") as f:
    m = "\n".join(mgmttasks)
    s = "\n".join(stdtasks)
    f.write(index_rst.format(mgmttasks=m, stdtasks=s,
            mgmtindices="\n".join(mgmtindices),
            stdindices="\n".join(stdindices)))

    #f.write("\n\n.. END\n")
