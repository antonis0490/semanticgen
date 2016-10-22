from django.db import models


class searches_sentiments(models.Model):
    # id         = models.AutoField(primary_key=True)
    url        = models.TextField()
    sentiments = models.TextField()
    date       = models.DateTimeField()

    def __str__(self):
        return self.url
