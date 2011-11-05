import os
import sys

from django.conf import settings as _settings


def get_server_context(**kwargs):

    settings = kwargs.pop('settings', _settings)

    context = {
        'name': getattr(settings, 'SERVER_APP_NAME',
            settings.ROOT_URLCONF.split('.')[0]),
        'domain': getattr(settings, 'SERVER_DOMAIN',
            'test.com'),
        'upstream': getattr(settings, 'SERVER_UPSTREAM',
            '%s:%d' % (
                 getattr(settings,
                    'SERVER_UPSTREAM_HOST', '127.0.0.1'),
                 getattr(settings,
                    'SERVER_UPSTREAM_PORT', (8000 if
                        ('gunicorn' in settings.INSTALLED_APPS) else 3031)),
            )),
        'ssl': getattr(settings, 'SERVER_USE_SSL', False),
        'ssl_rewrite': getattr(settings, 'SERVER_SSL_REWRITE', False),
        'static_root': settings.STATIC_ROOT.rstrip(' /'),
        'static_url': getattr(settings,
            'STATIC_URL', '/static/').rstrip(' /'),
        'media_root': settings.MEDIA_ROOT.rstrip(' /'),
        'media_url': settings.MEDIA_URL.rstrip(' /'),
        'using_virtual_env': hasattr(sys, 'real_prefix'),
        'python_executable': sys.executable,
        'using_celery': ('djcelery' in settings.INSTALLED_APPS),
        'disable_celerybeat': getattr(settings,
            'SERVER_DISABLE_CELERYBEAT', False),

    }

    context.update({
        'upstream_std_log_path': getattr(settings,
            'SERVER_ROOT_LOG',
            '/var/log/%s' % context['name']),
    })

    ex_head, ex_tail = os.path.split(sys.executable)

    #Detect uwsgi
    if os.path.isfile(os.path.join(ex_head, 'uwsgi')):
        context.update({
            'reverse': 'uwsgi',
            'uwsgi_path': os.path.join(ex_head, 'uwsgi')})

    #Detect gunicorn
    if 'gunicorn' in settings.INSTALLED_APPS:
        context.update({
            'reverse': 'gunicorn'})

    #get project root
    root = getattr(settings, 'APP_ROOT',
        getattr(settings, 'SITE_ROOT', None))
    if not root:
        root = os.getcwd()

    context.update({'home': root,
        'wsgi_script_alias': getattr(settings,
            'WSGI_SCRIPT_ALIAS',
            '%s/django.wsgi' % os.path.split(root)[0]),
    })

    if context['ssl']:
        crt = getattr(settings, 'SERVER_SSL_CRT_PATH', None)
        key = getattr(settings, 'SERVER_SSL_KEY_PATH', None)
        ca_path = getattr(settings, 'SERVER_SSL_CA_PATH', None)
        ca_file = getattr(settings, 'SERVER_SSL_CA_FILE', None)

        #bit iffy, relies on there being a ssl folder on the same
        #level as the django project.

        if not (crt and key):
            head, tail =  os.path.split(root)
            crt = '%s/ssl/%s.crt' % (head, context['name'])
            key = '%s/ssl/%s.key' % (head, context['name'])
            ca_path = '%s/ssl/CA' % (head)
            ca_file = '%s/ssl/CA/%s.crt' % (head, context['name'])

        context.update({
            'ssl_crt': crt,
            'ssl_key': key,
            'ssl_ca_path': ca_path,
            'ssl_ca_file': ca_file,
        })

    if context['using_virtual_env']:
        venv_path, venv_tail =  os.path.split(ex_head)
        context.update({'virtual_env': venv_path})

    if hasattr(settings, 'SERVER_SUPERVISOR_USER'):
        context.update({'supervisor_user': settings.SERVER_SUPERVISOR_USER})
        #defaults to www-data in the templates

    context.update(kwargs)

    return context
