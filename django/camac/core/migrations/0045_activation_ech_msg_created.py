# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-08 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_journal_translation_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='activation',
            name='ech_msg_created',
            field=models.BooleanField(default=False),
        ),
    ]
