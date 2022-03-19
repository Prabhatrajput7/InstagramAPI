from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=20)
    url = models.URLField()
    post = models.ForeignKey(User, on_delete=models.CASCADE)#user udemty[2], insta[1] 
    con = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-con']

    def __str__(self):
        return f'Title --> {self.title}'

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE) 

    def __str__(self):
        return f'Voter --> {self.voter} ** Post --> {self.post}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE) 
    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Post --> {self.post} ## Comment --> {self.comment}'        