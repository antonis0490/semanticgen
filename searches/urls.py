from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from generator.models import generator;

# Create a list view using data from the table in the db and return it at the searches html
urlpatterns = [ url(r'^$', ListView.as_view(queryset=generator.objects.all().order_by("-date"), template_name="searches/searches.html"))]