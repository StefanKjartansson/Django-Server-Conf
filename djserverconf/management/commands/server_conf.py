from textwrap import dedent
from optparse import make_option

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from djserverconf.conf.context import get_server_context


class Command(BaseCommand):

    args = "[<command> [<process>, ...]]"

    help = dedent("""

        Generates server configuration files.

           """).strip()

    option_list = BaseCommand.option_list + (
        make_option('--supervisor',
                action='store_true',
                dest='supervisor',
                default=False,
                help='Generate supervisor configuration file'),
        make_option('--nginx',
                action='store_true',
                dest='nginx',
                default=False,
                help='Generate nginx configuration file'),
        make_option('--apache',
                action='store_true',
                dest='apache',
                default=False,
                help='Generate apache configuration file'),
    )


    def handle_supervisor(self, context, f=None):

        stream = f or self.stdout

        if context['reverse'] == 'uwsgi':
            stream.write('#Auto generated uwsgi supervisor configuration:\n')
            stream.write(render_to_string('djserverconf/uwsgi_supervisor.conf',
                context) + '\n')

        elif context['reverse'] == 'gunicorn':
            stream.write('#Auto generated gunicorn supervisor configuration:\n')
            stream.write(render_to_string('djserverconf/gunicorn_supervisor.conf',
                context) + '\n')

        if context['using_celery']:
            stream.write('#Auto generated celery supervisor configuration:\n')
            stream.write(render_to_string('djserverconf/celery_supervisor.conf',
                context) + '\n')

            if not context.get('disable_celerybeat', False):
                stream.write('#Auto generated celery_beat supervisor configuration:\n')
                stream.write(render_to_string('djserverconf/celerybeat_supervisor.conf',
                    context) + '\n')


    def handle(self, *args, **options):

        context = get_server_context()
        if not any(map(options.get, ['nginx', 'apache', 'supervisor'])):

            import pprint
            pp = pprint.PrettyPrinter(indent=4, stream=self.stdout)
            self.stdout.write('Auto-detected server context:\n')
            pp.pprint(context)

            self.stdout.write(('-' * 80) + '\n')
            self.stdout.write('Auto generated nginx configuration example:\n')
            self.stdout.write(render_to_string('djserverconf/nginx.conf',
                context) + '\n')
            self.stdout.write(('-' * 80) + '\n')

            self.stdout.write('Auto generated apache configuration example:\n')
            self.stdout.write(render_to_string('djserverconf/apache.conf',
                context) + '\n')
            self.stdout.write(('-' * 80) + '\n')

            self.handle_supervisor(context)

        if options['nginx']:
            with open('%s-nginx.conf' % context['name'], 'w') as f:
                f.write(render_to_string('djserverconf/nginx.conf',
                    context))

        if options['supervisor']:
            with open('%s-supervisor.conf' % context['name'], 'w') as f:
                self.handle_supervisor(context, f)

        if options['apache']:
            with open('%s-apache' % context['name'], 'w') as f:
                f.write(render_to_string('djserverconf/apache.conf',
                    context))
