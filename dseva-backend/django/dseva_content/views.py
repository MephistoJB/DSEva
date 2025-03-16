from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets

# Create your views here.
class RepositoryView(ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositoriesListSerializer

    def create(self, request):
        print(request.data)
        #Perform check here
        return super().create(request)