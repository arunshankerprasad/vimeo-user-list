import logging
import urllib2
from bs4 import BeautifulSoup
import simplejson

from django.db import IntegrityError

from models import User

# plug soupselect
# https://code.google.com/p/soupselect/
import soupselect; soupselect.monkeypatch(BeautifulSoup)

def get_page(page_num):
    chrome_user_agent = "User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/27.0.1430.0 Safari/537.33"
    users = []
    request = urllib2.Request('http://vimeo.com/channels/staffpicks/subscribers/page:{0}/sort:datesubscribe'.format(page_num))
    request.add_header('User-Agent', chrome_user_agent)
    opener = urllib2.build_opener()
    page = opener.open(request).read()
    soup = BeautifulSoup(page)
    # soup.prettify()

    for a in soup.findSelect("ol.js-browse_list li a"):
        name = a['href']
        has_video_in_staff_pick = False
        url = 'http://vimeo.com{0}'.format(name)
        request = urllib2.Request(url)
        request.add_header('User-Agent', chrome_user_agent)
        opener = urllib2.build_opener()
        profile_page = opener.open(request).read()
        profile_soup = BeautifulSoup(profile_page)

        videos_api_url = "http://vimeo.com/api/v2/{0}/videos.json".format(name.replace('/', ''))
        videos = simplejson.loads(urllib2.urlopen(videos_api_url).read())
        for video in videos:
            request = urllib2.Request(video.get('url'))
            request.add_header('User-Agent', chrome_user_agent)
            opener = urllib2.build_opener()
            video_page = opener.open(request).read()
            video_soup = BeautifulSoup(video_page)
            for script in video_soup.findSelect("script"):
                if script.prettify().find('{"badge":{"name":"staffpicks"') > 0:
                    has_video_in_staff_pick = True
                    break

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
            has_video_in_staff_pick=has_video_in_staff_pick,
            has_atleast_one_video=vidoes > 0
        )


        try:
            logging.info(u"Going to try and save: {0}".format(u))
        except:
            logging.exception("Unable to log user info: ")
            pass

        try:
            u.save()
            users.append(u)
        except:
            logging.exception("Unable to save user: ")
            pass

    return users