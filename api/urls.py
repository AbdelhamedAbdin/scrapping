from . import views
from django.urls import path

app_name = "api"

urlpatterns = [
    path('', views.BookView.as_view({'get': 'list', 'post': 'create'}), name="book-view"),
    path('<int:order>/', views.BookView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="book-view"),
    # Download view
    path('download-book/<int:order>/', views.Downloader.as_view(), name="download-book")
]
