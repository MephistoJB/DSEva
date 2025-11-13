from django.forms import ModelForm

from .models import Repository, Developer


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = (
            'title',
            'foreign_id',
            #'description',
            'ownerD',
            'parent',
            #'watched_count',
            #'stars_count',
            #'loc',
            #'files',
        )

class DeveloperForm(ModelForm):
    class Meta:
        model = Developer
        fields = (
            'name',
            'foreign_id'
        )