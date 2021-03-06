# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-14 17:19
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    from common.utilities import generate_unique_key
    FileType = apps.get_model("bot", "FileType")
    db_alias = schema_editor.connection.alias

    types = [
        'image', 'video', 'url'
    ]

    FileType.objects.using(db_alias).bulk_create(
        [
            FileType(
                id=generate_unique_key(i),
                name=i
            ) for i in types
        ]
    )


def reverse_func(apps, schema_editor):
    from common.utilities import generate_unique_key
    FileType = apps.get_model("bot", "FileType")
    db_alias = schema_editor.connection.alias
    types = [
        'image', 'video', 'url'
    ]
    FileType.objects.using(db_alias).filter(
        pk__in=[generate_unique_key(i) for i in types]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
