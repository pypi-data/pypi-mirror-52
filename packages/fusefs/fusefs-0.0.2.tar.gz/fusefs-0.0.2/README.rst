======
FuseFS
======


.. image:: https://img.shields.io/pypi/v/fusefs.svg
        :target: https://pypi.python.org/pypi/fusefs

.. image:: https://readthedocs.org/projects/fusefs/badge/?version=latest
        :target: https://fusefs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


FuseFS: FUSE <-> pyFilesystem adapter


* Free software: GNU Affero General Public License v3 or later (AGPLv3+)
* Documentation: https://fusefs.readthedocs.io.

.. image:: demo.gif
   :width: 512
   :alt: FuseFS demo

Description
-----------

FuseFS is an adapter that allows any filesystem interfaced by pyFilesystem to be mounted and accessed natively on any OS that supports FUSE (Filesystem in Userspace). Some interfaces for pyFilesystem include zip files, SSH, various cloud storage providers, and even IMAP servers. This means this tool can allow interaction with compressed folders, remote servers, your email, etc or combinations of any as if they are all normal folders local to your system.

Features
--------

* Provide a common interface to any filesystem using pyFilesystem_

* Access the provided interface natively via FUSE_

* Use placeholders during invocation to dynamically get values from the user

Installation and Usage
----------------------

0) Ensure FUSE is installed.

1) Install via pip.

  * ``pip install fusefs``

2) Run ``fusefs <url> <mountpoint>``. ``url`` is the pyFilesystem resource to be mounted, and may contain placeholders for such values as username, host, password, etc.

  * Default placeholder pattern is ``[[placeholder]]``, where the ``placeholder`` is a name used by the interactive prompt to specify the value requested.

  * An optional ``mode`` may be prepended with a ``separator`` to the ``placeholder``. The default separator is ``:``, and the only available mode (currently) is ``hide``, which masks provided input to get such values as passwords. Eg. ``hide:password``.

3) Use ``mountpoint`` as you would the contents of any other folder.


TODO
----

* Write tests

* Complete implementation

* Implement config file mode

* Fix bugs

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _pyFilesystem: https://github.com/PyFilesystem/pyfilesystem2
.. _FUSE: https://github.com/libfuse/libfuse
