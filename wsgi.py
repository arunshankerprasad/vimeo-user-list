import os
import sys

# First set the path for external libs
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'),)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'vimeotest')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'vimeotest.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
