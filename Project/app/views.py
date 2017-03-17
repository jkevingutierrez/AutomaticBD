from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic


class IndexView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        return 'hello'
