from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

import urllib2
from bs4 import BeautifulSoup

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

    if request.POST:

        page = urllib2.urlopen('http://vimeo.com/channels/staffpicks/subscribers').read()
        soup = BeautifulSoup(page)
        soup.prettify()

        for a in soup.findSelect("ol#browse_list li a"):
            users.append(a['title'])

    t = loader.get_template('get_users.html')
    c = Context({
        'current_time': datetime.now(),
        'users':        users
    })

    return HttpResponse(t.render(c))

