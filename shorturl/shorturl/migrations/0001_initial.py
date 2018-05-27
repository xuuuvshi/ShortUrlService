# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-05-26 08:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import shorturl.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_time')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated_time')),
                ('custom_url', models.CharField(db_index=True, max_length=32, verbose_name='custom_url')),
                ('access_count', models.IntegerField(default=0, verbose_name='access_count')),
                ('long_url', models.CharField(max_length=200, verbose_name='long_url')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'short_url',
            },
            bases=(shorturl.models.HashKeyBuilderMixin, models.Model),
        ),
    ]