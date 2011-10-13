from textwrap import dedent
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from djserverconf.conf.nginx import generate_nginx


class Command(BaseCommand):

    args = "[<command> [<process>, ...]]"

    help = dedent("""
        Generates a nginx config file.

        TODO: docs
           """).strip()

    option_list = BaseCommand.option_list + (
        #make_option("--daemonize","-d",
        #    action="store_true",
        #    dest="daemonize",
        #    default=False,
        #    help="daemonize before launching subprocessess"
        #),
    )

    def handle(self, *args, **options):
        print generate_nginx()
