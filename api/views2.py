from django.shortcuts import render

from .models import BookModel

import pandas as pd
from django_pandas.io import read_frame
from rest_pandas import (PandasSimpleView, PandasView, PandasUnstackedSerializer,
                         PandasCSVRenderer, PandasExcelRenderer, PandasViewSet)
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer

from .serializers import BookSerializer


class TimeSeriesView(PandasView):
    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    pandas_serializer_class = PandasUnstackedSerializer
    # renderer_classes = [PandasCSVRenderer, PandasExcelRenderer]
    renderer_classes = [PandasExcelRenderer]

    def get_data(self, request, *args, **kwargs):
        print(BookModel.objects.to_dataframe())
        return BookModel.objects.to_dataframe()

    def filter_queryset(self, qs):
        return qs

    def transform_dataframe(self, dataframe):
        dataframe.some_pivot_function(in_place=True)
        return dataframe

    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            return "Data Export"
        else:
            return None
