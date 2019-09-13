# Runcible

[![Documentation Status](https://readthedocs.org/projects/runcible/badge/?version=latest)](https://runcible.readthedocs.io/en/latest/?badge=latest)
[![Gitter](https://badges.gitter.im/runcible_project/community.svg)](https://gitter.im/runcible_project/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## What is Runcible?
Runcible is a framework and CLI application to allow for declarative switch management. It intakes a declared state for 
a device in YAML or JSON and turns it into a list of idempotent commands to configure that device, it then runs them 
over the desired protocol.

Runcible provides a high-level API for Python developers to leverage to manage devices programmatically, and also 
provides a YAML interface with configuration layering and inheritance for network engineers with any amount of 
programming experience.

## How is This Different from Ansible and Others?
Runcible was created to solve three major problems in regards to Network Automation:

### Interface Commonality
One of the core components of Runcible is a datatype known as Modules. Modules are plugin-independent interfaces that 
allow data with a common schema to be passed into multiple types of plugins. This allows for a large amount of 
configuration re-use between similar devices produced by different vendors. I.E. the vlans module should be implemented 
by any switch plugin that supports vlans, and the configuration should be identical (assuming the device supports the 
entire featureset of the vlans module.)

### Topology Awareness
One important aspect of any kind of network automation is ensuring that bad automation runs are dealt with, and that 
you stage your changes in a topology-aware manner. You wouldn’t want a bad change to propagate to your entire core 
switch fabric and take your network down. Runcible provides Schedulers that allow for intelligent automation runs allow 
you to ensure that your automated changes are made intelligently, and also control rollback and failure behavior.

### Protocol Agnosticism
Runcible doesn’t operate on a defined set of protocols. While most providers will go with a text based protocol 
(SSH, telnet, RS232), any protocol is supported. Runcible provides some sane default protocol modules based on paramiko 
for SSH, and pyserial for RS232 terminals, but has loose shim classes that allow plugin writers to implement any 
protocol they deem necessary without inhibiting any of Runcible’s features. This allows users to use their same 
automation repository for both bootstrapping devices via a serial connection, as well as making changes via SSH, 
Telnet, REST, or even protocols that haven’t been invented yet.

## Getting Started

Read the getting started guide here: https://runcible.readthedocs.io/en/development/getting_started.html