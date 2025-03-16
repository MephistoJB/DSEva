from django.contrib import admin

from dseva_content.models.repository import *
from dseva_content.models.developer import Developer
# Register your models here.

#admin.site.register(Repository)
admin.site.register(Developer)

class RepoAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in Repository._meta.fields]
    list_display = ('id', 'title', 'foreign_id', 'new')
admin.site.register(Repository, RepoAdmin)