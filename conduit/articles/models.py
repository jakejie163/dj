# -*- coding:UTF-8 -*-

from django.db import models

from core.models import TimestampedModel
from profiles.models import Profile


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag


class Article(TimestampedModel):
    slug = models.CharField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="articles"
    )
    tags = models.ManyToManyField(Tag, related_name="articles")

    def __str__(self):
        return self.title

class Comment(TimestampedModel):
    body = models.TextField()
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, related_name="comments", on_delete=models.CASCADE)
