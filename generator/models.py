from django.db import models

class sentiments(models.Model):
    id         = models.AutoField(primary_key=True)
    url        = models.CharField()
    sentiments = models.TextField()
    date       = models.DateTimeField()

    def __unicode__(self):
        return self.url
