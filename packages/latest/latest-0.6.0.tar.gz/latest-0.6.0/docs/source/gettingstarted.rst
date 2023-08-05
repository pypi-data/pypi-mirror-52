Getting Started
===============


Basic Syntax
------------

With :math:`\LaTeX` syntax in mind, :mod:`latest` defines a
**command** and an **environment**.
But, first of all, let's see how to leverage all the power of
python in a template.

Python expressions
::::::::::::::::::

You can include a python expression within a template.
By default, the syntax is::

   {$ python expression $}

A python expression returns a python object, so if you want a string instead,
you can use the :mod:`latest` **command**.
For more complex tasks involving some logic like *for loops* or *conditionals*
you can refer to
:mod:`latest` **environment**.

Contexts
::::::::

An expression needs a context (like a python dictionary) to be evaluated.
A context is generally provided globally for a template.
This context object is passed to every python expression,
command or environment in the template.
However, commands and environments can modify the context
to work with in their content.


Commands
::::::::

The :mod:`latest` command let you automatically convert to a string
the output of a python expression.
By default, the syntax is::

   \latest[options]{$ python expression $}

For example, the expression::

   If a = \latest{$ a $} and b = \latest{$ b $}, then a + b = \latest{$ a+b $}

with a data context :code:`{'a': 1, 'b': 2}` evaluates to::

   If a = 1 and b = 2, then a + b = 3


Environments
::::::::::::

A :mod:`latest` environment allow us to change the globally defined context.
This can be useful for many purposes
depending on the context provided:

*  :code:`dict` context: to ease the access to names in the context
   for the python expressions, commands, or enviroments nested inside the
   environment
*  :code:`boolean` context: to provide a conditional functionality
*  :code:`list` context: to provide a loop functionality

By default, the syntax is::

   \begin{latest}{$ context $}[options]
        content...
   \end{latest}


Creating a template
-------------------

A template file can be of any type but :mod:`latest` searches in it for
:mod:`latest` **commands** and **enviroments**.


Creating a data file
--------------------

Data formats supported by :mod:`latest` are

* json
* yaml


The latest cli
--------------

Run :mod:`latest` script from the command line:: bash

    $ latest template data


where

    * **template** is the path to a template file
    * **data** is the path to a *json* or *yaml* formatted data file.


Example
-------

An example template file can be something like

.. literalinclude:: ../../test/res/template.tmpl
   :language: latex


while the data file can be something like (*yaml*)

.. literalinclude:: ../../test/res/data.yml
   :language: yaml


The expected output is

.. literalinclude:: ../../test/res/expected.tex
   :language: latex

