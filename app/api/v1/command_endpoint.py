
from datetime import datetime
import logging.config
import re
import json

from flask_restplus import Resource
from flask_restplus import Namespace
from flask_restplus import abort
from flask import request
import aniso8601

from app.handler import cmd_manager, validator, data_parser
from app.exception import ResourceNotFound, InvalidFormatException
from app.errors import CMD_PARAMETER_ERROR, CMD_NOT_EXISTS, FIELD_EMPTY_ERROR
from app.adaptor import sms_service, socket
from app.adaptor.mongodb import sms_mongodb

log = logging.getLogger(__name__)

namespace = Namespace('command', description='Send command to device')

from app.api.v1 import command_model  # nopep8


@namespace.route('/<string:device_type>')
class Command(Resource):
    @namespace.expect(command_model.command)
    @namespace.response(200, "Success")
    def post(self, device_type):
        """[發送設備指令簡訊]

        Args:
            device_type (str): [gps,rf]

        Raises:
            ResourceNotFound: [description]
            InvalidFormatException: [description]
            InvalidFormatException: [description]
            InvalidFormatException: [description]

        Returns:
            [dict]: [result]
        """
        data = request.get_json(force=True)
        cmd = data.get('command')
        phone = data.get('phone')
        telecom = data.get('telecom')
        user = request.environ['cmd_jwt_payload']["user"]
        payload = data.get('payload')

        if device_type not in ['rf', 'gps']:
            raise ResourceNotFound()

        if not cmd or not phone or not telecom or not user:
            raise InvalidFormatException(FIELD_EMPTY_ERROR)

        cmd_message = cmd_manager.get_command(cmd, device_type)
        if cmd_message:
            parameters = re.findall(r'<(.*?)>', cmd_message)
            for para in parameters:
                para_list = str.split(para, '|')

                # hint: para_list[0: <para>, 1: <type>, 2: <condition>]
                parameter_value = payload.get(para_list[0], None)
                if (parameter_value is not None 
                    and validator.CmdParameter.is_valid(para_list[1:], str(parameter_value))):

                    cmd_message = cmd_message.replace(f'<{para}>', str(parameter_value))
                else:
                    raise InvalidFormatException(CMD_PARAMETER_ERROR)

        else:
            raise InvalidFormatException(CMD_NOT_EXISTS)

        result = sms_service.send(cmd_message, phone, telecom)
        time_now = datetime.utcnow()
        log.info(result)
        sms_mongodb.insert_log({
            'type': 'user',
            'user': user,
            'cmd_name': cmd,
            'datetime': time_now,
            'content': cmd_message,
            'result': result,
            'payload': payload
        })

        socket.handle_emit('user_command', {
            'user': user,
            'content': cmd_message,
            'cmdName': cmd,
            'payload': payload,
            'datetime': data_parser(time_now),
            'status': result[0].get('status'),
            '_id': result[0].get('_id')
        })

        return {
            '_id': str(result[0].get('_id')),
            'status': result[0].get('status'),
            'message': result[0].get('message'),
            'datetime': data_parser(time_now),
            'content': cmd_message
        }, 200


@namespace.route('/history')
class History(Resource):
    @namespace.expect(command_model.history)
    @namespace.response(200, "Success")
    def get(self):
        args = command_model.history.parse_args()
        device_id = args.get('device_id')
        head_id = args.get('head_id')
        end_id = args.get('end_id')
        limit = args.get('limit')

        result = sms_mongodb.get_command_log(device_id, limit, head_id, end_id)

        return json.loads(json.dumps(result, default=data_parser)), 200


@namespace.route('/history/search')
class HistorySearch(Resource):
    @namespace.expect(command_model.history_search)
    @namespace.response(200, "Success")
    def get(self):
        device_id = request.args.get('device_id')
        query = request.args.get('q')

        if not device_id or not query:
            abort(400, FIELD_EMPTY_ERROR)

        res = sms_mongodb.command_log_search(device_id, query)
        return json.loads(json.dumps(res, default=data_parser)), 200


@namespace.route('/history/list')
class HistoryList(Resource):
    @namespace.response(200, "Success")
    def get(self):

        res = sms_mongodb.get_command_log_list()
        
        return json.loads(json.dumps(res, default=data_parser)), 200
