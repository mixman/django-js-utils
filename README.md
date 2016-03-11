Django JS Utils [![Build Status](https://travis-ci.org/mixman/django-js-utils.svg?branch=master)](https://travis-ci.org/mixman/django-js-utils)
===============

A fork of dutils, a library for using Django urlpatterns on the clientside.

Installation
------------

1. Add `django_js_utils` to INSTALLED_APPS

2. Set the file to hold the generated urls
```URLS_JS_GENERATED_FILE = 'static/js/dutils.conf.urls.js'```

3. Add inclusion/exclusions patterns
```
    URLS_INCLUDE_PREFIX = ['^api',]
    URLS_INCLUDE_PATTERN = ['index','status']
    URLS_EXCLUDE_PREFIX = ['^internal',]
    URLS_EXCLUDE_PATTERN = ['index',]
```

4. Add to your project:
```
    <script type="text/javascript" src="{{STATIC_URL}}dutils.js"></script>
    <script type="text/javascript" src="{{STATIC_URL}}dutils.conf.urls.js"></script>
```

Usage
-----

1. Create the `URLS_JS_GENERATED_FILE` (for production remember to run `collectstatic`):
```
    python manage.py js_urls
```

2. Clientside Django urlpatterns:
```
    url('time_edit', {'project_id': 1, time_id: 2}
    url('time_edit', [1, 2])
```

Credits
-------

Credit contributing to django-js-utils goes to:
* Marco Louro (author)
* Chris Reeves
* Dimitri Gnidash
* Luke Zapart
* Robby Dermody
* Antti Kaihola
* Simon Williams
* Jussi Vaihia
