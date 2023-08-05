This is a port of `concurrent.futures`_ standard library module of Python 3.

There are different versions of the ``concurrent.futures`` code, for each version of Python 3.
This package contains the latest code from CPython master_ branch with small changes to make it compatible with both
Python 3.6 and Python 3.7.

It does not work with Python 2, but for that you can use pythonfutures_.

To install it, simply run::

    pip install futures3

To import it:

    .. code-block:: python

        from futures3.thread import ThreadPoolExecutor
        from futures3.process import ProcessPoolExecutor

.. _master: https://github.com/python/cpython/tree/master/Lib/concurrent/futures
.. _concurrent.futures: https://docs.python.org/3.8/library/concurrent.futures.html
.. _pythonfutures: https://github.com/agronholm/pythonfutures
