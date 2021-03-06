# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-06 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logging_viewer', '0002_auto_20161223_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestresponsenote',
            name='process_time',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestresponsenote',
            name='request_body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestresponsenote',
            name='request_content_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='requestresponsenote',
            name='request_headers',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestresponsenote',
            name='request_query_params',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestresponsenote',
            name='response_body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestresponsenote',
            name='response_headers',
            field=models.TextField(blank=True, null=True),
        ),
    ]
