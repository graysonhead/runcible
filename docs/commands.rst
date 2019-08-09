Usage
=====

Runcible commands can take up to 3 positional arguments:

``runcible [target] [func] [value]``

Target Selection
----------------

The ``target`` positional argument accepts a regular expression that selects a set of devices as defined in your dataset.

For example, given a set of devices [dc1-spine, dc1-core, dc2-spine, dc2-core], the target ``dc1-.*`` would select the
subset [dc1-spine, dc1-core].

To target all devices, use a regular expression of ``.*``. For more information on regular expressions, see
https://docs.python.org/3/library/re.html#regular-expression-syntax .


Functions
---------

Functions determine what action Runcible will take against the target devices. This function is a need string (see
:ref:`need` for more information.)

.. _special_functions:

Special Functions
-----------------

Special functions are needs that have special behavior, they are listed below:

- ``apply``: Apply will compare the desired state with the current state and idempotency apply changes to targeted devices.
- ``cstate.GET``: Dumps the current state of targeted devices.