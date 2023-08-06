Projects, Snapshots, and Sessions
=================================

Snapshots and sessions make it easy to deploy, save, and reproduce Ray
projects.

Quick start (CLI)
-----------------

.. code-block:: bash

    # Creates a snapshot of the current project.
    # This saves a copy of all files found in the current project directory, as
    # well as any files specified in the output_files list in
    # .rayproject/project.yaml.
    # Currently, the files are saved to local disk, under ~/.ray-snapshots.
    $ any snapshot create [--name <project-name>]

    # Start a session from a given snapshot. All files saved in the snapshot
    # that were not specified in output_files in .rayproject/project.yaml will be
    # synced to the session. If no snapshot is specified, then take a snapshot
    # and start a session. Once the snapshot has been deployed, this runs the
    # specified command (optional), which must be specified in the project.yaml
    # file.  Alternatively, use --shell to run a raw shell command. You can
    # start multiple sessions at the same time by providing a wildcard for
    # a parameter as in `any session start command --parameter "*"`.
    $ any session start <command-name> [arguments] [--name <session-name>] [--snapshot-name <snapshot-name>] [--shell]

    # Open a console for the given session.
    $ any session attach

    # List the active sessions. An asterisk will be printed in front of the
    active one, if any.
    $ any session list [--name <session-name>]
    # Project sessions:
    # *Session(name=session1 created_at=2019-09-08 00:48:15.391648)
    #  Session(name=session0 created_at=2019-09-08 00:45:15.371339)

    # Execute a command on an active session. You can execute commands on
    # multiple sessions at the same time by specifying a pattern in <session-name>.
    # The pattern can contain * to match an arbitrary string of characters or ?
    # to match a single character, in the same way that wildcards can be used
    # in bash.
    $ any session execute <command-name> [arguments] [--name <session-name>] [--shell]

    # Synchronize a session with a snapshot. Similar to session execute, you can
    # specify a pattern for <session-name>.
    $ any session sync [--name <session-name>] --snapshot-name <snapshot-name>

    # Stop the given session and terminate all of its worker nodes. You can terminate
    # all active sessions with `any session stop --name "*"`.
    $ any session stop

Managing snapshots
------------------

By default, snapshots are kept around forever.
You can list your snapshots and manually delete snapshots with a given name.

.. code-block:: bash

    # List all snapshots of the current project
    $ any snapshot list
    # Project snaphots:
    # Snapshot(name=48bddd25-a312-470e-97fa-ad9cf9d4c823 created_at=2019-09-04 05:18:12.739830)

    # Delete a snapshot(s) with a given name.
    $ any snapshot delete <snapshot-name>

Managing sessions
-----------------
By default, sessions are kept around forever.
You can get more information about sessions, such as the snapshots that the session was synced with and the commands that were run on the snapshot through `any session start`.

.. code-block:: bash

    # List more information about a session.
    $ any snapshot list --name session1
    # Snapshots applied to Session(name=session1 created_at=2019-09-08 00:48:15.391648)
    #  2019-09-08 00:48:15.392570: Snapshot(name=hello created_at=2019-09-08 00:47:09.082986)
    #  2019-09-08 00:53:24.184101: Snapshot(name=hello created_at=2019-09-08 00:47:09.082986)
    #  2019-09-08 00:54:08.611014: Snapshot(name=hello created_at=2019-09-08 00:47:09.082986)
    # Commands run during Session(name=session1 created_at=2019-09-08 00:48:15.391648)
    #  2019-09-08 00:53:24.187074: 'echo "Starting ray job"'
    #  2019-09-08 00:54:08.614122: 'ls'


.. toctree::
   :maxdepth: -1
   :caption: CLI reference

   cli_reference.rst
