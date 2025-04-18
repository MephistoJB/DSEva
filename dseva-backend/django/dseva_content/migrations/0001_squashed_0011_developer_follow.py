# Generated by Django 5.1 on 2025-01-30 19:50

import django.db.models.deletion
import django.utils.timezone
import dseva_content.models.repository
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('dseva_content', '0001_initial'), ('dseva_content', '0002_repository_description_repository_files_and_more'), ('dseva_content', '0003_repository_created_at_repository_updated_at'), ('dseva_content', '0004_alter_repository_created_at_and_more'), ('dseva_content', '0005_alter_repository_description_alter_repository_owner_and_more'), ('dseva_content', '0006_alter_repository_created_at'), ('dseva_content', '0007_repository_foreign_id'), ('dseva_content', '0008_repository_firstvisit_repository_lastvisit_and_more'), ('dseva_content', '0009_alter_repository_foreign_id'), ('dseva_content', '0010_repository_new'), ('dseva_content', '0011_developer_follow')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('follow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='dseva_content.developer')),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('files', models.IntegerField(default=0)),
                ('loc', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='dseva_content.developer')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='dseva_content.repository')),
                ('stars_count', models.IntegerField(default=0)),
                ('watched_count', models.IntegerField(default=0)),
                ('created_at', dseva_content.models.repository.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', dseva_content.models.repository.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('foreign_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('firstVisit', dseva_content.models.repository.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('lastVisit', dseva_content.models.repository.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(default='Repository', editable=False, max_length=255)),
                ('new', models.BooleanField(default=True)),
            ],
        ),
    ]
