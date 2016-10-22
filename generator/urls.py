from django.conf.urls import url
from generator.views import generatorFun
urlpatterns = [
    url(r'^$',generatorFun.as_view()),
]