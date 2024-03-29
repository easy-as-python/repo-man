Welcome to repo-man's documentation!
====================================

Manage repositories of different types.

.. toctree::
   :maxdepth: 2
   :caption: Documentation contents:
   :hidden:

   reference/modules
   CHANGELOG

.. toctree::
   :glob:
   :caption: Architecture decision records:
   :hidden:

   architecture/decisions/*

If you work in open source or as a cross-team individual contributor in your organization,
you may have dozens of repositories cloned to your local machine.
Those repositories may be of several different *types*, exhibiting a particular file structure or purpose.

You may find yourself wanting to query or mutate repositories of a particular type and,
unless the repositories of that type share a common name prefix or some other signifier,
it can prove tedious to specify which repositories to run commands against.
Even great tools like `fzf <https://github.com/junegunn/fzf>`_ don't quite reduce the burden of selecting all desired repositories at this scale.

repo-man is a tool for managing a catalog of repositories and their types to improve your productivity.

Getting started
---------------

Using repo-man involves two major steps: Installing the package and configuring it for your repositories.

Installation
************

To get started, install the ``repo-man`` package using your favorite package management tool
(hint: :command:`python -m pip install repo-man`).
If you want to use ``repo-man`` in a global context, you can use a tool like `pipx <https://pypa.github.io/pipx/>`_.

After you've installed ``repo-man`` and have activated its environment as needed,
the :command:`repo-man` command will be available for you to use.
You can run :command:`repo-man --help` to see all the available options.

Configuration
*************

To configure repo-man, create a :file:`repo-man.cfg` file alongside your cloned repositories.
This file is an INI-style file with sections, where each section name is a repository type.
In each repository type section, a single ``known`` property specifies a newline-delimited list of repositories.

A valid :file:`repo-man.cfg` file might look something like the following:

.. code-block:: cfg

   [some-type]
   known =
       repo-one
       repo-two

   [some-other-type]
   known =
       repo-three


With this configuration, you can now use the :command:`repo-man` command to manage your repositories.

Ignoring directories
++++++++++++++++++++

Some directories next to your configuration file may not be repositories,
or you may just want to ignore them when using repo-man.

You can use a special ``[ignore]`` section in the :file:`repo-man.cfg` to hide these directories:

.. code-block:: cfg

    [ignore]
    some-undesired-directory
    .some-hidden-directory


Usage
*****

This section describes some of the useful ways to leverage repo-man for productivity.

.. note::

    Always check the output of the :command:`repo-man --help` command for the most accurate usage information.


Listing repositories
++++++++++++++++++++

.. code-block:: shell

    $ repo-man list --type some-type
    repo-one
    repo-two

Listing types for a repository
++++++++++++++++++++++++++++++++

.. code-block:: shell

    $ repo-man types repo-one
    some-type

Adding a repository
+++++++++++++++++++

You can add a repository to an existing type:

.. code-block:: shell

    $ repo-man add repo-four --type some-type

You can also add a repository to an existing type:

.. code-block:: shell

    $ repo-man add repo-five --type some-brand-new-type

Listing known types
+++++++++++++++++++++

.. code-block:: shell

    $ repo-man sniff --known
    some-type
    some-other-type


Combining with other tools
++++++++++++++++++++++++++

The value of repo-man comes in when combining its output with other tools.
As an example, you can iterate over all the repositories of a given type to take some action:

.. code-block:: shell

    $ for repo in $(repo-man list --type some-type); do
        cd $repo;
        # take some action;
        cd ..;
    done


Metacommands
++++++++++++

These commands help you query and improve your repo-man configuration.

Unconfigured repositories
^^^^^^^^^^^^^^^^^^^^^^^^^

List repositories you have cloned but that have no configured type:

.. code-block:: shell

    $ repo-man sniff --unconfigured
    some-unknown-repo
    some-other-unknown-repo

Duplicate repositories
^^^^^^^^^^^^^^^^^^^^^^

Some repositories may be of multiple types, but you may also accidentally configure a repository as two types.
You can list all the repositories that you've configured as more than one type:

.. code-block:: cfg

    [some-type]
    known =
        repo-one
        repo-two

    [some-other-type]
    known =
        repo-one


.. code-block:: shell

    $ repo-man sniff --duplicates
    repo-one

Tips and tricks
+++++++++++++++

You may wish to create a hierarchy of types, starting your type names with the most general classification.
As an example, you may have several different package and application types that you could capture as follows:

.. code-block:: cfg

    [application.django]
    known =
        some-django-project
        some-other-django-project

    [application.node]
    known =
        some-node-service

    [package.python]
    known =
        repo-man

    [package.javascript]
    known =
        left-pad
        is-even

repo-man doesn't currently do anything special with these, but could grow features to e.g. list type classes.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
