from rest_framework import serializers

<<<<<<< HEAD
from .models import Repository
=======
from .models import Developer1, Repository1
>>>>>>> 098b29c (Enabled remote debugging and github sync of the first objects)

class RepositoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository1
        fields = (
            'id',
            'title'
<<<<<<< HEAD
=======
        )
class DeveloperListSerializer(serializers.ModelSerializer):
        model = Developer1
        fields = (
            'id',
            'name'
>>>>>>> 098b29c (Enabled remote debugging and github sync of the first objects)
        )