from flask_restplus import reqparse


deviceinfo = reqparse.RequestParser()
deviceinfo.add_argument('type', type=str, help='設備類型', default='gps')
deviceinfo.add_argument('serial_id', type=int, help='設備 ID', default=414)

suggestion = reqparse.RequestParser()
suggestion.add_argument('type', type=str, help='查詢類型', default='gps')

rf_gps_caseprj = reqparse.RequestParser()
rf_gps_caseprj.add_argument('caseprj_uid', type=str,
                            help='個案uid')
