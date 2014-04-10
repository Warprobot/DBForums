from API.tools.entities import posts, threads, subscriptions

__author__ = 'warprobot'

from API.Views.helpers import related_exists, choose_required, intersection
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":

        content = json.loads(request.body)
        required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        optional = intersection(request=content, values=["isDeleted"])
        try:
            choose_required(data=content, required=required_data)
            thread = threads.save_thread(forum=content["forum"], title=content["title"],
                                         isClosed=content["isClosed"],
                                         user=content["user"], date=content["date"],
                                         message=content["message"],
                                         slug=content["slug"], optional=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":
        content = request.GET.dict()
        required_data = ["thread"]
        related = related_exists(content)
        try:
            choose_required(data=content, required=required_data)
            thread = threads.details(id=content["thread"], related=related)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def vote(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "vote"]
        try:
            choose_required(data=content, required=required_data)
            thread = threads.vote(id=content["thread"], vote=content["vote"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def subscribe(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            choose_required(data=content, required=required_data)
            subscription = subscriptions.save_subscription(email=content["user"], thread_id=content["thread"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": subscription}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def unsubscribe(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            choose_required(data=content, required=required_data)
            subscription = subscriptions.remove_subscription(email=content["user"],
                                                             thread_id=content["thread"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": subscription}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def open(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            choose_required(data=content, required=required_data)
            thread = threads.open_close_thread(id=content["thread"], isClosed=0)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def close(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            choose_required(data=content, required=required_data)
            thread = threads.open_close_thread(id=content["thread"], isClosed=1)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def update(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "slug", "message"]
        try:
            choose_required(data=content, required=required_data)
            thread = threads.update_thread(id=content["thread"], slug=content["slug"],
                                           message=content["message"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def remove(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            choose_required(data=content, required=required_data)
            thread = threads.remove_restore(thread_id=content["thread"], status=1)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def restore(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            choose_required(data=content, required=required_data)
            thread = threads.remove_restore(thread_id=content["thread"], status=0)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": thread}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def thread_list(request):
    if request.method == "GET":
        content = request.GET.dict()
        try:
            identifier = content["forum"]
            entity = "forum"
        except KeyError:
            try:
                identifier = content["user"]
                entity = "user"
            except KeyError:
                return HttpResponse(json.dumps({"code": 1, "response": "Any methods?"}),
                                    content_type='application/json')
        optional = intersection(request=content, values=["limit", "order", "since"])
        try:
            t_list = threads.threads_list(entity=entity, identifier=identifier, related=[], params=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": t_list}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_posts(request):
    if request.method == "GET":
        content = request.GET.dict()
        required_data = ["thread"]
        entity = "thread"
        optional = intersection(request=content, values=["limit", "order", "since"])
        try:
            choose_required(data=content, required=required_data)
            p_list = posts.posts_list(entity=entity, params=optional, identifier=content["thread"], related=[])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": p_list}), content_type='application/json')
    else:
        return HttpResponse(status=405)