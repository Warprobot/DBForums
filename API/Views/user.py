from API.tools.entities import users, posts, followers

__author__ = 'warprobot'

"""
API functions for user
"""

from API.Views.helpers import return_response, test_required, extras, GET_parameters, return_error
import json
from django.http import HttpResponse


def create(request):
    if request.method == "POST":

        request_data = json.loads(request.body)
        required_data = ["email", "username", "name", "about"]
        optional = extras(request=request_data, values=["isAnonymous"])
        try:
            test_required(data=request_data, required=required_data)
            user = users.save_user(email=request_data["email"], username=request_data["username"],
                                   about=request_data["about"], name=request_data["name"], optional=optional)
        except Exception as e:
            return return_error(e.message)
        return return_response(user)
    else:
        return HttpResponse(status=405)


def details(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        try:
            test_required(data=request_data, required=required_data)
            user_details = users.details(email=request_data["user"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user_details)
    else:
        return HttpResponse(status=405)


def follow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            test_required(data=request_data, required=required_data)
            following = followers.add_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following)
    else:
        return HttpResponse(status=405)


def unfollow(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["follower", "followee"]
        try:
            test_required(data=request_data, required=required_data)
            following = followers.remove_follow(email1=request_data["follower"], email2=request_data["followee"])
        except Exception as e:
            return return_error(e.message)
        return return_response(following)
    else:
        return HttpResponse(status=405)


def list_followers(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        followers_param = extras(request=request_data, values=["limit", "order", "since_id"])
        try:
            test_required(data=request_data, required=required_data)
            follower_l = followers.followers_list(email=request_data["user"], type="follower", params=followers_param)
        except Exception as e:
            return return_error(e.message)
        return return_response(follower_l)
    else:
        return HttpResponse(status=405)


def list_following(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        followers_param = extras(request=request_data, values=["limit", "order", "since_id"])
        try:
            test_required(data=request_data, required=required_data)
            followings = followers.followers_list(email=request_data["user"], type="followee", params=followers_param)
        except Exception as e:
            return return_error(e.message)
        return return_response(followings)
    else:
        return HttpResponse(status=405)


def list_posts(request):
    if request.method == "GET":
        request_data = GET_parameters(request)
        required_data = ["user"]
        optional = extras(request=request_data, values=["limit", "order", "since"])
        try:
            test_required(data=request_data, required=required_data)
            posts_l = posts.posts_list(entity="user", params=optional, identifier=request_data["user"], related=[])
        except Exception as e:
            return return_error(e.message)
        return return_response(posts_l)
    else:
        return HttpResponse(status=405)


def update(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        required_data = ["user", "name", "about"]
        try:
            test_required(data=request_data, required=required_data)
            user = users.update_user(email=request_data["user"], name=request_data["name"], about=request_data["about"])
        except Exception as e:
            return return_error(e.message)
        return return_response(user)
    else:
        return HttpResponse(status=405)