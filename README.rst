#########################################################
  python-libuuid - Faster UUID generation using libuuid
#########################################################

A Python C extension for faster generation of `UUID`_ objects. It supports
libuuid-based generation of version 1 and 4 UUIDs. The library is fully
compatible with the `standard uuid module`_, while also providing specialized,
optimized, functions for generating `UUID`_ strings.

``python-libuuid`` is roughly 8-10 times faster than the pure-python version.

It's basically just a thin `Cython`_ wrapper around `libuuid by Theo Tso`_.

.. _UUID: http://tools.ietf.org/html/rfc4122
.. _standard uuid module: http://docs.python.org/library/uuid.html
.. _libuuid by Theo Tso: http://git.kernel.org/?p=fs/ext2/e2fsprogs.git;a=tree;f=lib/uuid
.. _cython: http://cython.org/

Installation
------------

You can install ``python-libuuid`` either via the Python Package Index (PyPI)
or from source.

To install using ``pip``::

    $ pip install python-libuuid


To install using ``easy_install``::

    $ easy_install python-libuuid

If you have downloaded a source tarball you can install it by doing the
following,::

    $ python setup.py build
    # python setup.py install # as root


Usage / Examples
----------------

The ``libuuid`` module provides a similar interface to ``uuid``, resulting in fully
compatible UUID objects. ``libuuid.UUID`` is also a subclass of ``uuid.UUID``,
so existing code using ``isinstance`` will continue to work.

    >>> import libuuid
    >>> libuuid.uuid1()
    UUID('a3a32410-940a-11df-8ead-002219990fd7')

    >>> libuuid.uuid4()
    UUID('85651a1f-118f-480d-a116-526b2dd37322')

Furthermore, ``libuuid`` has a few extra utility functions not available in
``uuid``. These are handy when you don't need a "full" UUID object, but just
need the byte representation. The ``_bytes`` functions have less overhead than
the common interface.

    >>> libuuid.uuid1_bytes()
    '\x05f\xe1d\x94\x0b\x11\xdf\x8e\xad\x00"\x19\x99\x0f\xd7'

    >>> libuuid.uuid4_bytes()
    '\x05f\xe1d\x94\x0b\x11\xdf\x8e\xad\x00"\x19\x99\x0f\xd7'


Gotchas
-------

 * ``libuuid`` only provides random (version 4) and time based (version 1) UUIDs.

 * Calling ``libuuid.uuid1`` with `node` or `clock_seq` is not supported, and will
   silently fall back to the ``uuid.UUID`` implementation for compatibility.

 * Only tested on Linux. It should work on any platform, but e2fsprogs is
   probably just readily available on Linux distributions.


Bug tracker
-----------

If you have any suggestions, bug reports or annoyances please report using
the Github `issue tracker`_

.. _issue tracker: http://github.com/dln/python-libuuid/issues/


Contributing
------------

Development takes place at Github: http://github.com/dln/python-libuuid/

Patches and contributions are more than welcome.


License
-------

This software is licensed under the ``BSD`` software license.
See the ``LICENSE`` file in the top distribution directory for full license
text.


.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
