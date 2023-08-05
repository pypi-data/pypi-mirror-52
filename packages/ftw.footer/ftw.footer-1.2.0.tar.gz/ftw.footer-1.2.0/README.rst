Introduction
============

``ftw.footer`` provides a viewlet, which shows 1 - 4 contextual portlet columns.

Compatibility
-------------

- Plone 4.3.x
- Plone 5.1.x

Plone 5 notes
-------------

- Since Plone 5 provides the means to edit any portlet manager through the
  Manage portlets menu item, we've taken the step to disable the manage-footer
  view from Plone 5 onwards.  (It also didn't work well on small screens).

- Plone 5's (default) Barceloneta theme automatically distributes the portlet
  managers from this product across the footer.  This is usually OK, but if it
  does not suit your requirements, then you should use a different theme.

Installation
============


- Add ``ftw.footer`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.footer

- Run `bin/buildout`

- Install the generic import profile.


Configuration
=============

The amount of portlet columns in the footer can be configured in the
`portal_registry` option `IFooterSettings.columns_count`.

Up to four columns are currently supported.


Screenshot
===========

.. image:: https://raw.github.com/4teamwork/ftw.footer/master/docs/screenshot.png

The screenshot is created with
`plonetheme.onegov <https://github.com/OneGov/plonetheme.onegov>`_.



Links
=====

- Github: https://github.com/4teamwork/ftw.footer
- Issues: https://github.com/4teamwork/ftw.footer/issues
- Pypi: http://pypi.python.org/pypi/ftw.footer
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.footer


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.footer`` is licensed under GNU General Public License, version 2.
