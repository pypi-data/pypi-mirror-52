# -*- coding: utf-8 -*-
from collective.denyroles import config
from collective.denyroles.utils import must_check
from Products.PluggableAuthService.interfaces.authservice import _noroles
from Products.PluggableAuthService.PluggableAuthService import PluggableAuthService as PAS


PAS._orig_authorizeUser = PAS._authorizeUser


def _authorizeUser(self, user, accessed, container, name, value, roles=_noroles):
    """ -> boolean (whether user has roles).

    o Add the user to the SM's stack, if successful.

    o Return
    """
    if must_check():
        principal_roles = user.getRoles()  # noqa P001
        for role in config.DENIED_ROLES:
            if role in principal_roles:
                return 0
    return self._orig_authorizeUser(user, accessed, container, name, value, roles=roles)


PAS._authorizeUser = _authorizeUser
