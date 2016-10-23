from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from searches.models import searches_sentiments
from generator.models import generator;

urlpatterns = [ url(r'^$', ListView.as_view(queryset=generator.objects.all(), template_name="searches/searches.html"))]