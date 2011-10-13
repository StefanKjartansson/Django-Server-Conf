import os
import sys

from django.conf import settings
from django.template.loader import render_to_string


class Project(object):

    def __init__(self, name, domain,
            static_root, reverse='http',
            ssl=False, upstreams=None):

        self.name = name
        self.domain = domain
        self.static_root = static_root
        self.reverse = reverse
        self.ssl = ssl
        self.upstreams = upstreams or ['127.0.0.1:3031']


def generate_nginx():

    using_virtualenv = hasattr(sys, 'real_prefix')

    kw = {}

    if os.path.isfile('/%s' % os.path.join(
        *(sys.executable.split('/')[:-1] + ['uwsgi']))):
        kw.update({'reverse': 'uwsgi'})

    if hasattr(settings, 'SERVER_UPSTREAMS'):
        kw.update({'upstreams': settings.SERVER_UPSTREAMS})

    p = Project(settings.SERVER_NAME,
        settings.SERVER_DOMAIN,
        settings.STATIC_ROOT, **kw)

    print render_to_string('djserverconf/nginx.conf',
        {'project': p})
