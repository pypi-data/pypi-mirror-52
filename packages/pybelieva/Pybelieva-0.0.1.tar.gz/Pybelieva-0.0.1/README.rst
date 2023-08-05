UnbPy
=====

|logo| ## About UnbPy > UnbPy is a library providing a Python interface
to the > `UnbelivaBoat API <https://unbelievable.pizza/api/docs>`__. To
use it, you need > to get a token from the official documentation page.
Also supports discord.py > Guild and User objects.

|discord| |status| |release| |api| |documentation| |python|

Help
----

    You can find an in-depth tutorial and a detailed documentation on
    `our wiki <https://github.com/dev-cats/UnbPy/wiki>`__.

Quick Start
-----------

Setup
~~~~~

1. Install UnbPy.
2. Go to `the UnbelivaBoat site <https://unbelievable.pizza>`__.
3. Login to your Discord account.
4. Go to `the API page <https://unbelievable.pizza/api/docs>`__.
5. Click "Copy" under the big string of red text. Your token is now in
   the clipboard. |example|

.. code:: python

    >>> client = Client('Insert token here')
    >>> guild = Guild(0) # Replace 0 with a Discord guild id
    >>> user = User(0)   # Replace 0 with a Discord user id

Functions
~~~~~~~~~

.. code:: python

    client.get_balance(guild, user)

Returns: ``User`` with all attributes set.

.. code:: python

    client.get_leaderboard(guild)

Returns: ``list`` of ``User``\ s with all attributes set, ordered by
rank.

.. code:: python

    client.patch_balance(guild, user, cash, bank)

Returns: ``User`` with all attributes except rank set and an updated
balance.

.. code:: python

    client.set_balance(guild, user, cash, bank)

Returns: ``User`` with all attributes except rank set and the new
balance.

Dependencies
------------

    -  Python
    -  aiohttp
    -  discord.py (optional)

.. |logo| image:: https://i.imgur.com/RLRDeQw.png
.. |discord| image:: https://discordapp.com/api/guilds/566686199834476555/embed.png
   :target: https://discord.gg/azdCbgv
.. |status| image:: https://img.shields.io/badge/status-release-brightgreen.svg
   :target: https://github.com/dev-cats/UnbPy/releases/tag/v1.0.0
.. |release| image:: https://img.shields.io/badge/version-v1.2.0-blue.svg
   :target: https://github.com/dev-cats/UnbPy/wiki/Version-History
.. |api| image:: https://img.shields.io/badge/api-v1-ff266a.svg
   :target: https://unbelievable.pizza/api/docs
.. |documentation| image:: https://img.shields.io/badge/documentation-100%25-brightgreen.svg
   :target: https://github.com/dev-cats/UnbPy/wiki/Documentation
.. |python| image:: https://img.shields.io/badge/python-any-blue.svg
   :target: https://python.org/
.. |example| image:: https://i.imgur.com/HBcXbn9.png
