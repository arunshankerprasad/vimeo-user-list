import wsgi

from django.core.management.base import NoArgsCommand

from vimeotest.user_list.utils import get_page
from vimeotest.user_list.models import User

class Command(NoArgsCommand):
    help = "Fetch users from Vimeo"

    def handle_noargs(self, **options):
        pn = 205
        total_count = User.objects.all().count()
        while total_count <= 5010:
            pn += 1
            print "Getting page: {0}".format(pn)
            u = get_page(pn)

            total_count = User.objects.all().count()

            print "Current Count: {0}".format(total_count)

