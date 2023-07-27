import sys
import traceback
from flask_socketio import SocketIO

import logging.config

NAMESPACE = '/index'

sio = None
log = logging.getLogger(__name__)


def init(flask_app):
    global sio

    try:
        sio = SocketIO(flask_app, logger=False, cors_allowed_origins="*")

    except Exception as e:
        log.debug(f'socketio init error: {e}')

    return sio


def server_sleep(sec: int):
    return sio.sleep(sec)


def handle_emit(event, data):
    try:
        sio.emit(event, data, namespace=NAMESPACE)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_message = ' traceback:' + \
            ''.join(traceback.format_tb(exc_traceback, 10)).replace("\n", "")
        log.error(f'emit {event} error: {e}' + traceback_message)
