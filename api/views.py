from django.http import JsonResponse

from .models import BookModel

import pandas as pd
from django_pandas.io import read_frame

from rest_framework.views import Response, APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_pandas import (PandasSimpleView, PandasView, PandasViewSet)
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .serializers import BookSerializer


class BookView(PandasView, ListCreateAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    renderer_classes = [JSONRenderer]

    def get_data(self, request, *args, **kwargs):
        return pd.read_csv('table.xlsx')

    def get(self, request, *args, **kwargs):
        # df = read_frame(BookModel.objects.all()) from database
        df = self.get_data(request, *args) # from io file
        serializer = self.serializer_class(df, many=True)
        # return Response(serializer.data, template_name='api.html', content_type="application/json")
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        pass
