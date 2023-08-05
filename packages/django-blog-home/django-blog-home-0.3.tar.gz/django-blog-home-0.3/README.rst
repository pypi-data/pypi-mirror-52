=====
Home
=====

Home is a simple Django app to conduct Web-based Blog Home. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'home',
    ]

2. Include the polls URLconf in your project urls.py like this::
    path('', include('home.urls')),

3. Run `python manage.py migrate` to create the home models.

4. Visit http://127.0.0.1:8000/ to participate in the poll.