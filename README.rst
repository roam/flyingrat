Flying Rat
==========

Flying Rat is a simple mail server for local development. It supports both SMTP to send messages and POP3 to fetch them.

All messages over SMTP are dropped into a single (local) mailbox, which allows you to test your application with real email addresses without running the risk of actually sending messages to those recipients. Running a simple mail server also means it's a lot easier to configure your application to send those messages during local development. The SMTP server runs on localhost at port 5050 by default and that's all you need to configure.

When a message is received it's stored on disk, either to a temporary directory or a directory of your choosing::

    $ flyingrat
    Running from directory /var/folders/zg/jx_p4s0s79j50bmrdlk404j00000gn/T/tmpop5Chy
    ^C
    $ flyingrat testrun/

This means you can examine the contents of the directory to view the actual message. But by default Flying Rat will also run a basic POP3 server on port 5051. So instead of having to watch the directory, just hook up your favorite email client (if you have one) to ``localhost:5051`` with any username and password.

Installing
----------

Flying Rat runs on Python 2. The easiest way to install is through `pipsi <https://github.com/mitsuhiko/pipsi>`_::

    $ pipsi install flyingrat


Options
-------

The most reliable source for possible options is the application itself. Just pass in the ``--help`` option::

    $ flyingrat --help
    Usage: flyingrat [OPTIONS] [DIRECTORY]

      Runs an SMTP server, POP3 server or both based on a directory.

      When no directory is supplied, a temporary directory will be created and
      used. The POP3 server accepts any username and password combination by
      default.

    Options:
      --version                    Print version and exit
      -m, --mode [smtp|pop3|both]  Run smtp, pop3 or both (default)
      -sa, --smtp-address TEXT     Address to run the SMTP server on. Defaults to
                                   localhost:5050
      -pa, --pop3-address TEXT     Address to run the POP3 server on. Defaults to
                                   localhost:5051
      -pu, --pop3-user TEXT        Username for the POP3 server (default: <any>)
      -pp, --pop3-password TEXT    Password for the POP3 server (default: <any>)
      --help                       Show this message and exit.
