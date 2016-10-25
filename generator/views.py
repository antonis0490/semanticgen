from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .form import submitURL
import json
from watson_developer_cloud import AlchemyLanguageV1
import re
import urllib
from bs4 import BeautifulSoup
from django.contrib.staticfiles.templatetags.staticfiles import static

import unicodedata
import datetime
import os, urllib, sys
import re
# import enchant
from .models import generator


def cleanText(data):
    # u = unicode(data, "utf-8"
    out = ''.join((c for c in unicodedata.normalize('NFD', data) if unicodedata.category(c) != 'Mn'))
    try:
        out = out.replace("\n", " ")
        return str(out)
    except UnicodeEncodeError:
    	return "InvalidCharsName"

    return out

def addToDB(url,sentiment):
    now = datetime.datetime.now()
    generator.objects.create(url=url, sentiments=str(sentiment),date=now)

def APIgen(url):
    key = "1d9f818df02f61fb5137c4105a19c49bc066efc8"
    sentimentList = []
    alchemy_language = AlchemyLanguageV1(api_key=str(key))
    ans = (json.dumps(
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
                sentimentList.append("#" + cleanText(entity["text"]))
        for keyword in keywords:
            if float(keyword["relevance"]) > 0.3:
                if str(keyword["text"] not in sentimentList):
                    sentimentList.append("#" + cleanText(keyword["text"]))
        return sentimentList

# def Customgen(url):
#
#     cmd = os.popen("elinks -dump %s" % url)
#     output = cmd.read()
#     cmd.close()
#
#     output = output.split("\n")
#
#     temp =  []  # save temporary data
#     temp3 = []  # save temporary data
#     temp4 = []  # save temporary data
#     temp6 = []  # save temporary data
#     for line in output:
#         line = line.strip()  # remove spaces from start and end of line
#
#         exploded = line.split()  # remove spaces from inbetween the line
#
#         if len(exploded) > 1:  # if space detected save each element in temp array
#             for e in exploded:
#                 temp.append(e)
#         else:
#             temp.append(exploded)
#     temp2 = temp
#
#     for word in temp2:
#         stopwords = ["a", "more", "less", "from", "all", "under", "all", "to", "an", "and", "the", "at", "or", "is",
#                      "has", "in", "the", "isnt", "he", "she", "it", "they", "we", "by", "on", "out", "before", "after",
#                      "later"]
#         regex = re.compile('[^a-zA-Z]')
#         word = regex.sub('', str(word))
#         if word.lower() not in stopwords:
#             if len(word) > 1:  # if word has more than 1 letter
#                 temp3.append(word)
#
#     for word in temp3:
#         if not word.startswith("http"):  # remove links
#             temp4.append(word)
#
#     #remove duplications
#     temp5 = list(set(temp4))
#
#     #remove non english words
#     # for word in temp5:
#     #
#     #     with open(dictionary) as dictionary:
#     #         english_vocab = set(word.strip().lower() for word in dictionary)
#     #
#     #     if word.lower() in english_vocab:
#     #         temp6.append(word)
#     return temp5

def Customgen(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html)
    data = soup.findAll(text=True)

    output = []

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            element = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore')
            return False

        return True

    result = filter(visible, data)

    for r in result:
        element = unicodedata.normalize('NFKD', r).encode('ascii', 'ignore')
        if element not in (" ", ""):
            output.append(element)

    return output

class generatorFun(View):
    def get(self, request, *args, **kwargs):
        theform = submitURL()
        context = {"title": "Submit URL",
                   "form": theform}
        return render(request, 'generator/generator.html', context)


    def post(self, request, *args, **kwargs):

        form = submitURL(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            apiselector = form.cleaned_data.get("apiselector")
            print(form.cleaned_data.get("apiselector"))
        else:
            url = "err1"

        if url != "err1":
            #If selection is from API
            if apiselector == "API":
                sentimentList = APIgen(url)
            elif apiselector == "Custom":
                sentimentList = Customgen(url)
        else:
            sentimentList = []

        addToDB(url,str(sentimentList))
        context = {"title": "Submit URL",
                   "form": form,
                   "sentimentList": sentimentList}
        return render(request, 'generator/generator.html',context)

#example:
    # https:// gateway - a.watsonplatform.net / calls / url / URLGetCombinedData?url = http: // www.cnbc.com / 2016 / 05 / 16 / buffetts - berkshire - hathaway - takes - new - stake - in -apple.html & outputMode = json & extract = keywords, entities, concepts & sentiment = 1 & maxRetrieve = 3 & apikey = 1
    # d9f818df02f61fb5137c4105a19c49bc066efc8