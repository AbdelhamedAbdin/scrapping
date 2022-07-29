from rest_framework import serializers

from rest_pandas import PandasSerializer


class BookSerializer(serializers.Serializer):
    # download = serializers.SerializerMethodField(read_only=True, label="تحميل الكتاب", default="http://127.0.0.1:8000/5/")

    class Meta:
        list_serializer_class = PandasSerializer
