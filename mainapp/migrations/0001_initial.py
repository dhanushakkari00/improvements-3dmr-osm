# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-29 20:19
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.IntegerField()),
                ('revision', models.IntegerField()),
                ('title', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=512)),
                ('rendered_description', models.CharField(max_length=1024)),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('license', models.IntegerField()),
                ('tags', django.contrib.postgres.fields.hstore.HStoreField(default={})),
                ('rotation', models.FloatField(default=0.0)),
                ('scale', models.FloatField(default=1.0)),
                ('translation_x', models.FloatField(default=0.0)),
                ('translation_y', models.FloatField(default=0.0)),
                ('translation_z', models.FloatField(default=0.0)),
                ('is_hidden', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'mainapp_latestmodel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'mainapp_latestmodel_categories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(max_length=1024)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('banned_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeof', models.IntegerField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1024)),
                ('rendered_comment', models.CharField(max_length=2048)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_id', models.IntegerField()),
                ('revision', models.IntegerField()),
                ('title', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=512)),
                ('rendered_description', models.CharField(max_length=1024)),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('license', models.IntegerField()),
                ('tags', django.contrib.postgres.fields.hstore.HStoreField(default={})),
                ('rotation', models.FloatField(default=0.0)),
                ('scale', models.FloatField(default=1.0)),
                ('translation_x', models.FloatField(default=0.0)),
                ('translation_y', models.FloatField(default=0.0)),
                ('translation_z', models.FloatField(default=0.0)),
                ('is_hidden', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='mainapp.Category')),
                ('location', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='Your description...', max_length=2048)),
                ('rendered_description', models.CharField(default='<p>Your description...</p>', max_length=4096)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Model'),
        ),
        migrations.AddField(
            model_name='change',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Model'),
        ),
    ]
