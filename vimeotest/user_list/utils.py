import logging
import urllib2
from bs4 import BeautifulSoup

from django.db import IntegrityError

from models import User

# plug soupselect
# https://code.google.com/p/soupselect/
import soupselect; soupselect.monkeypatch(BeautifulSoup)

def get_page(page_num):
    users = []
    page = urllib2.urlopen('http://vimeo.com/channels/staffpicks/subscribers/page:{0}/sort:datesubscribe'.format(page_num)).read()
    soup = BeautifulSoup(page)
    # soup.prettify()

    for a in soup.findSelect("ol#browse_list li a"):
        url = 'http://vimeo.com{0}'.format(a['href'])
        profile_page = urllib2.urlopen(url).read()
        profile_soup = BeautifulSoup(profile_page)

        pro = profile_soup.findSelect("div#profile span.badge_pro")
        plus = profile_soup.findSelect("div#profile span.badge_plus")
        vidoes = 0
        try:
            vidoes = int(profile_soup.findSelect("div#cols ul.pivots li")[0]['data-count'])
        except:
            pass


        u = User(
            name=unicode(a['title']).encode('utf-8', 'replace'),
            url=url,
            is_paying_user=True if pro or plus else False,
            has_video_in_staff_pick=False,
            has_atleast_one_video=vidoes > 0
        )
        try:
            u.save()
            users.append(u)
        except:
            logging.exception("Unable to save user: ")
            pass

    return users