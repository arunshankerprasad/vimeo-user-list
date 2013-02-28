
from datetime import datetime
import urllib2
from bs4 import BeautifulSoup

from django.template import Context, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# plug soupselect
# https://code.google.com/p/soupselect/
import soupselect; soupselect.monkeypatch(BeautifulSoup)

def list_users(request):
    """ List all users View """

    t = loader.get_template('list_users.html')
    c = Context({
        'current_time': datetime.now(),
    })
    return HttpResponse(t.render(c))

@csrf_exempt
def get_users(request):
    """ List all users View """

    users = []
    page = 0

    if request.POST:
        page = urllib2.urlopen('http://vimeo.com/channels/staffpicks/subscribers').read()
        soup = BeautifulSoup(page)
        soup.prettify()

        for a in soup.findSelect("ol#browse_list li a"):
            u = User(
                name=a['title'],
                url='',
                is_paying_user=False,
                has_video_in_staff_pick=False,
                has_atleast_one_video=False
            )
            u.put()
            users.append(u)

    t = loader.get_template('get_users.html')
    c = Context({
        'current_time': datetime.now(),
        'users':        users,
        'page':         page
    })

    return HttpResponse(t.render(c))

