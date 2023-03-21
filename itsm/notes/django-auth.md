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
