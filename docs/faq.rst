Open questions
==============

**Why don't we register the known "bad" addons?** Rather than removing the from
the database? it could help us to collect useful information about the name of
the malicious addons / know how much they're used etc, and maybe (technically)
have quicker answers.

→  We actually want to register these, so we will be able to detect them easily
in the future or even blacklist them if needed.

**Do we want all the hashes to be accessible for a specified name?** This can
help to know how many release exist for a specified addon and to find them
easily in our database.

→  That's indeed something that will be useful.

**Do we want to do the search on the addonid only? What does the spec say atm:
is the tuple (name + addonid) unique?** In other words, is it possible to do
the check only on the addonid, without considering the name at all?
