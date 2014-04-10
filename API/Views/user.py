from API.tools.entities import users, posts, followers

__author__ = 'warprobot'

"""
API functions for user
"""

from API.Views.helpers import choose_required, extras
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":

        request_data = json.loads(request.body)
        required_data = ["email", "username", "name", "about"]
        optional = extras(request=request_data, values=["isAnonymous"])
        try:
            choose_required(data=request_data, required=required_data)
            user = users.save_user(email=request_data["email"], username=request_data["username"],
                                   about=request_data["about"], name=request_data["name"], optional=optional)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": user}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        required_data = ["user"]
        try:
            choose_required(data=request_data, required=required_data)
            user_details = users.details(email=request_data["user"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": user_details}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def follow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            choose_required(data=request_data, required=required_data)
            following = followers.add_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": following}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def unfollow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            choose_required(data=request_data, required=required_data)
            following = followers.remove_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": following}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_followers(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        required_data = ["user"]
        followers_param = extras(request=request_data, values=["limit", "order", "since_id"])
        try:
            choose_required(data=request_data, required=required_data)
            follower_l = followers.followers_list(email=request_data["user"], type="follower", params=followers_param)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": follower_l}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_following(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        required_data = ["user"]
        followers_param = extras(request=request_data, values=["limit", "order", "since_id"])
        try:
            choose_required(data=request_data, required=required_data)
            followings = followers.followers_list(email=request_data["user"], type="followee", params=followers_param)
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": followings}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def list_posts(request):
    if request.method == "GET":
        request_data = request.GET.dict()
        required_data = ["user"]
        optional = extras(request=request_data, values=["limit", "order", "since"])
        try:
            choose_required(data=request_data, required=required_data)
            posts_l = posts.posts_list(entity="user", params=optional, identifier=request_data["user"], related=[])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": posts_l}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["user", "name", "about"]
        try:
            choose_required(data=request_data, required=required_data)
            user = users.update_user(email=request_data["user"], name=request_data["name"], about=request_data["about"])
        except Exception as e:
            return HttpResponse(json.dumps({"code": 1, "response": (e.message)}), content_type='application/json')
        return HttpResponse(json.dumps({"code": 0, "response": user}), content_type='application/json')
    else:
        return HttpResponse(status=405)