from convious.restaurant.models import *
from django.db.models import Sum, Count

# Celery is overkill. Let's try Huey.
# TODO: Configure Huey with Django
# https://huey.readthedocs.io/en/latest/contrib.html#django
# For now, run it like this:
# ./manage.py run_huey
# doesn't work on windows
from huey import SqliteHuey
from huey import crontab

huey = SqliteHuey(filename="/tmp/job.db")

# Deletes all old vote counts
@huey.periodic_task(crontab(minute="0", hour="0"))
def reset_votecount(self):
    VoteCount.objects.all().delete()


# Generate daily winners for all dates that have votes in them
@huey.periodic_task(crontab(minute="0", hour="0"))
def generate_daily_winners():
    # Create a daily winner for this date
    def create_daily_winner(eligible_date):
        top_restaurants_for_eligible_date = (
            Vote.objects.filter(created=eligible_date)
            .values("restaurant")
            .annotate(total_score=Sum("weight"), total_users=Count("user"))
            .order_by("-total_score", "-total_users")
        )
        winner = top_restaurants_for_eligible_date.first()["restaurant"]
        DailyWinner.objects.create(date=eligible_date, restaurant_id=winner)

    distinct_dates = list(Vote.objects.values("created").distinct())
    for vote in distinct_dates:
        eligible_date = vote["created"]
        if DailyWinner.objects.filter(date=eligible_date).exists():
            print(f"{eligible_date} winner exists!")
        else:
            print(f"creating {eligible_date} winner...")
            create_daily_winner(eligible_date)
            print(f"created {eligible_date} winner.")

    # def create_daily_winner(eligible_date):
    # votes = list(
    #     Vote.objects.filter(created=eligible_date)
    #     .values("restaurant")
    #     .annotate(total_score=Sum("weight"), total_users=Count("user"))
    #     .order_by("total_score")
    # )
    # highest_score = max([v["total_score"] for v in votes])
    # top_scores = [v for v in votes if v["total_score"] == highest_score]

    # winner = None
    # if len(top_scores) == 1:
    #     winner = top_scores[0]["restaurant"]
    # elif len(top_scores) > 1:
    #     most_unique_votes = max([v["total_users"] for v in top_scores])
    #     top_unique_votes = [
    #         v for v in votes if v["total_users"] == most_unique_votes
    #     ]
    #     if len(top_unique_votes) == 1:
    #         winner = top_unique_votes[0]["restaurant"]
    #     elif len(top_unique_votes) > 1:
    #         print("WARNING!!! multiple winners, randomly choosing one!")
    #         winner = top_unique_votes[0]["restaurant"]
    #     else:
    #         print("WARNING!!! Bug! No winner!")
    # else:
    #     print("WARNING!!! Bug! No winner!")
