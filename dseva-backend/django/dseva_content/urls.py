from django.urls import path

from . import api 

urlpatterns = [
    path('', api.repositories_list, name='api_repositories_list'),
    path('repositories/', api.repositories_list, name='api_repositories_list'),
    path('developer/', api.developer_list, name='api_developer_list'),
    path('createrepository/', api.create_repository, name='api_create_repository'),
    path('nextelement/', api.next_element, name='api_next_element'),
    path('<int:id>/', api.repository_detail, name='api_repository_detail'),
]

