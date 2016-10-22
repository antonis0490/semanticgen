from django.db import models
import random

def code_generator(size=6, chars="abcdefghiklmnopqrstuvwuxz"):
    return ''.join(random.choice(chars) for i in range(size))


class generator(models.Model):

    url = models.TextField(max_length=240)
    sentiments = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return str(self.url)

    def save(self, *args, **kwargs):
        sentiments = code_generator()
        super(generator, self).save(*args, **kwargs)