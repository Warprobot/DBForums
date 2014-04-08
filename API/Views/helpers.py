__author__ = 'warprobot'

import json
from django.http import HttpResponse

"""
Helpers to make HttpResponses
"""


def get_related(request_data):
    try:
        related = request_data["related"]
    except KeyError:
        related = []
    return related


def get_optional(request_data, possible_values):
    optional = {}
    for value in possible_values:
        try:
            optional[value] = request_data[value]
        except KeyError:
            continue
    return optional


def GET_parameters(request_data):
    data = {}
    for el in request_data.GET:
        #if el == "related":
        #    data["related"] = request_data.GET.get(el)#getlist("related")
        #else:
        data[el] = request_data.GET.get(el)
    return data


def return_response(object):
    response_data = {"code": 0, "response": object}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def return_error(message):
    response_data = {"code": 1, "response": message}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def test_required(data, required):
    for el in required:
        if el not in data:
            raise Exception("required element " + el + " not in parameters")
        if data[el] is not None:
            try:
                data[el] = data[el].encode('utf-8')
            except Exception:
                continue

    return