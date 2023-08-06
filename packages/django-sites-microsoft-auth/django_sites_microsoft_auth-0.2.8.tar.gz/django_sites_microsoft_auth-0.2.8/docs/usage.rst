=====
Usage
=====

Quickstart
----------

1. Install `Django <https://docs.djangoproject.com/en/stable/topics/install/>`_
2. Install and configure the `Sites framework <https://docs.djangoproject.com/en/stable/ref/contrib/sites/#enabling-the-sites-framework>`_

    .. important::

        **Make sure you update the domain in your `Site` object**

        This needs to match the host (hostname + port) that you are using to
        access the Django site with. The easiest way to do this to go to
        `/admin/sites/site/1/change/` if you have the admin site enabled.

        `SITE_ID` is only required if want to use the `MicrosoftClient` without
        a request object (all of the code provided in this package uses a request
        object). If you want multiple `Site` objects and generate authorize URL
        when accessing your site from multiple domains, you *must not* set a `SITE_ID`

3. Create a `Azure AD App <https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade>`_.
   After you register the app, make sure you click on "Certificates & Secrets"
   and generate a new Client Secret.

    .. important::

        You will need Client ID and an Client Secret for step 5. Make sure
        you generate these and store them somewhere.

        When you are registering the app it will ask for a Redirect URI. This
        **must** match the absolute URL of your `sites_microsoft_auth:auth-callback`
        view. By default this would be `https://<your-domain>/microsoft/auth-callback/`.

        This URL **must be HTTPS** unless your hostname is `localhost`.
        `localhost` can **only** be used if `DEBUG` is set to `True`.
        Microsoft only allows HTTP authentication if the hostname is
        `localhost`.

4. Install package from PyPi

.. code-block:: console

    $ pip install django_sites_microsoft_auth

5. Create a `custom user model <https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#specifying-a-custom-user-model>`_

The easiest way to do this is to subclass `sites_microsoft_auth.models.SitesUser`.
You can also create your own custom user model that includes the following fields:

.. code-block:: python3

    from django.contrib.sites.models import Site
    import sites_microsoft_auth.models

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[sites_microsoft_auth.models.UnicodeSpaceUsernameValidator],
        unique=True,
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

6. Add the following to your `settings.py`

.. code-block:: python3

    INSTALLED_APPS = [
        # other apps...
        'django.contrib.sites',
        'sites_microsoft_auth',
    ]

    AUTH_USER_MODEL = 'app_name.YourCustomUserModel'

    TEMPLATES = [
        {
            # other template settings...
            'OPTIONS': {
                'context_processors': [
                    # other context_processors...
                    'sites_microsoft_auth.context_processors.microsoft',
                ],
            },
        },
    ]

    AUTHENTICATION_BACKENDS = [
        'sites_microsoft_auth.backends.MicrosoftAuthenticationBackend',
        'django.contrib.auth.backends.ModelBackend' # if you also want to use Django's authentication
        # I recommend keeping this with at least one database superuser in case of unable to use others
    ]

    # values you got from step 2 from your Mirosoft app
    MICROSOFT_AUTH_CLIENT_ID = 'your-client-id-from-apps.dev.microsoft.com'
    MICROSOFT_AUTH_CLIENT_SECRET = 'your-client-secret-from-apps.dev.microsoft.com'

    # pick one MICROSOFT_AUTH_LOGIN_TYPE value
    # Microsoft authentication
    # include Microsoft Accounts, Office 365 Enterpirse and Azure AD accounts
    MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

    # Xbox Live authentication
    MICROSOFT_AUTH_LOGIN_TYPE = 'xbl'  # Xbox Live authentication



7. Add the following to your `urls.py`

.. code-block:: python3

    urlpatterns = [
        # other urlpatterns...
        path('microsoft/', include('sites_microsoft_auth.urls', namespace='microsoft')),
    ]

8. Run migrations

.. code-block:: console

    $ python manage.py migrate

8. Start site and goto `/admin` to and logout if you are logged in.
9. Login as `Microsoft/Office 365/Xbox Live` user. It will fail. This will
   automatically create your new user.
10. Login as a `Password` user with access to change user accounts.
11. Go to `Admin -> Users` and edit your Microsoft user to have any permissions
    you want as you normally.

Test Site
---------

As part of unit testing, there minimal functioning site that is pimarily used
for running tests against and to help development. It can be used as a
reference for how to do some things.

The full reference site exists under `tests/site`

To setup,

1. Make sure you have installed the project `from sources <installation.html#from-sources>`_.
2. Get a Microsoft app with a Client ID and Client Secret following step 3
   above.
3. Create a `tests/site/local.py` file and add your
   `MICROSOFT_AUTH_CLIENT_ID` and `MICROSOFT_AUTH_CLIENT_SECRET` settings
4. Start up the site

.. code-block:: console

    $ python -m tests.site migrate
    $ python -m tests.site createsuperuser
    $ python -m tests.site runserver

5. Configure your `Site <http://localhost:8000/admin/sites/site>`_.


Sliencing `Scope has changed` warnings
--------------------------------------

If you stay on 1.3.x for a bit and you start getting
`Scope has changed from "User.Read" to "User.Read email profile openid".`, you
can silence this warning by setting an env variable for
`OAUTHLIB_RELAX_TOKEN_SCOPE` before starting Django.
