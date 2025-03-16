from django.forms import ModelForm

from .models import Repository


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