__author__ = 'warprobot'

from API.DBTools import threads, posts, subscriptions
from API.Views.helpers import return_response, get_related, test_required, get_optional, GET_parameters, return_error
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":

        request_data = json.loads(request.body)
        required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        optional = get_optional(request_data=request_data, possible_values=["isDeleted"])
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.save_thread(forum=request_data["forum"], title=request_data["title"], isClosed=request_data["isClosed"],
                                     user=request_data["user"], date=request_data["date"], message=request_data["message"],
                                     slug=request_data["slug"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def details(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["thread"]
        related = get_related(request_data)
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.details(id=request_data["thread"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def vote(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "vote"]
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.vote(id=request_data["thread"], vote=request_data["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def subscribe(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            test_required(data=request_data, required=required_data)
            subscription = subscriptions.save_subscription(email=request_data["user"], thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def unsubscribe(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            test_required(data=request_data, required=required_data)
            subscription = subscriptions.remove_subscription(email=request_data["user"], thread_id=request_data["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=400)


def open(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.open_close_thread(id=request_data["thread"], isClosed=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def close(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.open_close_thread(id=request_data["thread"], isClosed=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread", "slug", "message"]
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.update_thread(id=request_data["thread"], slug=request_data["slug"], message=request_data["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def remove(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.remove_restore(thread_id=request_data["thread"], status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def restore(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=request_data, required=required_data)
            thread = threads.remove_restore(thread_id=request_data["thread"], status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=400)


def thread_list(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        identificator = None
        try:
            identificator = request_data["forum"]
            entity = "forum"
        except KeyError:
            try:
                identificator = request_data["user"]
                entity = "user"
            except KeyError:
                return return_error("No user or forum parameters setted")
        optional = get_optional(request_data=request_data, possible_values=["limit", "order", "since"])
        try:
            t_list = threads.threads_list(entity=entity, identificator=identificator, related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(t_list)
    else:
        return HttpResponse(status=400)


def list_posts(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["thread"]
        entity = "thread"
        optional = get_optional(request_data=request_data, possible_values=["limit", "order", "since"])
        try:
            test_required(data=request_data, required=required_data)
            p_list = posts.posts_list(entity=entity, identificator=request_data["thread"], related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=400)