.. title:: ldrand

ldrand
======

.. image:: https://readthedocs.org/projects/ldrand/badge/?version=latest&style=plain
    :target: https://ldrand.readthedocs.org

A basic linker wrapper that randomizes the link order. This can be used for compiling benchmarked programs to
reduce the impact of specific link orders on the benchmarking results.

Not all linking orders might work, due to dependencies, therefore ``ldrand`` currently tries a new linking order
until it succeeds (or the maximum number of tries is reached which is current set to 10 but can be configured
via the environment variable ``LDRAND_TRIES``).

Installation
------------

.. code:: sh

    pip3 install ldrand


Usage
-----

Calling the ``ldrandp`` command returns the path of the ``bin`` folder that contains the script that masks the ``ld``
tool. Setting the wrapped linker explicitly is supported by setting the environment variable ``LDRAND_LINKER``.

A typical usage would look like:

.. code:: sh

    PATH="`ldrandp`:$PATH" make

    # Or with an explicit linker
    PATH="`ldrandp`:$PATH" LDRAND_LINKER="/usr/bin/custom_linker/ld" make


Contributing
------------

`Bug reports <https://github.com/parttimenerd/ldrand/issues>`_ and
`Code contributions <https://github.com/parttimenerd/ldrand>`_ are highly appreciated.
