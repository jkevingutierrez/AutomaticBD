import json
from django.views.generic import ListView
from django.views.generic.base import View
from django.http import JsonResponse


class IndexView(ListView):
    template_name = "index.html"
    queryset = 'AutomaticBD'
    context_object_name = 'projectName'


class ServiceView(View):

    @staticmethod
    def get(request):
        to_json = {
            "key1": "value1",
            "key2": "value2"
        }
        return JsonResponse(to_json)

    @staticmethod
    def post(request, *args, **kwargs):
        print('Raw Data: "%s"' % request.META)
        print('Raw Data: "%s"' % type(request.body))
        to_json = json.loads(request.body)
        return JsonResponse(to_json)
