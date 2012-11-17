import sys
import re

import types
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.core.management.base import BaseCommand
from django.utils import simplejson
from django.utils.datastructures import SortedDict
from django.conf import settings as project_settings
from django_js_utils import settings as app_settings

RE_KWARG = re.compile(r"(\(\?P\<(.*?)\>.*?\)\)?)") #Pattern for recongnizing named parameters in urls
RE_ARG = re.compile(r"(\(.*?\))") #Pattern for recognizing unnamed url parameters

URLS_JS_GENERATED_FILE = getattr(project_settings, 'URLS_JS_GENERATED_FILE', app_settings.URLS_JS_GENERATED_FILE)
URLS_JS_TO_EXPOSE = getattr(project_settings, 'URLS_JS_TO_EXPOSE', app_settings.URLS_JS_TO_EXPOSE)

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Create urls.js file by parsing all of the urlpatterns in the root urls.py file
        """
        js_patterns = SortedDict()
        print "Generating Javascript urls file %s" % URLS_JS_GENERATED_FILE
        Command.handle_url_module(js_patterns, project_settings.ROOT_URLCONF)
        #output to the file
        urls_file = open(URLS_JS_GENERATED_FILE, "w")
        urls_file.write(";dutils.conf.urls = ")
        simplejson.dump(js_patterns, urls_file)
        urls_file.write(";")
        print "Done generating Javascript urls file %s" % URLS_JS_GENERATED_FILE
        
    @staticmethod
    def handle_url_module(js_patterns, module_name, prefix=""):
        """
        Load the module and output all of the patterns
        Recurse on the included modules
        """
        if isinstance(module_name, basestring):
            __import__(module_name)
            root_urls = sys.modules[module_name]
            patterns = root_urls.urlpatterns
        elif isinstance(module_name, types.ModuleType):
            root_urls = module_name
            patterns = root_urls.urlpatterns
        else:
            root_urls = module_name
            patterns = root_urls

        for pattern in patterns:
            if issubclass(pattern.__class__, RegexURLPattern):
                if pattern.name and pattern.name in URLS_JS_TO_EXPOSE:
                    full_url = prefix + pattern.regex.pattern
                    for chr in ["^","$"]:
                        full_url = full_url.replace(chr, "")
                    #handle kwargs, args
                    kwarg_matches = RE_KWARG.findall(full_url)
                    if kwarg_matches:
                        for el in kwarg_matches:
                            #prepare the output for JS resolver
                            full_url = full_url.replace(el[0], "<%s>" % el[1])
                    #after processing all kwargs try args
                    args_matches = RE_ARG.findall(full_url)
                    if args_matches:
                        for el in args_matches:
                            full_url = full_url.replace(el, "<>")#replace by a empty parameter name
                    #unescape escaped chars which are not special sequences
                    full_url = re.sub(r'\\([^\dAZbBdDsSwW])', r'\1', full_url)
                    js_patterns[pattern.name] = "/" + full_url
            elif issubclass(pattern.__class__, RegexURLResolver):
                if pattern.url_patterns:
                    if (isinstance(pattern.urlconf_name, types.ModuleType)
                        and pattern.urlconf_name.__name__ not in URLS_JS_TO_EXPOSE):
                        continue
                    Command.handle_url_module(js_patterns, pattern.url_patterns, prefix=pattern.regex.pattern)
                elif pattern.urlconf_name:
                    if pattern.urlconf_name in URLS_JS_TO_EXPOSE:
                        Command.handle_url_module(js_patterns, pattern.urlconf_name, prefix=pattern.regex.pattern)
