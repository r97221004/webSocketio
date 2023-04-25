from functools import wraps
import logging.config
# from app.adaptor.socket import handle_emit
from flask import request
from flask import abort
# import jwt
# from app.config import JwtConfig, UserConfig

log = logging.getLogger(__name__)


# def jwt_required():
#     def _jwt_required(func):
#         @wraps(func)
#         def decorated_view(*args, **kwargs):

#             token = request.headers.get('authorization')
#             if not token:
#                 log.info('Unauthorized')
#                 abort(401, 'Unauthorized')

#             PREFIX = 'Bearer '
#             if not token.startswith(PREFIX):
#                 log.info('Invalid authorization format')
#                 abort(400, 'Invalid authorization format')
#             token = token[len(PREFIX):]
#             try:
#                 request.environ['cmd_jwt_payload'] = jwt.decode(
#                     token, JwtConfig.SECRET, algorithms=JwtConfig.ALGORITHM)

#             except Exception as e:
#                 abort(403, str(e))
#             try:
#                 user = request.environ["cmd_jwt_payload"]["user"]  # noqa:F841
#             except Exception as e:
#                 abort(403, str(e))
#             try:
#                 group = request.environ['cmd_jwt_payload']["group"]
#             except Exception as e:
#                 abort(403, str(e))
#             if not list(filter(lambda x: x in UserConfig.CMD_GROUP, group)):
#                 abort(403, "no privileges")
#             return func(*args, **kwargs)
#         return decorated_view
#     return _jwt_required


def sio_jwt_required():
    def _sio_jwt_required(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            token = request.headers.get('authorization')

            if not token:
                print('Unauthorized')
            #     handle_emit(401, 'Unauthorized')

            # PREFIX = 'Bearer '
            # if not token.startswith(PREFIX):
            #     log.info('Invalid authorization format')
            #     handle_emit(400, 'Invalid authorization format')
            # token = token[len(PREFIX):]
            # try:
            #     request.environ['cmd_jwt_payload'] = jwt.decode(
            #         token, JwtConfig.SECRET, algorithms=JwtConfig.ALGORITHM)

            # except Exception as e:
            #     handle_emit(403, str(e))

            # try:
            #     group = request.environ['cmd_jwt_payload']["group"]
            #     if not list(filter(lambda x: x in UserConfig.CMD_GROUP, group)):
            #         handle_emit(403, "no privileges")
            # except Exception as e:
            #     handle_emit(403, str(e))

            return func(*args, **kwargs)
        return decorated_view
    return _sio_jwt_required
