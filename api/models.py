from django.db import models
from django_pandas.managers import DataFrameManager


class BookModel(models.Model):
    book_ordering = models.IntegerField()
    novel = models.CharField(max_length=255)
    author = models.CharField(max_length=150)
    country = models.CharField(max_length=30)
    objects = DataFrameManager()

    class Meta:
        ordering = ('-book_ordering',)

    def __str__(self):
        return self.book_ordering
