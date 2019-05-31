.. _getting-started:


Getting Started
===============

Runcible and MergeDB example
----------------------------

MergeDB is a project created for Runcible to make declaration of configurations easier, as a result MergeDB is a
preferred mechanism for defining Runcible declarations (although you can also use flat YAML or JSON files as well.)

For this example, I will build a simple 3 switch setup inside of GNS3 using Cumulus VX for the operating system.

Here is the topology:

.. image:: screenshots/network_topology_3switch.png

.. warning::
    It is highly recommended to use Runcible with switch fabrics only when you have a dedicated out-of-band management
    network that won't become inaccessible in the event of misconfiguration.

First, create a directory that contains a file named ``mdb.yaml``, which we will leave blank for now. This file
indicates to MergeDB that we are creating a MergeDB database in this directory. Next we will create two folders,
one for our device declarations, and one for our configuration layers. We will call these folders ``devices`` and
``layers``. In the base of those two directories, create a file called ``dir.yaml`` in each directory and leave them
blank for now. These files inform MergeDB that the .yaml files we will create in these directories are valid MergeDB
declarations.

.. note::
    This directory structure is completely arbitrary. MergeDB is designed in a manner that lets you organize your
    declarations in whatever way makes sense to you.

Next, lets create a few configuration layers that define our switch configurations. Firstly, our switches all have the
default U: ``cumulus`` P: ``CumulusLinux!`` credentials, so lets create a layer that adds those attributes to the meta
object:

.. literalinclude:: ../examples/mergedb_getting_started/layers/ssh_auth.yaml

Next, our switches should all contain the same VLANS in this example, so lets make a layer that defines those:

.. literalinclude:: ../examples/mergedb_getting_started/layers/vlans.yaml

Note that we are using jinja2 templating to avoid needing to duplicate the vlan definitions.

Now, lets create some layers that define our switch environment. In this example, we want all of the uplinks from the
dist1 and dist2 switches to be tagged on all vlans, and the downlinks from the switches to the PCs to be untagged. As a
result, we will create two different layers called ``core.yaml`` and ``dist.yaml``.

.. literalinclude:: ../examples/mergedb_getting_started/layers/core.yaml

.. literalinclude:: ../examples/mergedb_getting_started/layers/dist.yaml

As you can see, our core has all tagged interfaces, whereas the first two ports on the dist switch are untagged, and the
last port is tagged.

Now we need to create the declarations for our switches. In the device directory, create a .yaml for each of the
devices:

.. literalinclude:: ../examples/mergedb_getting_started/devices/core.yaml

.. literalinclude:: ../examples/mergedb_getting_started/devices/dist1.yaml

.. literalinclude:: ../examples/mergedb_getting_started/devices/dist2.yaml

At this point, if you were to run MergeDB, you would get blank output because we haven't added anything to the build
list. So lets add the rest of our inheritance structure and the build list to the dir.yaml inside the devices directory:

.. literalinclude:: ../examples/mergedb_getting_started/devices/dir.yaml


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

