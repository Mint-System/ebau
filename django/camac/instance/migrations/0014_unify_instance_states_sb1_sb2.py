# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-27 10:42
from __future__ import unicode_literals

from django.db import migrations
from camac.constants import kt_bern as constants


def migrate_instance_states(apps, schema_editor):
    Instance = apps.get_model("instance.Instance")
    Instance.objects.filter(
        instance_state__in=(
            constants.INSTANCE_STATE_SELBSTDEKLARATION_FREIGABEQUITTUNG,
        )
    ).update(instance_state=constants.INSTANCE_STATE_SELBSTDEKLARATION_AUSSTEHEND)

    Instance.objects.filter(
        instance_state__in=(
            constants.INSTANCE_STATE_ABSCHLUSS_DOKUMENTE,
            constants.INSTANCE_STATE_ABSCHLUSS_FREIGABEQUITTUNG,
        )
    ).update(instance_state=constants.INSTANCE_STATE_ABSCHLUSS_AUSSTEHEND)


class Migration(migrations.Migration):

    dependencies = [("instance", "0013_unify_instance_states")]

    operations = [migrations.RunPython(migrate_instance_states)]
