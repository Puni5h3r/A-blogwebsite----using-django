from typing import List

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from django.utils import timezone

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)



    #creating this will conventionally return the title in string
    def __str__(self):
        return self.title
# overrride default model save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

        # creating a Meta class which will upbring the data from Database in descending order
        # therefore, we can the last blog earlier
    class Meta:
        ordering = ['-created_on']

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80,blank=False)
    email = models.EmailField(blank=False)
    body = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
