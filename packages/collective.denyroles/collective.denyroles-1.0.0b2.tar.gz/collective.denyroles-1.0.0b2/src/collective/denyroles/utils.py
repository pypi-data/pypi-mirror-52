# -*- coding: utf-8 -*-
from collective.denyroles import config
from zope.globalrequest import getRequest


def must_check(request=None):
    """Must we check the roles?"""
    deny_roles = config.DENY_ROLES
    if deny_roles is not None:
        return deny_roles
    if request is None:
        request = getRequest()
        if request is None:
            return True
    if request.getHeader(config.DO_CHECK_ROLES_HEADER):
        return True
    if request.getHeader(config.DONT_CHECK_ROLES_HEADER):
        return False
    # So there is no explicit environment variable,
    # and no explicit request header.
    return True
