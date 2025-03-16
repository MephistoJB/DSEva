from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Developer1, Repository1
from .serializers import DeveloperListSerializer, RepositoriesListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def repositories_list(request):
    repositories = Repository1.objects.all()
    serializer = RepositoriesListSerializer(repositories, many=True)

    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def developer_list(request):
    developer = Developer1.objects.all()
    serializer = DeveloperListSerializer(developer, many=True)

    return JsonResponse({
        'data': serializer.data
    })