# Generated by Django 5.1 on 2025-01-30 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dseva_content', '0012_rename_owner_repository_ownerd_developer_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='foreign_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
