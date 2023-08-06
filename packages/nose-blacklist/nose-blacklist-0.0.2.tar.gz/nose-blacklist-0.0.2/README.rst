================
 nose-blacklist
================

.. image:: https://travis-ci.org/pglass/nose-blacklist.svg?branch=master
    :target: https://travis-ci.org/pglass/nose-blacklist

nose-blacklist is a plugin for nose_ that provides a powerful way of skipping
tests without requiring code changes.

- Test cases are excluded by regex matching
- Tests cases are matched by their fully-qualified names, including the module,
  class, and function/method names.
- Tests to skip can be sourced from one or more files, or from cli arguments


Quickstart
==========

.. code-block:: shell

    $ pip install nose-blacklist

    $ nosetests --with-blacklist \
        --blacklist=<pattern1> \
        --blacklist=<pattern2> \
        mytests/

Blacklist strings can be specified from one or more files. Blacklist files can
be used in conjunction with the ``--blacklist`` arguments.

.. code-block:: shell

    $ cat blacklist.txt
    test_thing
    # test_other_thing
    test_third_thing

    $ nosetests --with-blacklist \
        --blacklist-file=blacklist.txt \
        mytests/

The blacklist file should have a single pattern per line, as above. Any line
starting with a ``#`` is commented and will be ignored.


.. _nose: https://nose.readthedocs.org/en/latest/
