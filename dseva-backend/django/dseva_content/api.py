from django.http import JsonResponse
from django.db.models import Case, When, F
import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from dseva_content.models.developer import Developer
from dseva_content.models.repository import *
from .serializers import *
from .forms import RepositoryForm, DeveloperForm

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def repositories_list(request):
    repositories = Repository.objects.all()
    serializer = RepositoriesListSerializer(repositories, many=True)

    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def developer_list(request):
    developer = Developer.objects.all()
    serializer = DeveloperListSerializer(developer, many=True)

    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def next_element(request):

    repository = Repository.objects.annotate(
        new_order=Case(
            When(new=True, then=0),  # Wenn new=True, dann Reihenfolge 0
            default=1,               # Standardreihenfolge für alles andere
            output_field=models.IntegerField()
        )
    #).filter(lastVisit__lt=datetime.datetime.now() - datetime.timedelta(days=1)).order_by('new_order', 'lastVisit').first()
    ).order_by('new_order', 'lastVisit').first()

    developer = Developer.objects.annotate(
        new_order=Case(
            When(new=True, then=0),  # Wenn new=True, dann Reihenfolge 0
            default=1,               # Standardreihenfolge für alles andere
            output_field=models.IntegerField()
        )
    ).order_by('new_order', 'lastVisit').first()
    #).filter(lastVisit__lt=datetime.datetime.now() - datetime.timedelta(days=1)).order_by('new_order', 'lastVisit').first()
    #if developer.lastVisit>repository.lastVisit:
    #serializer = RepositoryDetailSerializer(repository)
    #else:
    
    print('debug', f"Developer with id {developer.foreign_id} lastVisited: {developer.lastVisit}")
    print('debug', f"Repository {repository.title} with id {repository.foreign_id} lastVisited: {repository.lastVisit}")

    if developer.lastVisit<repository.lastVisit:
        developer.lastVisit = datetime.datetime.now()
        developer.save()
        serializer = DeveloperDetailSerializer(developer)
    else:
        repository.lastVisit = datetime.datetime.now()
        repository.save()
        serializer = RepositoryDetailSerializer(repository)
    return JsonResponse({
        'data': serializer.data
    })

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def repository_detail(request, id):
    repository = Repository.objects.filter(foreign_id=id)
    values = repository.values()
    values2 = Repository.objects.all().values()
    #repository = Repository.objects.all()
    serializer = RepositoryDetailSerializer(repository[0], many=False)
    #serializer = RepositoriesListSerializer([repository], many=True)
    return JsonResponse(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_and_update_repository(request):
    fi = request.POST['foreign_id']
    repository = Repository.objects.filter(foreign_id=fi).first()
    if(not repository):
        repository = Repository.objects.filter(foreign_id=[fi]).first()
    post_data = dict(request.POST)
    post_data['foreign_id'] = fi
    post_data['title'] = post_data['title'][0]
    if 'ownerD' in post_data:
        di = request.POST.get('ownerD')
        developer = Developer.objects.filter(foreign_id=di).first()
        if not developer:
            developer = Developer.objects.create()
            developer.foreign_id = di
            developer.lastVisit = datetime.datetime.now()
            developer.save()
        else:
            developer.new = False
        post_data['ownerD']=developer.id
    if(repository):
        post_data['new']=False
        form = RepositoryForm(post_data, instance=repository)
    else:
        form = RepositoryForm(post_data)

    if form.is_valid():
        repo = form.save(commit=False)
        repo.ownerD = developer
        repo.lastVisit = datetime.datetime.now()
        repo.save()
        return JsonResponse({'success': True})
    else:
        error = form.errors
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'errors': form.errors.as_json()}, status=400)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_and_update_developer(request):
    fi = request.POST['foreign_id']
    developer = Developer.objects.filter(foreign_id=fi).first()
    if(not developer):
         developer = Developer.objects.filter(foreign_id=[fi]).first()
    post_data = dict(request.POST)
    post_data['foreign_id'] = fi
    post_data['name'] = post_data['name'][0]
    
    # Handle follow relationship if provided
    #if 'follow' in post_data:
    #    follow_id = request.POST.get('follow')
    #    follow_developer = Developer.objects.filter(foreign_id=follow_id).first()
    #    if follow_developer:
    #        post_data['follow'] = follow_developer.id
    #    else:
    #         # Remove follow if developer doesn't exist
    #         post_data.pop('follow', None)
    
    if developer:
        post_data['new'] = False
        form = DeveloperForm(post_data, instance=developer)
    else:
        form = DeveloperForm(post_data)
    if form.is_valid():
        dev = form.save(commit=False)
        dev.lastVisit = datetime.datetime.now()
        dev.save()
        return JsonResponse({'success': True})
    else:
        error = form.errors
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'errors': form.errors.as_json()}, status=400)