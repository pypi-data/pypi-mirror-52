.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi. It is a comment.

collective.denyroles
====================

This is a monkey patch for PAS (``PluggableAuthService``).
It denies access to Plone Sites for users with roles like Manager or Editor.


Features
--------

- A patch for the PAS ``_authorizeUser`` method that checks the roles of the user, and gives no authorization when some roles are found.

- Configuration via environment variables or request headers to see if the check should be done.


Use case
--------

You have a Plone Site on two domains:

- edit.example.local is for editing.
  Users with the Editor or Manager role login here to edit and manage the site.
  This is a local domain that can only be reached within your local network or a VPN.

- www.example.org is for anonymous users and maybe also for standard Members without extra roles.
  This domain is protected by a special firewall to prevent common web attacks like
  dubious form submissions, request flooding, spammers, cross site scripting attacks, etcetera.

Problems:

- Editors sometimes login to the public domain,
  and get errors during editing because the firewall is too protective.

- The system administrator complains that he has setup a special domain for editing and managing,
  so that no changes can come in from the public site,
  and yet unexpectedly the editors can login and make changes via the public site anyway.

This package gives you options to prevent users with some global roles from accessing the (public) site.
To be more precise: they will be treated as anonymous.
When they try to login, the login process will fail.


Installation
------------

Install collective.denyroles by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.denyroles


and then running ``bin/buildout``.
It is immediately active, without needing activation within the Plone Site.

You may need some more configuration in your buildout config.
See the next section.


Configuration
-------------

The roles that are denied access, can be seen in ``src/collective/denyroles/config.py``.
We might make this configurable at some point.
Currently they are:

- Manager
- Site Administrator
- Editor
- Reviewer
- Contributor

There are two ways to configure whether the roles should be checked or not:
via environment variables or via request headers.


Environment variables
~~~~~~~~~~~~~~~~~~~~~

You can set an environment variable to always deny the roles::

    export DENY_ROLES=1

Set this to 1 (or another positive integer) for yes, and 0 for no.
Any other values will be ignored.

Note that the OS environment can be different when you manually start your Plone instance or start it in a cronjob.
So it is better to set this in your Plone ``buildout.cfg``::

    [instance]
    recipe = plone.recipe.zope2instance
    environment-vars =
        DENY_ROLES 1

Run the buildout and it will be set in the Plone config,
in this case in ``parts/instance/etc/zope.conf``.

The environment variable is useful when the roles should be checked for *all* traffic to this Plone instance.
If you have a ZEO setup with two zeoclients, where one zeoclient gets all traffic from editors, and another gets the anonymous visitors, you can do this:

- zeoclient for editors: ``DENY_ROLES 0``
- zeoclient for anonymous: ``DENY_ROLES 1``

Now editors can edit normally in their edit environment.
And when they accidentally login on the anonymous environment, they will be treated as anonymous.


Request headers
~~~~~~~~~~~~~~~

When the environment variable is *not set at all*, or set to an invalid value, we check the request headers.
We have two headers, to sidestep problems when a hacker manages to insert a header::

    X_DO_CHECK_ROLES
    X_DONT_CHECK_ROLES

The default when the environment variable is not set, and no headers are present, is to deny the roles.
So:

- When none of these headers are set, we deny access to editors.

- When ``X_DO_CHECK_ROLES`` is set, we deny access to editors.

- When ``X_DONT_CHECK_ROLES`` is set, we allow access to all roles.

- When both headers are set, ``X_DO_CHECK_ROLES`` wins, and we deny access to editors.

The approach with request headers is useful when you have a single zeoclient that handles all traffic for two different domains.
The web server (like nginx or Apache) should then add a header, depending on which domain the traffic comes in:

- For the edit domain: ``X_DONT_CHECK_ROLES``

- Optionally for the public domain: ``X_DO_CHECK_ROLES``.
  This is to make it explicit.
  Also, it helps when you are not sure if a hacker may be able to insert the other header.

The value does not matter, as long as the request header with this name exists,
but 1 seems a good value.


Suggested buildout usage
------------------------

This is a suggestion on how to properly add this in a buildout.
Note that this focuses on configuring collective.denyroles, and ignores lots of other useful settings::

    [zeoclient]
    # Configuration for public zeoclient.
    recipe = plone.recipe.zope2instance
    http-address = 8080
    zeo-client = on
    eggs =
        Plone
        collective.denyroles
    # Environment variables shared by all zeoclients:
    base-environment-vars =
        zope_i18n_compile_mo_files true
    environment-vars =
        ${:base-environment-vars}
    # In the public zeoclient, we deny access to editors/managers:
        DENY_ROLES 1

    [zeoclient-cms]
    # Second Plone zeoclient, only used for CMS, so for editors.
    # The next weird line means: inherit all settings from the [zeoclient] section:
    <= zeoclient
    # Use a different port:
    http-address = 8090
    environment-vars =
        ${:base-environment-vars}
    # In the CMS zeoclient, we do not want to deny access to editors/managers:
        DENY_ROLES 0

    [instance]
    # Standalone Plone instance without ZEO setup, for local development.
    <= zeoclient
    zeo-client = off
    environment-vars =
        ${:base-environment-vars}
    # With single instance, we do not want to deny access to editors/managers:
        DENY_ROLES 0


Support
-------

If you are having issues, please let us know.
Contact Maurits van Rees at Zest Software, m.van.rees@zestsoftware.nl.
Or open an issue in `GitHub <https://github.com/collective/collective.denyroles/issues/>`_.


License
-------

The project is licensed under the GPLv2.
