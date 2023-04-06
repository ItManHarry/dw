# Using the Django authentication system
## User Objects
> User objects are the core of the authentication system. They typically represent the people interacting with your site and are used to enable things like restricting access, registering user profiles, associating content with creators etc. Only one class of user exists in Django’s authentication framework, i.e., 'superusers' or admin 'staff' users are just user objects with special attributes set, not different classes of user objects.
> The primary attributes of the default user are:
- username
- password
- email
- first_name
- last_name
## Create users
> The most direct way to create users is to use the included create_user() helper function:
```bazaar
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
>>> user.last_name = 'Lennon'
>>> user.save()
```
## Creating superusers
> Create superusers using the createsuperuser command:
```bazaar
$ python manage.py createsuperuser --username=joe --email=joe@example.com
```
> You will be prompted for a password. After you enter one, the user will be created immediately. If you leave off the --username or --email options, it will prompt you for those values.
## Changing passwords
> To change a user’s password, you have several options:
1. manage.py changepassword *username* offers a method of changing a user’s password from the command line.
2. using set_password()
```bazaar
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='john')
>>> u.set_password('new password')
>>> u.save()
```
## Authenticating users
> Use authenticate() to verify a set of credentials. It takes credentials as keyword arguments, username and password for the default case, checks them against each authentication backend, and returns a User object if the credentials are valid for a backend. If the credentials aren’t valid for any backend or if a backend raises PermissionDenied, it returns None.
```bazaar
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # A backend authenticated the credentials
else:
    # No backend authenticated the credentials
```
## Authentication in web requests
> Django uses sessions and middleware to hook the authentication system into request objects.
> These provide a request.user attribute on every request which represents the current user. If the current user has not logged in, this attribute will be set to an instance of AnonymousUser, otherwise it will be an instance of User.
> You can tell them apart with is_authenticated, like so:
```bazaar
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```
## How to log a user in
> If you have an authenticated user you want to attach to the current session - this is done with a login() function.
**login(request, user, backend=None)**
> To log a user in, from a view, use login(). It takes an HttpRequest object and a User object. login() saves the user’s ID in the session, using Django’s session framework.
> Note that any data set during the anonymous session is retained in the session after a user logs in.
> This example shows how you might use both authenticate() and login():
```bazaar
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```
## How to log a user out
**logout(request)**
> To log out a user who has been logged in via django.contrib.auth.login(), use django.contrib.auth.logout() within your view. It takes an HttpRequest object and has no return value. Example:
```bazaar
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    # Redirect to a success page.
```
## Limiting access to logged-in users
> The raw way to limit access to pages is to check request.user.is_authenticated and either redirect to a login page:
```bazaar
from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
```
> The login_required decorator
```bazaar
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    ...
```
## The LoginRequiredMixin mixin
> When using class-based views, you can achieve the same behavior as with login_required by using the LoginRequiredMixin. This mixin should be at the leftmost position in the inheritance list.
```bazaar
from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
```
## The permission_required decorator
> It’s a relatively common task to check whether a user has a particular permission. For that reason, Django provides a shortcut for that case: the permission_required() decorator.:
```bazaar
from django.contrib.auth.decorators import permission_required

@permission_required('polls.add_choice')
def my_view(request):
    ...
```
> Just like the has_perm() method, permission names take the form "<app label>.<permission codename>" (i.e. polls.add_choice for a permission on a model in the polls application).
## The PermissionRequiredMixin mixin
> To apply permission checks to class-based views, you can use the PermissionRequiredMixin:
```bazaar
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = 'polls.add_choice'
    # Or multiple of permissions:
    permission_required = ('polls.view_choice', 'polls.change_choice')
```
## Password management in Django
### Password validation
> By default, validators are used in the forms to reset or change passwords and in the createsuperuser and changepassword management commands. Validators aren’t applied at the model level, for example in User.objects.create_user() and create_superuser(), because we assume that developers, not users, interact with Django at that level and also because model validation doesn’t automatically run as part of creating models.
- Enabling password validation
> Password validation is configured in the AUTH_PASSWORD_VALIDATORS setting:
```
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```
> This example enables all four included validators:
1. **UserAttributeSimilarityValidator**, which checks the similarity between the password and a set of attributes of the user.
2. **MinimumLengthValidator**, which checks whether the password meets a minimum length. This validator is configured with a custom option: it now requires the minimum length to be nine characters, instead of the default eight.
3. **CommonPasswordValidator**, which checks whether the password occurs in a list of common passwords. By default, it compares to an included list of 20,000 common passwords.
4. **NumericPasswordValidator**, which checks whether the password isn’t entirely numeric.

