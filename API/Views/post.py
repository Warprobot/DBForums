from API.tools.entities import posts

__author__ = 'warprobot'

import json
from django.http import HttpResponse
from API.Views.helpers import test_required, return_response, extras, get_related, GET_parameters, return_error


"""
API functions for user
"""


def create(request):
    if request.method == "POST":

        content = json.loads(request.body)
        required_data = ["user", "forum", "thread", "message", "date"]
        optional_data = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
        optional = extras(request=content, values=optional_data)
        try:
            test_required(data=content, required=required_data)
            post = posts.create(date=content["date"], thread=content["thread"],
                                message=content["message"], user=content["user"],
                                forum=content["forum"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":

        content = GET_parameters(request)
        required_data = ["post"]
        related = get_related(content)
        try:
            test_required(data=content, required=required_data)
            post = posts.details(content["post"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=405)


def post_list(request):
    if request.method == "GET":
        content = GET_parameters(request)
        try:
            identifier = content["forum"]
            entity = "forum"
        except KeyError:
            try:
                identifier = content["thread"]
                entity = "thread"
            except KeyError:
                return return_error("No thread or forum parameters in request")

        optional = extras(request=content, values=["limit", "order", "since"])
        try:
            p_list = posts.posts_list(entity=entity, params=optional, identifier=identifier, related=[])
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=405)


def remove(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["post"]
        try:
            test_required(data=content, required=required_data)
            post = posts.remove_restore(post_id=content["post"], status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=405)


def restore(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["post"]
        try:
            test_required(data=content, required=required_data)
            post = posts.remove_restore(post_id=content["post"], status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=405)


def update(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["post", "message"]
        try:
            test_required(data=content, required=required_data)
            post = posts.update(update_id=content["post"], message=content["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=405)


def vote(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["post", "vote"]
        try:
            test_required(data=content, required=required_data)
            post = posts.vote(vote_id=content["post"], vote_type=content["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(post)
    else:
        return HttpResponse(status=405)