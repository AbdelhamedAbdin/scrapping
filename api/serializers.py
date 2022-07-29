from rest_framework import serializers

from rest_pandas import PandasSerializer


class BookSerializer(serializers.Serializer):

    class Meta:
        list_serializer_class = PandasSerializer
