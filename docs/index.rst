Addon registration API
######################

The goal of this service is to integrate closely with the addons.mozilla.org
website (a.k.a AMO) to provide a way to register non AMO-listed addons as
a really simple process.

`The initial brainstorm is there <https://wiki.mozilla.org/User:Jorge.villalobos/WorkWeek2012Q2/FileRegistration>`_

Goals
=====

Registering addons allows more security for the end users: it is then possible
to detect malwares or addons with fake names which are trying to mislead the
end users.

For us (Mozilla), this creates a way to contact addons authors and engage
a discussion with them where we couldn't previously. This can be useful when it
comes to security updates or malwares.

Behind the scenes
=================

When an user wants to install a new addon, the user-agent (firefox) will have
a look at the hash of the ``.xpi`` file it is trying to install and send a request
to our server, which will do a verification on this hash, to be sure it matches
something known to us.

It acts as a whitelist: all the known addons will be installed without any
warning and the other ones will be either not installed or a warning will be
issued.

What's an addon anyway?
-----------------------

An addon contains different important piece of metadata. The ones which are
interesting to us are the following:

- an unique addon id
- a name
- a version 
- some files associated with it

How do we proceed?
------------------

Each time someone wants to release a new addon, it needs to register it on AMO.
This also applies to new versions of already existing addons. This process can
be automated really easily using the HTTP APIs this service is providing.

The information sent to the AMO registration service are the following:

1. The addon id
2. the addon name
3. the addon version
4. A number of hashes, matching each `.xpi` (a release can contain more than
   one xpi, for instance if it is distributed over more than one OS).

These information are sent to our services. In case there is a match, all is
fine and we don't display anything. In case nothing is found in the db,
a warning is shown to the user.

More doc
========

.. toctree::
   :maxdepth: 2

   design
   faq
