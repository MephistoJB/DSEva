from rest_framework import serializers

from dseva_content.models.developer import Developer
from dseva_content.models.repository import *


class RepositoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = (
            'id',
            'title',
            'foreign_id',
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
            'lastVisit',
            'type'
        )

class DeveloperDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = (
            'id',
            'title',
            'foreign_id',
            'firstVisit',
            'lastVisit',
            'type'
        )


class DeveloperListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = (
            'id',
            'name'
        )