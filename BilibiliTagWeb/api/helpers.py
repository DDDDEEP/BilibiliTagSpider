
def response_json(data={}, errmsg=''):
    result = {
        'status': 0,
        'data': data,
        'errors': [],
        'message': 'success'
    }
    if errmsg != '':
        result['status'] = 1
        result['data'] = {}
        result['message'] = errmsg
    return result


def check_dict_required_param(dict, params):
    for param in params:
        if dict.get(param) is None:
            return False
    return True
