from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .form import submitURL
import json
from watson_developer_cloud import AlchemyLanguageV1
import unicodedata

def cleanText(data):
    # u = unicode(data, "utf-8"
    out = ''.join((c for c in unicodedata.normalize('NFD', data) if unicodedata.category(c) != 'Mn'))
    try:
        return str(out)
    except UnicodeEncodeError:
    	return "InvalidCharsName"

    return out

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
        sentimentList = []
        form = submitURL(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            print(form.cleaned_data.get("url"))
        else:
            url = "err1"

        key = "1d9f818df02f61fb5137c4105a19c49bc066efc8"

        if url != "err1":
            alchemy_language = AlchemyLanguageV1(api_key=str(key))
            ans =(json.dumps(
                alchemy_language.combined(
                    url=str(url),
                    extract='entities,keywords',
                    sentiment=1,

                    ),
                indent=2))
            # ans = eval(ans)
            ans = json.loads(str(ans))

            status = str(ans['status'])

            if status == "OK":
                entities = ans["entities"]
                keywords = ans["keywords"]
                for entity in entities:
                    if float(entity["relevance"]) > 0.3:
                        sentimentList.append("#"+cleanText(entity["text"]))
                for keyword in keywords:
                    if float(keyword["relevance"]) > 0.3:
                        if str(keyword["text"] not in sentimentList):
                            sentimentList.append("#"+cleanText(keyword["text"]))
                print sentimentList
        else:
            sentimentList = []

        context = {"title": "Submit URL",
                   "form": form,
                   "sentimentList": sentimentList}
        return render(request, 'generator/generator.html',context)

#example:
    # https:// gateway - a.watsonplatform.net / calls / url / URLGetCombinedData?url = http: // www.cnbc.com / 2016 / 05 / 16 / buffetts - berkshire - hathaway - takes - new - stake - in -apple.html & outputMode = json & extract = keywords, entities, concepts & sentiment = 1 & maxRetrieve = 3 & apikey = 1
    # d9f818df02f61fb5137c4105a19c49bc066efc8