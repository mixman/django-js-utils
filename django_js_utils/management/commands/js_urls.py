import subprocess, os
import simplejson as json

from django.core.management.base import BaseCommand
from django.conf import settings as project_settings

from django_js_utils import conf_jsutils
from django_js_utils.utils import PatternsParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Create urls.js file by parsing all of the urlpatterns in the root urls.py file
        """

        print "Generating Javascript urls file %s" % conf_jsutils.URLS_JS_GENERATED_FILE

        parser = PatternsParser()
        parser.parse(project_settings.ROOT_URLCONF)

        subprocess.call('mkdir {}'.format(os.path.dirname(conf_jsutils.URLS_JS_GENERATED_FILE)).split())
        with open(conf_jsutils.URLS_JS_GENERATED_FILE, "w+") as f:
            f.write(";dutils.conf.urls = ")
            json.dump(parser.patterns, f)
            f.write(";")

        print "Done generating Javascript urls file %s" % conf_jsutils.URLS_JS_GENERATED_FILE
