from API.tools.entities import forums, posts, threads

__author__ = 'warprobot'

from API.Views.helpers import get_related, return_response, test_required, extras, GET_parameters, return_error
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["name", "short_name", "user"]
        try:
            test_required(data=content, required=required_data)
            forum = forums.save_forum(name=content["name"], short_name=content["short_name"],
                                      user=content["user"])
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":
        content = GET_parameters(request)
        required_data = ["forum"]
        related = get_related(content)
        try:
            test_required(data=content, required=required_data)
            forum = forums.details(short_name=content["forum"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=405)


def list_threads(request):
    if request.method == "GET":
        content = GET_parameters(request)
        required_data = ["forum"]
        related = get_related(content)
        optional = extras(request=content, values=["limit", "order", "since"])
        try:
            test_required(data=content, required=required_data)
            threads_l = threads.threads_list(entity="forum", identificator=content["forum"],
                                             related=related, params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(threads_l)
    else:
        return HttpResponse(status=405)


def list_posts(request):
    if request.method == "GET":
        content = GET_parameters(request)
        required_data = ["forum"]
        related = get_related(content)

        optional = extras(request=content, values=["limit", "order", "since"])
        try:
            test_required(data=content, required=required_data)
            posts_l = posts.posts_list(entity="forum", params=optional, identifier=content["forum"],
                                       related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_l)
    else:
        return HttpResponse(status=405)


def list_users(request):
    if request.method == "GET":
        content = GET_parameters(request)
        required_data = ["forum"]
        optional = extras(request=content, values=["limit", "order", "since_id"])
        try:
            test_required(data=content, required=required_data)
            users_l = forums.list_users(content["forum"], optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(users_l)
    else:
        return HttpResponse(status=405)