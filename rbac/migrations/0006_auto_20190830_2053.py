# Generated by Django 2.0 on 2019-08-30 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_role_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='action',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Action', verbose_name='操作'),
        ),
    ]
