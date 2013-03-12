import wsgi

from optparse import make_option
import time

from django.core.management.base import NoArgsCommand, BaseCommand

from vimeotest.user_list.utils import get_page
from vimeotest.user_list.models import User

class Command(NoArgsCommand):
    help = "Fetch users from Vimeo"
    option_list = BaseCommand.option_list + (
        make_option('--start',
            action='store',
            dest='start',
            default=1,
            type="int",
            help='Optionally override the start page option'),
        )

    def handle_noargs(self, **options):
        pn = options.get('start', 1)
        total_count = User.objects.all().count()
        while total_count <= 5010:
            print "Getting page: {0}".format(pn)

            try:
                u = get_page(pn)
            except:
                time.sleep(120)
                u = get_page(pn)

            total_count = User.objects.all().count()

            print "Current Count: {0}".format(total_count)
            pn += 1
