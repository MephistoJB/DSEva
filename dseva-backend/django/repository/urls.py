from django.urls import path

from . import api 

urlpatterns = [
    path('', api.repositories_list, name='api_repositories_list'),
    path('', api.developer_list, name='api_developer_list'),
]

