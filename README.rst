=========================
 Python Daemonizer Class
=========================

|ci| |wheels| |release| |badge| |coverage|

|pre| |reuse| |cov| |pylint|

|tag| |license| |python| |plat|

This is a Python class that will daemonize your Python script so it can
continue running in the background. It works on Unix, Linux and OS X,
creates a PID file and has standard commands (start, stop, restart) plus
a foreground mode.

Based on `this original version from jejik.com`_.

.. _this original version from jejik.com: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

Quick Start
===========

Usage
-----

Define a class which inherits from ``Daemon`` and has a ``run()`` method
(which is what will be called once the daemonization is completed).

.. code-block:: python

  from daemonizer import Daemon


  class pantalaimon(Daemon):
      def run(self):
          do_mything()


Depending on what your code is doing, you may also want to subclass the
``cleanup()`` method to close sockets, etc (called after ``stop()`` and
before termination).

Create a new object of your class, specifying where you want your PID
file to exist:

.. code-block:: python

  pineMarten = pantalaimon("/path/to/pid.pid")
  pineMarten.start()


Actions
-------

* ``start`` - start the daemon (create PID and daemonize)
* ``stop`` - stop the daemon (stop the child process and remove the PID)
* ``restart`` - run ``stop`` then ``start``
* ``status`` - show daemon status

Foreground
----------

This is useful for debugging because you can start the code without
making it a daemon. The running script then depends on the open shell
like any normal Python script.

To do this, just call the ``run()`` method directly instead of ``start()``:

.. code-block:: python

  pineMarten.run()

Continuous execution
--------------------

The ``run()`` method will be executed just once so if you want the
daemon to be doing stuff continuously you may wish to use the schedule_
module to execute code snippets repeatedly (examples_). For daemon
examples see the next section.

.. _schedule: https://pypi.org/project/schedule/
.. _examples: https://schedule.readthedocs.io/en/stable/examples.html
.. _script: https://github.com/sarnold/pyserv/blob/master/scripts/httpdaemon

Consumer examples
~~~~~~~~~~~~~~~~~

Pyserv_ is a growing collection of threaded Python server bits, including
custom `HTTP server`_ and WSGI_ classes, along with corresponding console
entry points and some daemon scripts. The latest addition includes an async
version of the original tftpy-based daemon script.

The ``httpdaemon``, ``atftpdaemon``, and ``tftpdaemon`` commands are
stand-alone `Python daemon`_ scripts with the same core server code, as
well as a default user configuration adjustable via environment
variables.

.. _Pyserv: https://github.com/sarnold/pyserv
.. _HTTP server: https://docs.python.org/3/library/http.server.html
.. _WSGI: https://docs.python.org/3/library/wsgiref.html
.. _Python daemon: https://github.com/sarnold/python-daemonizer

Install with pip
----------------

This updated version is *not* published on PyPI, thus use one of the
following commands to install the latest python-daemonizer in a Python
virtual environment on any platform.

From source::

  $ python3 -m venv env
  $ source env/bin/activate
  $ pip install git+https://github.com/sarnold/python-daemonizer.git

The alternative to python venv is the Tox_ test driver.  If you have it
installed already, clone this repository and try the following commands
from the python-daemonizer source directory.

To install in dev mode and run the tests::

  $ tox -e py

To run pylint::

  $ tox -e lint


.. note:: After installing in dev mode, use the environment created by
          Tox just like any other Python virtual environment.  The dev
          install mode of Pip allows you to edit the script and run it
          again while inside the virtual environment. By default Tox
          environments are created under ``.tox/`` and named after the
          env argument (eg, py).


To install the latest release, eg with your own ``tox.ini`` file in
another project, use something like this::

  $ pip install https://github.com/sarnold/python-daemonizer/releases/download/0.4.0/daemonizer-0.4.0-py3-none-any.whl

That said, the "proper" form for git-based dependencies would be more like
this::

  daemonizer @ git+https://github.com/sarnold/python-daemonizer.git@0.4.1#69d4c9b6f3916cd5ae87c8b3a78eca1015eeed0f


.. _Tox: https://github.com/tox-dev/tox


Pre-commit
----------

This repo is now pre-commit_ enabled for python/rst source and file-type
linting. The checks run automatically on commit and will fail the commit
(if not clean) and perform simple file corrections.  For example, if the
mypy check fails on commit, you must first fix any fatal errors for the
commit to succeed. That said, pre-commit does nothing if you don't install
it first (both the program itself and the hooks in your local repository
copy).

You will need to install pre-commit before contributing any changes;
installing it using your system's package manager is recommended,
otherwise install with pip into your usual virtual environment using
something like::

  $ sudo emerge pre-commit  --or--
  $ pip install pre-commit

then install it into the repo you just cloned::

  $ git clone https://github.com/sarnold/python-daemonizer
  $ cd python-daemonizer/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    $ pre-commit autoupdate

Most (but not all) of the pre-commit checks will make corrections for you,
however, some will only report errors, so these you will need to correct
manually.

Automatic-fix checks include ffffff, isort, autoflake, and miscellaneous
file fixers. If any of these fail, you can review the changes with
``git diff`` and just add them to your commit and continue.

If any of the mypy, bandit, or rst source checks fail, you will get a report,
and you must fix any errors before you can continue adding/committing.

To see a "replay" of any ``rst`` check errors, run::

  $ pre-commit run rst-backticks -a
  $ pre-commit run rst-directive-colons -a
  $ pre-commit run rst-inline-touching-normal -a

To run all ``pre-commit`` checks manually, try::

  $ pre-commit run -a


SBOM and license info
=====================

This project is now compliant with the REUSE Specification Version 3.3, so the
corresponding license information for all files can be found in the ``REUSE.toml``
configuration file with license text(s) in the ``LICENSES/`` folder.

Related metadata can be (re)generated with the following tools and command
examples.

* reuse-tool_ - REUSE_ compliance linting and sdist (source files) SBOM generation
* sbom4python_ - generate SBOM with full dependency chain

Commands
--------

Use tox to create the environment and run the lint command::

  $ tox -e reuse                      # --or--
  $ tox -e reuse -- spdx > sbom.txt   # generate sdist files sbom

Note you can pass any of the other reuse commands after the ``--`` above.

Use the above environment to generate the full SBOM in text format::

  $ source .tox/reuse/bin/activate
  $ sbom4python --system --use-pip -o <file_name>.txt

Be patient; the last command above may take several minutes. See the
doc links above for more detailed information on the tools and
specifications.

.. _pre-commit: https://pre-commit.com/index.html
.. _reuse-tool: https://github.com/fsfe/reuse-tool
.. _REUSE: https://reuse.software/spec-3.3/
.. _sbom4python: https://github.com/anthonyharrison/sbom4python


.. |ci| image:: https://github.com/sarnold/python-daemonizer/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/python-daemonizer/actions/workflows/ci.yml
    :alt: CI Status

.. |wheels| image:: https://github.com/sarnold/python-daemonizer/actions/workflows/wheels.yml/badge.svg
    :target: https://github.com/sarnold/python-daemonizer/actions/workflows/wheels.yml
    :alt: Wheel Status

.. |coverage| image:: https://github.com/sarnold/python-daemonizer/actions/workflows/coverage.yml/badge.svg
    :target: https://github.com/sarnold/python-daemonizer/actions/workflows/coverage.yml
    :alt: Coverage workflow

.. |badge| image:: https://github.com/sarnold/python-daemonizer/actions/workflows/pylint.yml/badge.svg
    :target: https://github.com/sarnold/python-daemonizer/actions/workflows/pylint.yml
    :alt: Pylint Status

.. |release| image:: https://github.com/sarnold/python-daemonizer/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/python-daemonizer/actions/workflows/release.yml
    :alt: Release Status

.. |cov| image:: https://raw.githubusercontent.com/sarnold/python-daemonizer/badges/master/test-coverage.svg
    :target: https://github.com/sarnold/python-daemonizer/
    :alt: Test coverage

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/python-daemonizer/badges/master/pylint-score.svg
    :target: https://github.com/sarnold/python-daemonizer/actions/workflows/pylint.yml
    :alt: Pylint score

.. |reuse| image:: https://api.reuse.software/badge/git.fsfe.org/reuse/api
    :target: https://api.reuse.software/info/git.fsfe.org/reuse/api
    :alt: REUSE status

.. |license| image:: https://img.shields.io/badge/license-CC--BY--SA--3.0-blue
    :target: https://github.com/sarnold/python-daemonizer/blob/master/LICENSE
    :alt: License

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/python-daemonizer?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/python-daemonizer/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.9+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python

.. |plat| image:: https://img.shields.io/badge/platforms-POSIX-blue.svg
    :target: https://github.com/sarnold/python-daemonizer/
    :alt: Platform

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
