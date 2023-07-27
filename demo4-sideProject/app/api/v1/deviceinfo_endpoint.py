import json
from flask_restplus import Resource
from flask_restplus import Namespace
from itertools import groupby
from app.api.v1.deviceinfo_model import deviceinfo, suggestion, rf_gps_caseprj
from app.exception import ResourceNotFound

from app.adaptor import mssql
from app.adaptor.mongodb import moj_mongodb


namespace = Namespace('deviceinfo', description='Get device information')


@namespace.route('/')
class device_info(Resource):
    @namespace.expect(deviceinfo)
    @namespace.response(200, "Success")
    def get(self):
        args = deviceinfo.parse_args()
        device_type = args.get('type')
        serial_id = args.get('serial_id')
        if device_type not in ['gps', 'rf']:
            raise ResourceNotFound

        result = mssql.get_device_info(serial_id, device_type)

        return result, 200


@namespace.route('/suggestion')
class device_suggest(Resource):
    @namespace.expect(suggestion)
    @namespace.response(200, "Success")
    def get(self):
        args = suggestion.parse_args()
        info_type = args.get('type')
        res = []
        if info_type in ['gps', 'rf']:
            result = mssql.get_device_id_suggestion(info_type)
            res = list(map(lambda i: str(i.get('serial_id')), result))

        elif info_type == 'whitelist':
            res = mssql.get_whitelist_suggestion()

        elif info_type == 'phonebook':
            data = mssql.get_phonebook_suggestion()
            for district, value in groupby(data, key=lambda x: x['district']):
                district_group = {
                    'district': district,
                    'detail': []
                }
                for i in value:
                    district_group['detail'].append({
                        'name': i['name'],
                        'phone': i['phone']
                    })
                res.append(district_group)

        else:
            raise ResourceNotFound

        return res, 200


@namespace.route('/rf_gps_device')
class rf_gps_device(Resource):
    @namespace.expect(rf_gps_caseprj)
    @namespace.response(200, "Success")
    def get(self):
        args = rf_gps_caseprj.parse_args()
        caseprj_uid = args.get("caseprj_uid")
        result = moj_mongodb.get_rf_gps_device_id(caseprj_uid)
        return json.loads(json.dumps(result))
