__author__ = 'warprobot'


from API.DBTools import forums, threads, posts
from API.Views.helpers import get_related, return_response, test_required, get_optional, GET_parameters, return_error
import json
from django.http import HttpResponse

def create(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["name", "short_name", "user"]
        try:
            test_required(data=request_data, required=required_data)
            forum = forums.save_forum(name=request_data["name"], short_name=request_data["short_name"],
                                      user=request_data["user"])
        except Exception as e:
            print("name = " + request_data["name"])
            print("short_name = " + request_data["short_name"])
            print("user = " + request_data["user"])
            print(e.message)
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        related = get_related(request_data)
        try:
            test_required(data=request_data, required=required_data)
            forum = forums.details(short_name=request_data["forum"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(forum)
    else:
        return HttpResponse(status=400)


def list_threads(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        related = get_related(request_data)
        optional = get_optional(request_data=request_data, possible_values=["limit", "order", "since"])
        try:
            test_required(data=request_data, required=required_data)
            threads_l = threads.threads_list(entity="forum", identificator=request_data["forum"],
                                             related=related, params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(threads_l)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        related = get_related(request_data)

        optional = get_optional(request_data=request_data, possible_values=["limit", "order", "since"])
        try:
            test_required(data=request_data, required=required_data)
            posts_l = posts.posts_list(entity="forum", identificator=request_data["forum"],
                                       related=related, params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_l)
    else:
        return HttpResponse(status=400)


def list_users(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["forum"]
        optional = get_optional(request_data=request_data, possible_values=["limit", "order", "since_id"])
        try:
            test_required(data=request_data, required=required_data)
            users_l = forums.list_users(request_data["forum"], optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(users_l)
    else:
        return HttpResponse(status=400)