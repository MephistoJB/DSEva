from rest_framework import serializers

from .models import*

class RepositoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = (
            'id',
            'title',
            'firstVisit',
            'lastVisit'
        )

class RepositoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = (
            'id',
            'title',
            'foreign_id',
            'firstVisit',
            'lastVisit'
        )


class DeveloperListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = (
            'id',
            'name'
        )