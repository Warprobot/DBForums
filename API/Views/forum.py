from API.tools.entities import forums, posts, threads

__author__ = 'warprobot'

from API.Views.helpers import related_exists, choose_required, intersection
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["name", "short_name", "user"]
        try:
            choose_required(data=content, required=required_data)
            forum = forums.save_forum(name=content["name"], short_name=content["short_name"],
                                      user=content["user"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": forum}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":
        get_params = request.GET.dict()
        required_data = ["forum"]
        related = related_exists(get_params)
        try:
            choose_required(data=get_params, required=required_data)
            forum = forums.details(short_name=get_params["forum"], related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": forum}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_threads(request):
    if request.method == "GET":
        content = request.GET.dict()
        required_data = ["forum"]
        related = related_exists(content)
        optional = intersection(request=content, values=["limit", "order", "since"])
        try:
            choose_required(data=content, required=required_data)
            threads_l = threads.threads_list(entity="forum", identifier=content["forum"],
                                             related=related, params=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": threads_l}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_posts(request):
    if request.method == "GET":
        content = request.GET.dict()
        required_data = ["forum"]
        related = related_exists(content)

        optional = intersection(request=content, values=["limit", "order", "since"])
        try:
            choose_required(data=content, required=required_data)
            posts_l = posts.posts_list(entity="forum", params=optional, identifier=content["forum"],
                                       related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": posts_l}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_users(request):
    if request.method == "GET":
        content = request.GET.dict()
        required_data = ["forum"]
        optional = intersection(request=content, values=["limit", "order", "since_id"])
        try:
            choose_required(data=content, required=required_data)
            users_l = forums.list_users(content["forum"], optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": users_l}), content_type='application/json')
    else:
        return HttpResponse(status=405)