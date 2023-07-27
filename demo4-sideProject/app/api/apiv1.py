# import sys
# import traceback
# import logging
# from flask import Blueprint
# from flask_restplus import Api
# from app.exception import ResourceNotFound, InvalidFormatException
# from app.api.v1.command_endpoint import namespace as command_api
# from app.api.v1.deviceinfo_endpoint import namespace as deviceinfo_api


# log = logging.getLogger(__name__)

# blueprint = Blueprint('api', __name__, url_prefix='/v1')
# api = Api(blueprint,
#           version="1.0",
#           title="DEVICE COMMAND API",
#           description="API for device command")
# api.add_namespace(command_api)
# api.add_namespace(deviceinfo_api)


# @api.errorhandler(Exception)
# def default_error_handler(e):
#     exc_type, exc_value, exc_traceback = sys.exc_info()
#     traceback_message = ' traceback:' + \
#         ''.join(traceback.format_tb(exc_traceback, 10)).replace("\n", "")
#     log.error(f'Server error: {e}' + traceback_message)
#     return {'message': 'Internal Server Error'}, 500


# @api.errorhandler(ResourceNotFound)
# def resource_not_found_error_handler(e):
#     return {'message': e.message}, 404


# @api.errorhandler(InvalidFormatException)
# def invalid_format_error_handler(e):
#     return {'message': e.message}, 400
