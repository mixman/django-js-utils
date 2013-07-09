import re

from os.path import join, dirname
from django.conf import settings

default_path = join(dirname(__file__), 'static/js/dutils.conf.urls.js')
URLS_JS_GENERATED_FILE = getattr(settings, 'URLS_JS_GENERATED_FILE', default_path)
URLS_JS_TO_EXPOSE = getattr(settings, 'URLS_JS_TO_EXPOSE', [])

#Pattern for recongnizing named parameters in urls
RE_KWARG = re.compile(r"(\(\?P\<(.*?)\>.*?\)\)?)")
#Pattern for recognizing unnamed url parameters
RE_ARG = re.compile(r"(\(.*?\))")
