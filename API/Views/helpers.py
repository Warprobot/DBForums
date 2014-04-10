__author__ = 'warprobot'

import json
from django.http import HttpResponse

"""
Helpers to make HttpResponses
"""


def get_related(request):
    try:
        related = request["related"]
    except KeyError:
        related = []
    return related


def extras(request, values):
    optional = {}
    for value in values:
        try:
            optional[value] = request[value]
        except Exception:
            continue
    return optional


def GET_parameters(request_data):
    data = {}
    for el in request_data.GET:
        data[el] = request_data.GET.get(el)
    return data


def return_response(response):
    content = {"code": 0, "response": response}
    return HttpResponse(json.dumps(content), content_type='application/json')


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