Introduction
============

What is Runcible?
-----------------

Runcible is a framework and CLI application to allow for declarative switch management. It intakes a declared state for
a device in YAML or JSON and turns it into a list of idempotent commands to configure that device, it then runs them
over SSH, Telnet, or RS-232 (plugins can be written for any text based terminal, or REST API however.)

Runcible provides a high-level API for Python developers to leverage to manage devices programmatically, and also
provides a YAML interface with configuration layering and inheritance for network engineers with any amount of
programming experience.


What is a Runcible?
-------------------

Depending on who you ask, its either a nonsensical word, a word for spork, or a faster than light transportation network.

How is This Different from Ansible and Others?
----------------------------------------------

Runcible focuses on network devices (Switches, Routers, Firewalls, Wireless Gear), and also has some strong opinions in
regards to YAML structure. This gives it many advantages for network appliances, chiefly different devices or devices
from different vendors being able to share a similar interface. Since network devices must comply with networking
standards, they generally all operate in a similar fashion, and as a result can be abstracted in a similar fashion. This
makes it rather unsuited to managing operating systems.

While Ansible is the current de-facto option for managing network device configurations, it doesn't support the concept
of layering configurations, which is extremely important if you are trying to define a network using DRY (Don't Repeat
Yourself) principles.

I Want to Get Involved
----------------------

Great! Head over to the :ref:`contribution-guide`.