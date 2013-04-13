import logging

from django.template import Context, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from models import User, UserFile
from forms import SearchForm

## http://stackoverflow.com/questions/2249792/json-serializing-django-models-with-simplejson
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.db.models import Model
from django.utils.functional import curry

class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet) or isinstance(obj, model):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self,obj)

# partial function, we can now use dumps(my_dict) instead
# of dumps(my_dict, cls=DjangoJSONEncoder)


def list_users(request):
    """ List all users View """

    t = loader.get_template('list_users.html')
    c = Context({
        'form' : SearchForm()
    })
    return HttpResponse(t.render(c))

@csrf_exempt
def search(request):
    r = {}

    form = SearchForm(data=request.GET)
    if form.is_valid():
        r['is_success'] = True
        users = User.objects.all()
        cd = form.cleaned_data
        if cd.get('name'):
            users = users.filter(name__icontains=cd.get('name'))
        if cd.get('flter') == u'1':
            users = users.filter(is_paying_user=True)
        elif cd.get('flter') == u'2':
            users = users.filter(has_atleast_one_video=True)
        elif cd.get('flter') == u'3':
            users = users.filter(has_video_in_staff_pick=True)

        r['total_count'] = users.count()
        r['users'] = loads(serialize('json', users[:100]))
    else:
        r['is_success'] = False
        r.update(form.errors)

    return HttpResponse(dumps(r), mimetype='application/json')


@csrf_exempt
def upload(request):
    """ Upload View """

    t = loader.get_template('upload.html')
    c = Context({
        'files': UserFile.objects.all()
    })
    if request.POST:
        uf = UserFile(user_file=request.FILES['userfile'], absolute_path=request.POST.get('absolute_path', ''),
            content_type=request.FILES['userfile'].content_type)
        uf.save()
        if not uf.id:
            raise Exception('Not saved!')
        return HttpResponse(dumps({'name': uf.user_file.name, 'url': uf.user_file.url}), mimetype='application/json')

    return HttpResponse(t.render(c))


