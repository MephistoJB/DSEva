from rest_framework import serializers

from .models import Repository

class RepositoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = (
            'id',
            'title'
        )