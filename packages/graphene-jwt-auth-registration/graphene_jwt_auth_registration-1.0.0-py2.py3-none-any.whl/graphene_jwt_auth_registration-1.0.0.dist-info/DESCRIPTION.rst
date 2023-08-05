==============================
Graphene JWT Auth Registration
==============================

.. image:: https://badge.fury.io/py/graphene-jwt-auth-registration.svg
    :target: https://badge.fury.io/py/graphene-jwt-auth-registration

.. image:: https://travis-ci.org/fivethreeo/graphene-jwt-auth-registration.svg?branch=master
    :target: https://travis-ci.org/fivethreeo/graphene-jwt-auth-registration

.. image:: https://codecov.io/gh/fivethreeo/graphene-jwt-auth-registration/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/fivethreeo/graphene-jwt-auth-registration

Authentication and registration using graphene and JWT 

Documentation
-------------

.. The full documentation is at https://graphene-jwt-auth.readthedocs.io.

Quickstart
----------

Install Graphene JWT Auth Registration::

    pip install graphene-jwt-auth-registration

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",

        ...

        "djoser",
        "graphene_django",

        "gjwt_auth",
    ]

Set AUTH_USER_MODEL:

.. code-block:: python

    AUTH_USER_MODEL = "gjwt_auth.User"

Add JSONWebTokenBackend backend to your AUTHENTICATION_BACKENDS:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JSONWebTokenBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

Add the JSONWebTokenMiddleware:

.. code-block:: python

    GRAPHENE = {
        'SCHEMA': 'yourproject.schema.schema',
        'MIDDLEWARE': [
            'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ],
    }

Create graphene schema in `yourproject/schema.py`: 

.. code-block:: python

    import graphene
    import graphql_jwt

    from gjwt_auth.mutations import (
        Activate,
        DeleteAccount,
        Register,
        ResetPassword,
        ResetPasswordConfirm,
    )

    from gjwt_auth.schema import User, Viewer


    class RootQuery(graphene.ObjectType):
        viewer = graphene.Field(Viewer)

        def resolve_viewer(self, info, **kwargs):
            if info.context.user.is_authenticated:
                return info.context.user
            return None


    class Mutation(graphene.ObjectType):
        activate = Activate.Field()
        register = Register.Field()
        deleteAccount = DeleteAccount.Field()
        resetPassword = ResetPassword.Field()
        resetPasswordConfirm = ResetPasswordConfirm.Field()

        token_auth = graphql_jwt.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()

    schema = graphene.Schema(query=RootQuery, mutation=Mutation)


Set djoser setttings:

.. code-block:: python

    DOMAIN = os.environ.get('DJANGO_DJOSER_DOMAIN', 'localhost:3000')
    SITE_NAME = os.environ.get('DJANGO_DJOSER_SITE_NAME', 'my site')

    DJOSER = {

        'PASSWORD_RESET_CONFIRM_URL': '?action=set-new-password&uid={uid}&token={token}',
        'ACTIVATION_URL': 'activate?uid={uid}&token={token}',
        'SEND_ACTIVATION_EMAIL': True,
    }

    }

Add Graphenes URL patterns:

.. code-block:: python


    from django.conf.urls import url
    from django.views.decorators.csrf import csrf_exempt

    from graphene_django.views import GraphQLView

    ...

    urlpatterns = [
        ...
        url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
        ...
    ]

.. Features
   --------

   * TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2019-06-04)
++++++++++++++++++

* First release on PyPI.


