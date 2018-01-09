# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-09 14:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_auto_20180109_1440'),
        ('instance', '0001_initial'),
        ('document', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='attachmentsectionservice',
            name='service',
            field=models.ForeignKey(db_column='SERVICE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Service'),
        ),
        migrations.AddField(
            model_name='attachmentsectionrole',
            name='attachment_section',
            field=models.ForeignKey(db_column='ATTACHMENT_SECTION_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='document.AttachmentSection'),
        ),
        migrations.AddField(
            model_name='attachmentsectionrole',
            name='role',
            field=models.ForeignKey(db_column='ROLE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Role'),
        ),
        migrations.AddField(
            model_name='attachmentextensionservice',
            name='attachment_extension',
            field=models.ForeignKey(db_column='ATTACHMENT_EXTENSION_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='document.AttachmentExtension'),
        ),
        migrations.AddField(
            model_name='attachmentextensionservice',
            name='service',
            field=models.ForeignKey(db_column='SERVICE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Service'),
        ),
        migrations.AddField(
            model_name='attachmentextensionrole',
            name='attachment_extension',
            field=models.ForeignKey(db_column='ATTACHMENT_EXTENSION_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='document.AttachmentExtension'),
        ),
        migrations.AddField(
            model_name='attachmentextensionrole',
            name='role',
            field=models.ForeignKey(db_column='ROLE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Role'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='attachment_section',
            field=models.ForeignKey(db_column='ATTACHMENT_SECTION_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='attachments', to='document.AttachmentSection'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='instance',
            field=models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='attachments', to='instance.Instance'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='service',
            field=models.ForeignKey(blank=True, db_column='SERVICE_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.Service'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='user',
            field=models.ForeignKey(db_column='USER_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='attachments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentsectionservice',
            unique_together=set([('attachment_section', 'service')]),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentsectionrole',
            unique_together=set([('attachment_section', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentextensionservice',
            unique_together=set([('attachment_extension', 'service')]),
        ),
        migrations.AlterUniqueTogether(
            name='attachmentextensionrole',
            unique_together=set([('attachment_extension', 'role')]),
        ),
    ]
