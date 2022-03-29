from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from sympy import true


class Restaurant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, unique=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name


class Vote(models.Model):
    created = models.DateField(auto_now_add=True, null=False, blank=False)
    user = models.ForeignKey(User, related_name="votes", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, related_name="votes", on_delete=models.CASCADE
    )
    weight = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    class Meta:
        ordering = ["restaurant"]


class VoteCount(models.Model):
    """
    A utility model, made to make life easier when tallying how many votes a user has cast today.
    Doesn't actually store date, because it's easier to just reset the vote count with a daily task at tasks.py
    """

    user = models.OneToOneField(
        User, verbose_name=("User"), primary_key=True, on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    class Meta:
        ordering = ["user"]


class DailyWinner(models.Model):
    date = models.DateField(auto_now_add=True, null=False, blank=False, unique=True)
    restaurant = models.ForeignKey(
        Restaurant, related_name="win_dates", on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ["date"]
