import json


def get_json_success(msg=None):
    if msg is None:
        msg = '成功'
    dick = {'code': 1, 'msg': msg, 'data': ''}
    return json.dumps(dick, ensure_ascii=False)


def get_json_error(msg=None):
    if msg is None:
        msg = '错误'
    dick = {'code': 0, 'msg': msg, 'data': ''}
    return json.dumps(dick, ensure_ascii=False)


def get_json_common(code, msg, data):
    dick = {'code': code, 'msg': msg, 'data': data}
    return json.dumps(dick, ensure_ascii=False)
