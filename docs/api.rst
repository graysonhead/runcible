.. _api:

API
===

.. _api_example:

API Device Example
------------------

Create a dict representing the desired state of your device (In this case, a switch using the Cumulus provider)

.. code-block:: python

    from runcible.api import Device, CBType
    conf = {
        "meta": {
            "device": {
                "ssh": {
                    "hostname": "192.168.122.41",
                    "username": "cumulus",
                    "password": "CumulusLinux!",
                },
                "default_management_protocol": "ssh",
                "driver": "cumulus"
            }
        },
        "system": {
            "hostname": "switch-test"
        },
        "interfaces": [
            {"name": "swp1", "pvid": 22, "bpduguard": False},
            {"name": "swp2", "pvid": 23, "bpduguard": True, "portfast": True},
        ],
        "vlans": [
            {"id": 22},
            {"id": 23}
        ]
    }
    d = Device("switch1", conf)

The Device class provides two main methods, .plan() and .execute().

Plan generates a list of needs and displays them to the user as callbacks, execute applies those changes. Each can be
re-run without re-creating the instance as many times as desired, but you must run them in the order
.plan() -> .execute().

.. code-block:: python

    >>> d.plan()
    {'has_fatal': False, 'has_errors': False, 'log': [{'message': 'system needs no changes.', 'callback_type': 'INFO'}, {'message': 'interfaces needs:', 'callback_type': 'INFO'}, {'message': 'vlans needs:', 'callback_type': 'INFO'}]}
    >>> d.execute()
    {'has_fatal': False, 'has_errors': False, 'log': [{'message': 'interfaces.swp1.pvid.SET: 22', 'callback_type': 'SUCCESS'}, {'message': 'interfaces.swp2.pvid.SET: 23', 'callback_type': 'SUCCESS'}, {'message': 'interfaces.swp2.bpduguard.SET: True', 'callback_type': 'SUCCESS'}, {'message': 'interfaces.swp2.portfast.SET: True', 'callback_type': 'SUCCESS'}, {'message': 'vlans.module.CREATE: 20', 'callback_type': 'SUCCESS'}, {'message': 'vlans.module.CREATE: 4044', 'callback_type': 'SUCCESS'}]}


.. code-block:: python

    >>> d.plan()
    {'has_fatal': False, 'has_errors': False, 'log': [{'message': 'system needs no changes.', 'callback_type': 'INFO'}, {'message': 'interfaces needs no changes.', 'callback_type': 'INFO'}, {'message': 'vlans needs no changes.', 'callback_type': 'INFO'}]}
    >>> d.execute()
    {'has_fatal': False, 'has_errors': False, 'log': [{'message': 'No changes needed', 'callback_type': 'SUCCESS'}]}

If you don't want JSON callbacks, you can also change the callback method to terminal to show what the CLI will look
like.

.. code-block:: python

    >>> d = Device("switch1", conf, callback_method=CBMethod.TERMINAL)
    >>> d.plan()
    system needs no changes.
    interfaces needs:
    interfaces.swp1.pvid.SET: 22
    interfaces.swp2.pvid.SET: 23
    interfaces.swp2.bpduguard.SET: True
    interfaces.swp2.portfast.SET: True
    vlans needs:
    vlans.module.CREATE: 20
    vlans.module.CREATE: 4044
    >>> d.execute()
    interfaces.swp1.pvid.SET: 22
    interfaces.swp2.pvid.SET: 23
    interfaces.swp2.bpduguard.SET: True
    interfaces.swp2.portfast.SET: True
    vlans.module.CREATE: 20
    vlans.module.CREATE: 4044