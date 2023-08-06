.. contents:: Table of Contents


Introduction
============

This packages includes various browser vendor fixes for iframe-specific issues.

Compatibility
-------------

Plone 4.3.x
Plone 5.1.x


Installation
============

- Add the package to your buildout configuration:

::

    [instance]
    eggs +=
        ...
        ftw.iframefix


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.iframefix
- Issues: https://github.com/4teamwork/ftw.iframefix/issues
- Pypi: http://pypi.python.org/pypi/ftw.iframefix


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.iframefix`` is licensed under GNU General Public License, version 2.
