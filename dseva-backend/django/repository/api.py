from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Repository
from .serializers import RepositoriesListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def repositories_list(request):
    repositories = Repository.objects.all()
    serializer = RepositoriesListSerializer(repositories, many=True)

    return JsonResponse({
        'data': serializer.data
    })