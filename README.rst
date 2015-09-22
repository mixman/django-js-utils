==========================
dutils - Django JS Utils
==========================

dutils is a small utility library that aims to provide JavaScript/Django developers with
a few utilities that will help the development of RIA on top of a
Django Backend.

Reversing Django Urls from Javascript
-------------------------------------
Why is this useful
******************
One of the pillars of Django is DRY principle and hardcoding your urls in Javascript is violating that principle.

Moreover, building parametrized urls on the fly is error-prone and ugly.

What is included
****************
A snippet of Javascript implementation of Django reverse function that can be found in dutils.js

A management command js_urls to generate a list of all of your Django urls

Installation
************
1. Add django_js_utils application to your INSTALLED_APPS
Example::
    INSTALLED_APPS += ('django_js_utils')

2. Set the path and file name to generate urls to inside your django settings file.
Example::
    URLS_JS_GENERATED_FILE='static/js/dutils.conf.urls.js'

3. Set the url namespaces or names to resolve - only names specified in this list will be resolved to the file
Example::
    URLS_INCLUDE_PREFIX = ['^api',]
    URLS_INCLUDE_PATTERN = ['index','status']
    URLS_EXCLUDE_PREFIX = ['^internal',]
    URLS_EXCLUDE_PATTERN = ['index',]

4. Add entries into your base.html template (or where ever you need) to include the dutils.js file, along with the dutils.conf.urls.js patterns file. If you're using Django's staticfiles app, you'll use something
like::
    <script type="text/javascript" src="{{STATIC_URL}}dutils.js"></script>
    <script type="text/javascript" src="{{STATIC_URL}}dutils.conf.urls.js"></script>


Usage
*****
1. Generate a list of all available urls in the special
format::
    >>> python manage.py js_urls

To keep the list of urls up-to-date, it is recommended to include this command as part of the build process.

2. If you're using Django's staticfiles app, issue the collectstatic command to include dutils.js and the urls list you generated in step 1 in your static
directory::
    >>> python manage.py collectstatic

3. On the web page, reverse url as
such::
    >>> url('time_edit', {'project_id': 1, time_id: 2}
    >>> url('time_edit', [1, 2])

