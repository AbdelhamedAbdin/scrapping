from django.shortcuts import render

from .models import BookModel

import pandas as pd
from django_pandas.io import read_frame
from rest_pandas import PandasSimpleView, PandasView, PandasUnstackedSerializer
from rest_framework.views import Response
from rest_framework.generics import ListAPIView

from .serializers import BookSerializer


# class BookView(PandasSimpleView):
#
#     def get_data(self, request, *args, **kwargs):
#         qs = BookModel.objects.all()
#         return pd.read_csv('table.xlsx')
#         # df = read_frame(qs)
#         # print(df)
#
#     def get(self, request, *args):
#         df = read_frame(BookModel.objects.all())
#         print(df)
#         return Response(df)

# class BookView(PandasView):
#
#     def get(self, request, *args):
#         df = read_frame(BookModel.objects.all())
#         print(df)
#         return Response(df, template_name="api.html")


class BookView(PandasView, ListAPIView):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    pandas_serializer_class = PandasUnstackedSerializer

    def get_data(self, request, *args, **kwargs):
        # qs = BookModel.objects.all()
        return pd.read_csv('table.xlsx')
        # df = read_frame(qs)
        # print(df)

    def get(self, request, *args, **kwargs):
        # df = read_frame(BookModel.objects.all())
        df = self.get_data(request, *args)
        serializer = self.serializer_class(df, many=True)
        return Response(serializer.data, template_name='api.html')
