Temporal UUID64
===============
A time-based 64-bit UUID generator. The basic idea behind is to provide a
universally unique identifier that satisfies the following conditions:

Installation
------------

.. code-block::

   pip install temporaluuid64

Technical Details
-----------------

The time-based UUID consists of two components: a timestamp and a node ID.

.. code-block::

    +----------------------+--------------------+
    |  48-bit (timestamp)  |  16-bit (node_id)  |
    +----------------------+--------------------+

Sort entities in chronological order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Entities given their UUIDs must be able to be sorted in chronological order
without relying on additional data fields. This is why the timestamp bits
occupy the most significant bits.

Suitable for distributed systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Even if multiple identifiers are created at the exactly same time, given a
particular granularity (generally a millisecond), the UUID generator must be
able to provide a way to avoid collisions.

