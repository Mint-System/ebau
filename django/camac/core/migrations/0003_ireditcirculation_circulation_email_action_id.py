# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-27 07:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180306_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='ireditcirculation',
            name='circulation_email_action_id',
            field=models.ForeignKey(blank=True, db_column='CIRCULATION_EMAIL_ACTION_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Action'),
        ),
    ]
