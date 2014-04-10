from API.tools.entities import posts, threads, subscriptions

__author__ = 'warprobot'

from API.Views.helpers import return_response, get_related, test_required, extras, GET_parameters, return_error
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":

        content = json.loads(request.body)
        required_data = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
        optional = extras(request=content, values=["isDeleted"])
        try:
            test_required(data=content, required=required_data)
            thread = threads.save_thread(forum=content["forum"], title=content["title"],
                                         isClosed=content["isClosed"],
                                         user=content["user"], date=content["date"],
                                         message=content["message"],
                                         slug=content["slug"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":
        content = GET_parameters(request)
        required_data = ["thread"]
        related = get_related(content)
        try:
            test_required(data=content, required=required_data)
            thread = threads.details(id=content["thread"], related=related)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def vote(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "vote"]
        try:
            test_required(data=content, required=required_data)
            thread = threads.vote(id=content["thread"], vote=content["vote"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def subscribe(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            test_required(data=content, required=required_data)
            subscription = subscriptions.save_subscription(email=content["user"], thread_id=content["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=405)


def unsubscribe(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "user"]
        try:
            test_required(data=content, required=required_data)
            subscription = subscriptions.remove_subscription(email=content["user"],
                                                             thread_id=content["thread"])
        except Exception as e:
            return return_error(e.message)
        return return_response(subscription)
    else:
        return HttpResponse(status=405)


def open(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=content, required=required_data)
            thread = threads.open_close_thread(id=content["thread"], isClosed=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def close(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=content, required=required_data)
            thread = threads.open_close_thread(id=content["thread"], isClosed=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def update(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread", "slug", "message"]
        try:
            test_required(data=content, required=required_data)
            thread = threads.update_thread(id=content["thread"], slug=content["slug"],
                                           message=content["message"])
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def remove(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=content, required=required_data)
            thread = threads.remove_restore(thread_id=content["thread"], status=1)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def restore(request):
    if request.method == "POST":
        content = json.loads(request.body)
        required_data = ["thread"]
        try:
            test_required(data=content, required=required_data)
            thread = threads.remove_restore(thread_id=content["thread"], status=0)
        except Exception as e:
            return return_error(e.message)
        return return_response(thread)
    else:
        return HttpResponse(status=405)


def thread_list(request):
    if request.method == "GET":
        content = GET_parameters(request)
        identificator = None
        try:
            identificator = content["forum"]
            entity = "forum"
        except KeyError:
            try:
                identificator = content["user"]
                entity = "user"
            except KeyError:
                return return_error("No user or forum parameters setted")
        optional = extras(request=content, values=["limit", "order", "since"])
        try:
            t_list = threads.threads_list(entity=entity, identificator=identificator, related=[], params=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(t_list)
    else:
        return HttpResponse(status=405)


def list_posts(request):
    if request.method == "GET":
        content = GET_parameters(request)
        required_data = ["thread"]
        entity = "thread"
        optional = extras(request=content, values=["limit", "order", "since"])
        try:
            test_required(data=content, required=required_data)
            p_list = posts.posts_list(entity=entity, params=optional, identifier=content["thread"], related=[])
        except Exception as e:
            return return_error(e.message)
        return return_response(p_list)
    else:
        return HttpResponse(status=405)