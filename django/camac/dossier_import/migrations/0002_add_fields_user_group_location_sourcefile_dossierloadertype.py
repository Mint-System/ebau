# Generated by Django 2.2.17 on 2021-11-02 14:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import camac.dossier_import.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0014_servicegroup_sort"),
        ("dossier_import", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dossierimport",
            name="dossier_loader_type",
            field=models.CharField(
                choices=[("zip-archive-xlsx", "XlsxFileDossierLoader")],
                default="zip-archive-xlsx",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="dossierimport",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="dossier_imports",
                to="user.Group",
            ),
        ),
        migrations.AddField(
            model_name="dossierimport",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="user.Location",
            ),
        ),
        migrations.AddField(
            model_name="dossierimport",
            name="mime_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="dossierimport",
            name="source_file",
            field=models.FileField(
                blank=True,
                max_length=255,
                null=True,
                upload_to=camac.dossier_import.models.archive_path_directory_path,
            ),
        ),
        migrations.AddField(
            model_name="dossierimport",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="dossier_imports",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="dossier_loader_type",
            field=models.CharField(
                choices=[("zip-archive-xlsx", "XlsxFileDossierLoader")],
                default="zip-archive-xlsx",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="group",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="user.Group",
            ),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="location",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="user.Location",
            ),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="mime_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="source_file",
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="dossierimport",
            name="service",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="user.Service",
            ),
        ),
        migrations.AlterField(
            model_name="dossierimport",
            name="status",
            field=models.CharField(
                choices=[
                    ("done", "done"),
                    ("new", "new"),
                    ("in-progres", "in-progres"),
                    ("verified", "verified"),
                    ("failed", "failed"),
                ],
                default="new",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="historicaldossierimport",
            name="status",
            field=models.CharField(
                choices=[
                    ("done", "done"),
                    ("new", "new"),
                    ("in-progres", "in-progres"),
                    ("verified", "verified"),
                    ("failed", "failed"),
                ],
                default="new",
                max_length=32,
            ),
        ),
    ]
