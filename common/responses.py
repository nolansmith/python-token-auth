from flask import jsonify

def json_response(msg='There was an error', response_code_number=404, **kwargs):
    res = {'message': msg}
    for k in kwargs.keys():
        res[k] = kwargs.get(k)
    return jsonify(res), response_code_number