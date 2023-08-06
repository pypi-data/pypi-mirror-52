===================
bisos.setup Scripts
===================

.. contents::
   :depth: 3
..

Overview
========

Bash scripts (Interactive Command Modules – ICM) for bootstrapping BISOS
(ByStar Internet Services OS) software profiles on a virgin Linux
distro. Or for creating fully automated KVM guests that are ByStar
Platforms.

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact

Documentation
=============

Part of ByStar Digital Ecosystem http://www.by-star.net.

This module’s primary documentation is in
http://www.by-star.net/PLPC/180047

Installation
============

::

    sudo pip install bisos.setup

Usage
=====

“./bin/bxGenWithRepo”
---------------------

Does the following:

-  Clone specified repo

-  From within that repo executes specified entry point with params and
   args. This typically involves creating an account
