from rest_framework import serializers

from .models import Developer1, Repository1

class RepositoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository1
        fields = (
            'id',
            'title'
        )
class DeveloperListSerializer(serializers.ModelSerializer):
        model = Developer1
        fields = (
            'id',
            'name'
        )