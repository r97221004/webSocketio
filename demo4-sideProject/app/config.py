# -*- coding: UTF-8 -*-
"""[need loadenv]
    """
import os
import json

from app.extend import loadenv  # noqa:F401


class JwtConfig(object):
    SECRET = os.environ["JWT_SECRET"]
    ALGORITHM = os.environ["JWT_ALGORITHM"]


class UserConfig(object):
    CMD_GROUP = json.loads(os.environ["CMD_USER_GROUP"])
