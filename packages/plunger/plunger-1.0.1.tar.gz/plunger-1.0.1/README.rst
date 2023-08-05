Plunger
=======

A tool to inspect and clean gitlab's docker registry.

Installation
------------

Using pip::

   $ pip install plunger

Examples
--------

First export some env var to avoid reapeating command line arguments::

    $ export PLUNGER_REGISTRY=https://your.gitlab.registry/
    $ export PLUNGER_KEY_FILE=/path/to/your/key

Inspect the registry::

    $ # show size used by images, grouped by gitlab group
    $ plunger --list 1

    $ # show sizes only for a group
    $ plunger --list 2 --filter repository/

    $ # show sizes of all tags
    $ plunger --list 0 --filter repository/path/

Remove some images::

    $ # keep 4 latest tags for each repos
    $ plunger --keep 4

    $ # keep 2 latest tags for repos starting with 'repository/'
    $ plunger --keep 2 --filter repository/

    $ # remove all tags for repos starting with 'repository/path/'
    $ plunger --keep 0 --filter repository/path/
