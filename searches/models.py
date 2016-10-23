from django.db import models


class searches_sentiments(models.Model):
    url        = models.TextField()
    sentiments = models.TextField()
    date       = models.DateTimeField()


    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)