import pandas as pd

from rest_framework.views import Response, status
from rest_framework import viewsets, mixins
from rest_framework.renderers import JSONRenderer

from rest_pandas import PandasView

from django.http import HttpResponse
from django.views import View
from django.urls import reverse

from .serializers import BookSerializer

import pdfkit as pdf

import json, qrcode, os

from project.settings import BASE_DIR


class BookView(
        PandasView,
        viewsets.GenericViewSet,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin
    ):
    serializer_class = BookSerializer
    renderer_classes = [JSONRenderer]
    __ORDER_LABEL = 'الترتيب'  # index by that column

    # Get the main Dataframe
    def get_data(self, request, *args, **kwargs):
        df = pd.read_csv('table.xlsx')
        df.set_index(self.__ORDER_LABEL, inplace=True, drop=False)
        df = pd.DataFrame(df, columns=list(filter(lambda x: x != 'book', df.columns.to_list())))
        return df

    def list(self, request, *args):
        df = self.get_data(request, *args)
        serializer = self.serializer_class(df, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, order=None, **kwargs):
        df = self.get_data(request, *args)
        try:
            pk = int(order)
            df = pd.DataFrame(df.loc[pk]).drop(index=self.__ORDER_LABEL).to_json(force_ascii=False)
            data = dict(json.loads(df))
            data.update({"تحميل الكتاب": f"http://127.0.0.1:8000{reverse('api:download-book', args=[order])}"})
            return Response(json.loads(json.dumps(data)))
            # return Response(json.loads(df))
        except KeyError:
            return Response({'Message': ['Not Found']})

    def create(self, request, *args, **kwargs):
        df = self.get_data(request, *args)
        data_columns = list(filter(lambda data: data != self.__ORDER_LABEL, df.columns.to_list()))
        new_dataFrame = {}
        # Create a new index
        order_current_position = len(df.loc[:, self.__ORDER_LABEL])
        order_column = df.loc[order_current_position, self.__ORDER_LABEL]

        # check the length equality between request_data and data_columns
        if len(list(request.data)) != len(data_columns):
            return Response({'Message': 'the length of data is not equal to columns'})
        else:
            for request_columns in request.data:
                if request_columns in data_columns and request_columns != self.__ORDER_LABEL:
                    new_dataFrame.update({
                        request_columns: [request.data[request_columns]],
                        self.__ORDER_LABEL: [order_column + 1]
                    })
                else:
                    return Response({"Message": f"[{request_columns}] is not a correct column label name"})

        df2 = pd.DataFrame(new_dataFrame)
        df2.set_index(self.__ORDER_LABEL, inplace=True, drop=False)
        new_dataFrame = pd.concat([df, df2])
        new_dataFrame.to_csv("table.xlsx", index=False, encoding="utf-8")

        return Response(json.loads(new_dataFrame.to_json(force_ascii=False)), status=status.HTTP_201_CREATED)

    def update(self, request, *args, order=None, **kwargs):
        df = self.get_data(request, *args)
        data_columns = list(filter(lambda data: data != self.__ORDER_LABEL, df.columns.to_list()))
        new_dataFrame = {}

        try:
            pk = int(order)

            if len(list(request.data)) != len(data_columns):
                return Response({'Message': 'the length of data is not equal to columns'})
            else:
                for request_columns in request.data:
                    if request_columns in data_columns and request_columns != self.__ORDER_LABEL:
                        new_dataFrame.update({
                            request_columns: [request.data[request_columns]],
                            self.__ORDER_LABEL: [pk]
                        })
                        df.loc[pk, request_columns] = request.data[request_columns]
                        df.to_csv("table.xlsx", index=False, encoding="utf-8")
                    else:
                        return Response({"Message": f"[{request_columns}] is not a correct column label name"})

            return Response(json.loads(json.dumps(new_dataFrame)), status=status.HTTP_200_OK)
        except KeyError:
            return Response({'Message': ['Not Found']})

    def destroy(self, request, *args, order=None, **kwargs):
        df = self.get_data(request, *args)

        try:
            pk = int(order)
            df = df.drop(df[self.__ORDER_LABEL][pk])
            df.to_csv("table.xlsx", index=False, encoding="utf-8")
            return Response({'Message': ['Object has been removed successfully']}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'Message': ['Not Found']}, status=status.HTTP_404_NOT_FOUND)


class Downloader(View):

    def get(self, request, order=None):
        pk = int(order)
        order_label = 'الترتيب'

        if pk:
            df = pd.read_csv('table.xlsx')
            df.set_index(order_label, inplace=True, drop=False)
            queryset = df.loc[pk]

            create_qrcode = qrcode.make(queryset['book'])
            image_path = f"qrcode/{queryset[order_label]}.png"
            create_qrcode.save(image_path)

            with open("templates/file.html", "r+") as html_file:
                read_file = html_file.read().format(
                    novel=queryset['الرواية'],
                    author=queryset['المؤلف'],
                    qr_code=os.path.join(BASE_DIR / image_path)
                )
                pdf.from_string(read_file, f'novels/{queryset[order_label]}.pdf', css=['templates/style.css'])

            return HttpResponse("successful download")
        return HttpResponse("404 Not Found")
