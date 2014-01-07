import sys
import re
import types

from django.conf import settings
from django.utils.datastructures import SortedDict
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

from django_js_utils import conf_jsutils

class PatternsParser(object):
    def __init__(self):
        self._patterns = SortedDict()

    def parse(self, input):
        self.handle_url_module(input)

    def handle_url_module(self, module_name, prefix=""):
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
                val = getattr(pattern, 'name', None) or ''
                if getattr(settings, 'URLS_DEBUG', False):
                    print "VAL", val
                    print " PREFIX",prefix
                    print " PATTERN", pattern.regex.pattern
                if any(k in val for k in conf_jsutils.URLS_JS_TO_EXPOSE) or any(k in prefix for k in conf_jsutils.URLS_JS_TO_EXPOSE):
                    if any(k in pattern.regex.pattern for k in settings.URLS_EXCLUDE_PATTERN):
                        if getattr(settings, 'URLS_DEBUG', False):
                            print " ! EXCLUDED"
                        continue
                    self.parse_pattern(pattern, prefix)

            elif issubclass(pattern.__class__, RegexURLResolver):
                if pattern.url_patterns:
                    self.handle_url_module(pattern.url_patterns, prefix=prefix+pattern.regex.pattern)
                elif pattern.urlconf_name:
                    self.handle_url_module(pattern.urlconf_name, prefix=pattern.regex.pattern)

    def parse_pattern(self, pattern, prefix):
        full_url = prefix + pattern.regex.pattern
        for chr in ("^", "$"):
            full_url = full_url.replace(chr, "")

        #handle kwargs, args
        kwarg_matches = conf_jsutils.RE_KWARG.findall(full_url)
        if kwarg_matches:
            for el in kwarg_matches:
                #prepare the output for JS resolver
                full_url = full_url.replace(el[0], "<%s>" % el[1])

        #after processing all kwargs try args
        args_matches = conf_jsutils.RE_ARG.findall(full_url)
        if args_matches:
            for el in args_matches:
                full_url = full_url.replace(el, "<>")  # replace by a empty parameter name

        #unescape escaped chars which are not special sequences
        full_url = re.sub(r'\\([^\dAZbBdDsSwW])', r'\1', full_url)
        self._patterns[pattern.name] = "/" + full_url

    @property
    def patterns(self):
        return self._patterns
