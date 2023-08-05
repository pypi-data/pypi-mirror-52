=================
Django Easy Login
=================

Django Easy Login is a Django app that allows end-users to login with already created users at the system without
authentication.

Quick start
-----------

1. Add 'easy_login' to your INSTALLED_APPS settings:

.. code-block:: python

    INSTALLED_APPS = [
    ...
    'easy_login',
    ...
    ]

2. Now edit the example/urls.py module in your project:

.. code-block:: python

    urlpatterns = [
    ...
    url(r'^easy_login/', include('easy_login.urls', namespace='easy-login')),
    ...
    ]


3. Set middleware class:

.. code-block:: python

    TEMPLATES = [
        ...
        'context_processors': [
            'easy_login.context_processors.easy_login',
        ...
        ],
    ]

4. Define default url redirect:

.. code-block:: python

    EASY_URL_REDIRECT = 'test-app:index'

5. In template define easy_login variable:

.. code-block:: python

    {{ easy_login }}

Customization
-------------

You can change the view settings up to your wishes.
For customizing view settings please put this to the settings:

.. code-block:: python

    EASY_LOGIN_SETTINGS = {
    'FILTER': {},           # --> dict;
    'LIMIT': None,          # --> int;
    'LABELS': [],           # --> list, lambda;
    'LOGIN_BY': '',         # --> str;
    'GET_BY': '',           # --> str;
    'LOGIN_BUTTON': ''      # --> str;
    }

Options:
--------

-   **FILTER** - possible type - **dict**; Using this option you can by the attributes filter objects which are
    shown in the select bar. For example ``'FILTER': {'username': 'admin'}``. By default - *None*.
-   **LIMIT** - possible type - **int**; Limit number of records in dropdown. You can put None if you don't want to
    limit the number of users for select. By default - *10*.
-   **LABELS** - possible type - **list**, **lambda**; You can change the label of users displayed in dropdown.
    For example you can add roles, permissions and any other important information. Also, you can use
    lambda expression here, for ex. ``'LABELS': lambda x: x.username + ' - ' + str(x.id)``.
    By default - *__str__* method of your object.
-   **LOGIN_BY** - possible type - **str**, values: **'select', 'id', 'both'**; You can enable login with select field,
    ID input or both. By default - *'both'*.
-   **GET_BY** - possible type - **str**; You can change attribute by which you will authorize. By default - *'id'*.
-   **LOGIN_BUTTON** - possible type - **str**; You can change login button label. By default - *'Login'*.
