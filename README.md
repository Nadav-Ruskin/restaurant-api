# Hello

This repository contains the code for an API that serves a restaurant daily ranking service.
As well as code, it also includes some testing data and configuration information. These kind of files do not normally belong in a repository, but are distributed anyway for convenience. 

This solution utilizes Django Rest Framework. It also uses Huey for task scheduling.

There is only one app, named "restaurant". It has a bunch of views, serializers, models, and some helper functions, which have a TODO to be moved to their own python files.

The code and this README have a few todos. You can find all of them by looking up "TODO" using your favorite grep tool (like visual studio code).

## Files
`.vscode/launch.json` - Vscode config for debugging django

`convious/__init__.py`

`convious/asgi.py` - Default asgi file

`convious/settings.py` - Django settings file

`convious/urls.py` - Urls file

`convious/wsgi.py` - Default asgi file

`convious/restaurant/__init__.py`

`convious/restaurant/admin.py` - Default admin file

`convious/restaurant/apps.py` - Default apps file

`convious/restaurant/models.py` - Restaurant models

`convious/restaurant/serializers.py` - Restaurant serializers

`convious/restaurant/tasks.py` - Restaurant Huey periodic jobs

`convious/restaurant/tests.py` - Restaurant tests... empty for now

`convious/restaurant/views.py` - Restaurant views

`db.sqlite3` - Debug environment database

`manage.py` - Default manage file

`readme.MD` - You're standing here <-

`requirements.pdf` - This project's business requirements

`requirements.txt` - Python requirements file

`settings.HUEY` - Huey settings file

## Requirements
```
1. Everyone can add/remove/update restaurants
```
This is implemented using the /restaurants endpoint and the Restaurant model.

```
2. Every user gets X (hardcoded, but "configurable") votes per
day. Each vote has a "weight". First user vote on the same
restaurant counts as 1, second as 0.5, 3rd and all subsequent
votes as 0.25.
2.1. If a voting result is the same on multiple restaurants, the
winner is the one who got more distinct users to vote on it.
```
Configurable vote count: implemented using an environment variable and a default setting.
Vote count: Implemented with a dedicated model: VoteCount.
Vote weight: Calculated by the API on the fly using VoteCount.
Winner calculation: Implemented with the model DailyWinner, it is calculated every day by a periodic task in `convious\restaurant\tasks.py`.
The API endpoint is /votes

```
3. Every day vote amounts are reset. Unused previous day votes are
lost.
```
VoteCount is reset every day by a periodic task in `convious\restaurant\tasks.py`.

```
4. Show the history of selected restaurants per time period. For
example, the front-end should be able to query which restaurant
won the vote on a specific day.
```
This is implemented using the /dailywinners endpoint and the Restaurant model. Currently it only supports listing all restaurants and quarying specific dates.
TODO: Add query support for arbitrary time periods (e.g. 2022-03-01 to 2022-03-30).

```
5. Do not forget that frontend dev will need a way to show which
restaurants users can vote on and which restaurant is a winner
```
This is implemented using the /restaurants endpoint and the Restaurant model.
Currently, the API required user authentication, which we may not want.
TODO: Remove user authentication requirement from parts of the API where it is not wanted, TBD.

```
6. Readme on how to use the API, launch the project, etc.
```
You're standing here <-


## How to use

### Settings up a venv, installing prerequisites:
```bash
# Optional, making sure that we have the venv package installed, for example using Ubuntu:
apt-get install -y python3-venv

# Installing a new venv in the project directory:
python -m venv venv
# “Activating” the virtual environment. This shell session will now be using the virtual environment instead of the global interpreter:
. venv/bin/activate
# Installing all requirements in venv:
pip install -r requirements.txt
```

### Bootstapping the server
```bash
python manage.py migrate
```

### Running the server
```bash
python manage.py runserver
```

### Debugging using vscode
If your vscode has a Python extension, open any file and debug. The repository includes the needed configuration.




------------
all content by Nadav Ruskin
------------
