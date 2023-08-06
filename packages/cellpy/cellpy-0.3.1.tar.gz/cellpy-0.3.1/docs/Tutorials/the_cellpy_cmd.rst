The cellpy command
==================

At the moment, only a very limited set of things can be achieved by running
the ``cellpy`` command at the shell (or in the cmd window).

.. code-block:: shell

    $ cellpy
    Usage: cellpy [OPTIONS] COMMAND [ARGS]...

    Options:
     --help  Show this message and exit.

    Commands:
      info   This will give you some valuable information about your cellpy.
      pull   Download examples or tests from the big internet.
      run    Will in the future be used for running a cellpy process.
      setup  This will help you to setup cellpy.


A couple of commands are implemented to get some information about your
cellpy environment (currently getting your
cellpy version and the location of your configuration file):

.. code-block:: shell

    $ cellpy info --version
    [cellpy] version: 0.3.0

    $ cellpy info --configloc
    [cellpy] ->C:\Users\jepe\_cellpy_prms_jepe.conf


The most important command is probably the ``setup`` command (that should be run
when you install cellpy for the first time).

.. code-block:: shell

    $ cellpy setup --interactive

