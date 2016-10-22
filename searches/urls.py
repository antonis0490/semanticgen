from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from searches.models import searches_sentiments

urlpatterns = [ url(r'^$', ListView.as_view(queryset=searches_sentiments.objects.all(), template_name="searches/searches.html"))]