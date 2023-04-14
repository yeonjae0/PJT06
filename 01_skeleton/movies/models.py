from django.db import models
from django.conf import settings

class Movie(models.Model):
    # objects = models.Manager()
    title = models.CharField(max_length=20)
    description = models.TextField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    def __str__(self):
        return f'{self.id}번째글 - {self.title}'


class Comment(models.Model):
    # objects = models.Manager()
    content = models.CharField(max_length=100)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
