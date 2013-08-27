Addon registration API
######################

The goal of this service is to integrate closely with the addons.mozilla.org
website (a.k.a AMO) to provide a way to register non AMO-listed addons as
a really simple process.

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
a look at the hash of the .xpi file it is trying to install and send a request
to our server, which will do a verification on this hash, to be sure it matches
something known.

What's an addon anyway?
-----------------------

An addon contains different important piece of information:

- an unique addon id
- a name
- a version 
- some files associated with it

How do we proceed?
------------------

Each time someone wants to release a new addon, it needs to register the new
version on AMO. This process can be automated really easily using the HTTP APIs
this service is providing.

The information sent to the AMO registration service are the following:

1. The addon id
2. the addon name
3. the addon version
4. A number of hashes, matching each `.xpi` (a release can contain more than
   one xpi, for instance if it is distributed over more than one OS).

These information are sent to our services. In case there is a match, all is
fine and we don't display anything. In case nothing is found in the db,
a warning is shown to the user.

What does this mean?
====================

For the addon developpers
-------------------------

All of this means addons developers will need to register their addons on
addons.mozilla.org. 

On the user agent
-----------------

On the user-agent side, we need to do the following changes:

- Be sure it's possible to stop asking the server if the file is well known or
  not for certain addons.


More doc
========

.. toctree::
   :maxdepth: 2

   faq
