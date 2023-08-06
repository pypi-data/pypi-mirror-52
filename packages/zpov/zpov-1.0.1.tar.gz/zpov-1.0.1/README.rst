zpov
====

A minimalist note engine
------------------------

* ~500 lines of code
* no javascript
* usable on any browser, including on mobile
* no database, just a bare git repo for storage and sync
* http basic auth
* pages are markdown files in the git repo. earch "directory" *must* have
  an ``index.md`` at the top
* title of each page is the top line of the markdown file
* sub-pages are sorted alphabetically
* edition is a text area containing the markdown

Usage
-----

``zpov`` is a python application built using ``flask``. refer to the flask
documentation to learn about developement and/or debugging.

note that you will need a config file named ``zpov.yml`` in the current directory, looking like this

.. code-block:: yaml

    public_access: <true|false>

    users:  # required if public_access is ``false``
      <user>: "<hashed password>"

    repo_path: 'path/to/repo.git

where:

* ``path/to/repo.git`` is a *bare* git repository containing the markdown files.
* ``hashed_password`` was generated with ``nacl.pwhash.str('<password>')``.
