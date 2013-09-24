Design document
###############

So we need to do a service able to handle a lot of simultaneous calls.

The file registration should interact closely with addons.mozilla.org since
they are providing the information we need about user accounts.

The idea is to have a completely separated service handling the API, and to let
AMO handle the authentication.

The routing will be done at a higher level by a reverse proxy or directly at
the client leve, by using a different domain to access to service.

.. image:: images/design.png
   :align: center

Here, we can see that the writes are going trough the AMO API and then to the
addon registration API, whereas the reads are going directly to the addon
registration API.


Caching
=======

We have a lot of addons that will do calls to the API with the same data
(assuming a lot of people install the same version of the same addon).

That would be silly to do a check on the database each time we have a request,
and even more silly to have the client do the same call all the time with the
same response.

We should use caching mechanisms whenever possible.

Invalidation
------------

"Caching is easy, invalidation is hard".

One possibility would be to have all the information provided as static files.
This way, it is really easy to make it scale without issues.

Then, we could queue all the changes to the files (the writes) in memory and
do the appropriate changes to the files whenever that's needed.

This way, with very little effort, we get caching for free (caching mechanisms
use the last modification date of files for caching) and scaling this is like
scaling static files.
