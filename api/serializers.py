from rest_framework import serializers

from rest_pandas import PandasSerializer


class BookSerializer(serializers.Serializer):
    book_ordering = serializers.IntegerField()
    novel = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=150)
    country = serializers.CharField(max_length=30)

    class Meta:
        list_serializer_class = PandasSerializer
