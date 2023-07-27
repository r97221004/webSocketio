from flask_restplus import fields, reqparse

from app.api.v1.command_endpoint import namespace

command_payload = namespace.model('payload', {
    'username': fields.String(description='device id', example='G00414'),
    'host': fields.String(description='host IP', example='127.0.0.1'),
    'port': fields.Integer(description='host port', example='5000')
})

command = namespace.model('command', {
    'command': fields.String(description='指令ID', example='reportUrl'),
    'phone': fields.String(description='目標門號', example='0912345678'),
    'telecom': fields.String(description='電信業者', example='FET'),
    'payload': fields.Nested(description='指令參數', model=command_payload)
})

history = reqparse.RequestParser()
history.add_argument('device_id', type=str, help='設備uid', required=True)
history.add_argument('head_id', type=str, help='最新 oid')
history.add_argument('end_id', type=str, help='最舊 oid')
history.add_argument('limit', type=int, help='每次載入筆數', default=10)


history_search = reqparse.RequestParser()
history_search.add_argument('device_id', type=str,
                            help='設備uid', default='G00414')
history_search.add_argument('q', type=str, help='搜尋條件', default='reportUrl')
