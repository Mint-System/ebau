# Generated by Django 2.2.11 on 2020-04-27 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20200423_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='instance',
            field=models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='instance.Instance'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='instance',
            field=models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='instance.Instance'),
        ),
    ]
