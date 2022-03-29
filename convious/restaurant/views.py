from http.client import METHOD_NOT_ALLOWED
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework import permissions
from convious.restaurant.serializers import *
from drf_rw_serializers import generics
from django.http.response import Http404
from rest_framework.exceptions import MethodNotAllowed
import datetime


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created, viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be created, viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows restaurants to be created, viewed or edited.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class VoteViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows votes to be created, viewed or edited.
    """

    queryset = Vote.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # This is some boilerplate code that's neccessary to allow different serializers for different action classes.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serializer_action_classes = {
            "list": VoteSerializer,
            "create": VoteSerializerCreate,
            "retrieve": VoteSerializer,
            "update": VoteSerializerCreate,
            "partial_update": VoteSerializer,
            "destroy": VoteSerializer,
        }

    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs["partial"] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(VoteViewSet, self).get_serializer_class()


class DailyWinnerViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows daily winners to be viewed.
    """

    queryset = DailyWinner.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "date"
    serializer_class = DailyWinnerSerializer
