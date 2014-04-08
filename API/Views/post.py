__author__ = 'warprobot'

import json
from django.http import HttpResponse
from API.DBTools import posts
from API.Views.helpers import test_required, return_response, get_optional, get_related, GET_parameters, return_error


"""
API functions for user
"""


def create(request):
    if request.method == "POST":

        request_data = json.loads(request.body)
        required_data = ["user", "forum", "thread", "message", "date"]
        optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        optional = get_optional(request_data=request_data, possible_values=optional_data)
        try:
            test_required(data=request_data, required=required_data)
            post = posts.create(date=request_data["date"], thread=request_data["thread"],
                                message=request_data["message"], user=request_data["user"],
                                forum=request_data["forum"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":

        request_data = GET_parameters(request)
        required_data = ["post"]
        related = get_related(request_data)
        try:
            test_required(data=request_data, required=required_data)
            post = posts.details(request_data["post"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def post_list(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        identificator = None
        try:
            identificator = request_data["forum"]
            entity = "forum"
        except KeyError:
            try:
                identificator = request_data["thread"]
                entity = "thread"
            except KeyError:
                return return_error("No thread or forum parameters in request")

        optional = get_optional(request_data=request_data, possible_values=["limit", "order", "since"])
        try:
            p_list = posts.posts_list(entity=entity, identificator=identificator, related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post"]
        try:
            test_required(data=request_data, required=required_data)
            post = posts.remove_restore(post_id=request_data["post"], status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post"]
        try:
            test_required(data=request_data, required=required_data)
            post = posts.remove_restore(post_id=request_data["post"], status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post", "message"]
        try:
            test_required(data=request_data, required=required_data)
            post = posts.update(id=request_data["post"], message=request_data["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["post", "vote"]
        try:
            test_required(data=request_data, required=required_data)
            post = posts.vote(id=request_data["post"], vote=request_data["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=400)