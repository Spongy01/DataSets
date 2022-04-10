# Generated by Django 3.2.5 on 2022-04-02 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FolTabRel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_folder', models.CharField(max_length=20)),
                ('p_folder_brief', models.CharField(blank=True, max_length=50)),
                ('c_table', models.CharField(max_length=20)),
                ('c_table_brief', models.CharField(blank=True, max_length=50)),
                ('is_fav', models.BooleanField(default=False)),
                ('is_pinned', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FolFolRel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_folder', models.CharField(max_length=20)),
                ('p_folder_brief', models.CharField(blank=True, max_length=50)),
                ('c_folder', models.CharField(max_length=20)),
                ('c_folder_brief', models.CharField(blank=True, max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
