# Generated by Django 2.0 on 2019-08-27 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={},
        ),
        migrations.RenameField(
            model_name='action',
            old_name='caption',
            new_name='title',
        ),
    ]
