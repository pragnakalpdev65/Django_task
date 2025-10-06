from django.db import models
import datetime


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
   # post_date=models.DateTimeField("post date")
    post_date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

   
    