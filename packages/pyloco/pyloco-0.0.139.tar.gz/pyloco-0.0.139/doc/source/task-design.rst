..  -*- coding: utf-8 -*-

.. _task_design:

Task design
==================================

Writing a complex software generally requires additional effort to design
than a simple one. One common strategy is to split a complex functionality
of a software into multiple simpler units of programs. Tasks in pyloco 
naturally fit to this "divide-and-conqure" strategy as it is desinged to
be assembled together.

We suggests two high-level approaches for task decomposition. In following
sections, we will explain the details of the two approaches as well as
how you can use features of Pyloco to implement.

Action-oriented design
-----------------------

* focus on what software does
* software can be defined as a directed graph of actions


Data-oriented design
----------------------

* focus on what software produces
* software can be defined as a data flow
