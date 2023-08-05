Help
====

Running

.. code-block:: bash

   $ latest --help


   usage: latest [-h] [--config CONFIG] [--output OUTPUT] template data

   A LaTeX-oriented template engine.

   positional arguments:
     template              path to template file.
     data                  path to data file.

   optional arguments:
     -h, --help            show this help message and exit
     --config CONFIG, -c CONFIG
                           path to configuration file; default to
                           ~/.latest/latest.cfg.
     --output OUTPUT, -o OUTPUT
                           path to output file; default to stdout.
