from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .form import submitURL
class generatorFun(View):
    def get(self, request, *args, **kwargs):
        theform = submitURL()
        context = {"title": "Submit URL",
                   "form": theform}
        return render(request, 'generator/generator.html', context)


    def post(self, request, *args, **kwargs):
        # print(request.POST)
        # x = request.POST.get("url", "")
        # print x
        form = submitURL(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get("url"))

        key = "d9f818df02f61fb5137c4105a19c49bc066efc8"
        context = {"title": "Submit URL",
                   "form": form}
        return render(request, 'generator/generator.html',context)

#example:
    #https: // gateway - a.watsonplatform.net / calls / url / URLGetCombinedData?url = http: // www.cnbc.com / 2016 / 05 / 16 / buffetts - berkshire - hathaway - takes - new - stake - in -apple.html & outputMode = json & extract = keywords, entities, concepts & sentiment = 1 & maxRetrieve = 3 & apikey = 1
    d9f818df02f61fb5137c4105a19c49bc066efc8