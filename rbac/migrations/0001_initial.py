# Generated by Django 2.0 on 2019-08-27 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='操作标题')),
                ('code', models.CharField(max_length=32, verbose_name='方法')),
            ],
            options={
                'verbose_name_plural': '操作动作管理',
                'verbose_name': '操作动作管理',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='菜单名称')),
                ('icon', models.CharField(blank=True, max_length=128, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限标题')),
                ('url', models.CharField(max_length=128, verbose_name='含正则的URL')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.Action', verbose_name='操作')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='菜单')),
                ('parent', models.ForeignKey(blank=True, limit_choices_to={'parent__isnull': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='父权限')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='拥有的所有权限')),
            ],
        ),
    ]
