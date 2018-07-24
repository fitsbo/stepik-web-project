from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(default="")
    added_at = models.DateTimeField(
        blank=True, auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name='qa_user_likes')
    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/question/{}/'.format(self.id)


class Answer(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(default="")
    added_at = models.DateTimeField(
        blank=True, auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
