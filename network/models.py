from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404


class User(AbstractUser):
    pass


class Post(models.Model):
    header = models.CharField(max_length=512)
    text = models.TextField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="author")


    @property
    def likes_count(self):
        return Like.objects.filter(post=self).count()

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "creation_date": self.creation_date.strftime("%b %-d %Y, %-I:%M %p"),
            "edit_date": self.edit_date.strftime("%b %-d %Y, %-I:%M %p"),
            "header": self.header,
            "text": self.text,
            "likes": self.likes_count
        }


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)


class Follower(models.Model):
    followers = models.ManyToManyField(User, related_name='followers')
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)

    @classmethod
    def follow(cls, owner, followed):
        follower_class, created = cls.objects.get_or_create(
            owner=owner,
        )
        follower_class.followers.add(followed)

    @classmethod
    def unfollow(cls, owner, followed):
        follower_class = get_object_or_404(
            klass=cls,
            owner=owner,
        )
        follower_class.followers.remove(followed)