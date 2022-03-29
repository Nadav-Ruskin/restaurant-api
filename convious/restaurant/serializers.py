from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from datetime import date
from datetime import timedelta

import os

# TODO: Use django-environ ? Put max_votes in settings.py?
max_votes = os.getenv("MAX_VOTES", 50)


# TODO: Put exceptions in an exceptions.py file
import rest_framework.exceptions


class VoteLimitException(rest_framework.exceptions.APIException):
    status_code = 429
    detail = (
        f"Maximum votes reached. You cannot vote more than {max_votes} times a day."
    )


# class DailyWinnerNotYetException(rest_framework.exceptions.APIException):
#     status_code = 409
#     yesterday = date.today() - timedelta(days=1)
#     detail = f"Daily winners can only exist in past days. The latest available date is yesterday: {yesterday}"


class DailyWinnerNoVotesException(rest_framework.exceptions.APIException):
    status_code = 404
    yesterday = date.today() - timedelta(days=1)

    def __init__(self, date):
        super().__init__()
        self.detail = f"No votes were found on {date}"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["url", "created", "name"]


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ["url", "user", "restaurant", "weight"]


# Used for create votes. A different class from VoteSerializer because it's currently the best way to expose different fields for different request types.
class VoteSerializerCreate(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ["url", "restaurant"]
        read_only_fields = ["user", "weight"]

    def create(self, validated_data):
        user = self.context["request"].user
        return VoteManager.create_vote(user, validated_data)

    def to_representation(self, instance):
        serializer = VoteSerializer(
            instance, context={"request": self.context["request"]}
        )
        return serializer.data


# Todo: Move this helper class to a seperate file.
class VoteManager:
    """
    Generates a vote and manipulates vote count model
    Input: user and vote data
    Output: Generated vote
    Exceptions: VoteLimitException() if the daily vote limit has been reached
    """

    @staticmethod
    def create_vote(user, data):
        processed_data = dict(data)
        try:
            vote_count_today = VoteCount.objects.get(user=user)
        except VoteCount.DoesNotExist:
            vote_count_today = VoteCount.objects.create(user=user)
            vote_weight = 4
        else:
            if vote_count_today.count > max_votes:
                raise VoteLimitException()
            if vote_count_today.count == 1:
                vote_weight = 3
            elif vote_count_today.count == 2:
                vote_weight = 2
            else:
                vote_weight = 1
            vote_count_today.count += 1

        processed_data["weight"] = vote_weight
        processed_data["user"] = user

        # Only save the new vote count after the vote has been cast correctly to guarantee some level of atomicity...
        returned_object = Vote.objects.create(**processed_data)
        vote_count_today.save()
        return returned_object


class DailyWinnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailyWinner
        fields = ["url", "date", "restaurant"]
        lookup_field = "date"
        extra_kwargs = {"url": {"lookup_field": "date"}}
