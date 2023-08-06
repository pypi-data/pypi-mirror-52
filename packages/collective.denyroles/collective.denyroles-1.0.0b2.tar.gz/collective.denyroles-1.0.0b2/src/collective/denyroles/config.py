# -*- coding: utf-8 -*-
import logging
import os


logger = logging.getLogger("collective.denyroles")

# Default ID of our plugin in acl_users:
PLUGIN_ID = "denyroles"

# We could make this configurable.
DENIED_ROLES = ["Manager", "Site Administrator", "Editor", "Reviewer", "Contributor"]

# When request headers are checked, we look for these headers.
# We have two headers, to sidestep problems when a hacker manages to insert a header.
DO_CHECK_ROLES_HEADER = "X_DO_CHECK_ROLES"
DONT_CHECK_ROLES_HEADER = "X_DONT_CHECK_ROLES"

# Environment variable to determine if we deny roles.
DENY_ROLES_ENV = "DENY_ROLES"
DENY_ROLES = None


def read_deny_roles_from_env():
    global DENY_ROLES
    DENY_ROLES = os.getenv(DENY_ROLES_ENV, None)
    if DENY_ROLES is not None:
        try:
            DENY_ROLES = int(DENY_ROLES)
        except (ValueError, TypeError, AttributeError):
            logger.warning("Ignored non-integer %s environment variable.", DENY_ROLES_ENV)
            DENY_ROLES = None
    if DENY_ROLES is None:
        logger.info(
            "%s environment variable not set. Will check request headers %s and %s.",
            DENY_ROLES_ENV,
            DO_CHECK_ROLES_HEADER,
            DONT_CHECK_ROLES_HEADER,
        )
    elif DENY_ROLES == 0:
        DENY_ROLES = False
        logger.info(
            "%s environment variable set to zero. Will NOT deny access based on roles.",
            DENY_ROLES_ENV,
        )
    else:
        logger.info(
            "%s environment variable set to %d. Will deny access based on roles.",
            DENY_ROLES_ENV,
            DENY_ROLES,
        )
        DENY_ROLES = True


read_deny_roles_from_env()
