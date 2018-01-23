# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-23 15:01
from __future__ import unicode_literals

import camac.document.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachment_id', models.AutoField(db_column='ATTACHMENT_ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='NAME', max_length=255)),
                ('path', models.FileField(db_column='PATH', max_length=1024, upload_to=camac.document.models.attachment_path_directory_path)),
                ('size', models.IntegerField(db_column='SIZE')),
                ('date', models.DateTimeField(db_column='DATE', default=django.utils.timezone.now)),
                ('mime_type', models.CharField(db_column='MIME_TYPE', max_length=255)),
                ('is_parcel_picture', models.PositiveIntegerField(db_column='IS_PARCEL_PICTURE', default=0)),
                ('digital_signature', models.PositiveSmallIntegerField(db_column='DIGITAL_SIGNATURE', default=0)),
                ('is_confidential', models.PositiveSmallIntegerField(db_column='IS_CONFIDENTIAL', default=0)),
                ('identifier', models.CharField(blank=True, db_column='IDENTIFIER', max_length=255, null=True)),
            ],
            options={
                'db_table': 'ATTACHMENT',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AttachmentSection',
            fields=[
                ('attachment_section_id', models.AutoField(db_column='ATTACHMENT_SECTION_ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='NAME', max_length=100, unique=True)),
                ('sort', models.IntegerField(db_column='SORT', db_index=True)),
            ],
            options={
                'db_table': 'ATTACHMENT_SECTION',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AttachmentSectionGroupAcl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('read', 'Read permissions'), ('write', 'Read and write permissions'), ('admin', 'Read, write and delete permissions')], max_length=10)),
                ('attachment_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_acls', to='document.AttachmentSection')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.Group')),
            ],
        ),
        migrations.CreateModel(
            name='AttachmentSectionRoleAcl',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('mode', models.CharField(choices=[('read', 'Read permissions'), ('write', 'Read and write permissions'), ('admin', 'Read, write and delete permissions')], db_column='MODE', max_length=10)),
                ('attachment_section', models.ForeignKey(db_column='ATTACHMENT_SECTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='role_acls', to='document.AttachmentSection')),
                ('role', models.ForeignKey(db_column='ROLE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.Role')),
            ],
            options={
                'db_table': 'ATTACHMENT_SECTION_ROLE',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='AttachmentSectionServiceAcl',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('mode', models.CharField(db_column='MODE', max_length=20)),
                ('attachment_section', models.ForeignKey(db_column='ATTACHMENT_SECTION_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='document.AttachmentSection')),
                ('service', models.ForeignKey(db_column='SERVICE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.Service')),
            ],
            options={
                'db_table': 'ATTACHMENT_SECTION_SERVICE',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='attachment_section',
            field=models.ForeignKey(db_column='ATTACHMENT_SECTION_ID', on_delete=django.db.models.deletion.PROTECT, related_name='attachments', to='document.AttachmentSection'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attachments', to='user.Group'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='instance',
            field=models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='instance.Instance'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='service',
            field=models.ForeignKey(blank=True, db_column='SERVICE_ID', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='user.Service'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='user',
            field=models.ForeignKey(db_column='USER_ID', on_delete=django.db.models.deletion.PROTECT, related_name='attachments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentsectionserviceacl',
            unique_together=set([('attachment_section', 'service')]),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentsectionroleacl',
            unique_together=set([('attachment_section', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentsectiongroupacl',
            unique_together=set([('attachment_section', 'group')]),
        ),
    ]
