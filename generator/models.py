from django.db import models

# Main table to save searches and hashes generated
class generator(models.Model):

    url = models.TextField(max_length=240)
    sentiments = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

