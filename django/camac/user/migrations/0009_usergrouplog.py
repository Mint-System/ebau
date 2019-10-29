# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-25 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20191023_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroupLog',
            fields=[
                ('user_group_log_id', models.AutoField(db_column='USER_GROUP_LOG_ID', primary_key=True, serialize=False)),
                ('modification_date', models.DateTimeField(db_column='MODIFICATION_DATE')),
                ('user_id', models.IntegerField(db_column='USER_ID')),
                ('action', models.CharField(db_column='ACTION', max_length=500)),
                ('data', models.TextField(blank=True, db_column='DATA', null=True)),
                ('id1', models.IntegerField(db_column='ID1')),
                ('field1', models.CharField(db_column='FIELD1', max_length=30)),
                ('id2', models.IntegerField(db_column='ID2')),
                ('field2', models.CharField(db_column='FIELD2', max_length=30)),
            ],
            options={
                'db_table': 'USER_GROUP_LOG',
                'managed': True,
            },
        ),
    ]
