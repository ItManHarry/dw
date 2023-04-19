# Settings
## Using settings in Python code
> In your Django apps, use settings by importing the object django.conf.settings. Example:
```bazaar
from django.conf import settings
if settings.DEBUG:
    # Do something
```
> Note that django.conf.settings isn’t a module – it’s an object. So importing individual settings is not possible:
```bazaar
from django.conf.settings import DEBUG  # This won't work.
```
## Altering settings at runtime
> You shouldn’t alter settings in your applications at runtime. For example, don’t do this in a view:
```bazaar
from django.conf import settings
settings.DEBUG = True   # Don't do this!
```
> The only place you should assign to settings is in a settings file.
## Security
> Because a settings file contains sensitive information, such as the database password, you should make every attempt to limit access to it. For example, change its file permissions so that only you and your web server’s user can read it. This is especially important in a shared-hosting environment.
## Creating your own settings
> There’s nothing stopping you from creating your own settings, for your own Django apps, but follow these guidelines:
- Setting names must be all uppercase.
- Don’t reinvent an already-existing setting.