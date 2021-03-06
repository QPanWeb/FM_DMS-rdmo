# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-29 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0035_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subsection',
            name='section',
        ),
        migrations.AlterModelOptions(
            name='questionset',
            options={'ordering': ('section', 'order'), 'permissions': (('view_questionset', 'Can view Question set'),), 'verbose_name': 'Question set', 'verbose_name_plural': 'Question set'},
        ),
        migrations.RemoveField(
            model_name='questionset',
            name='subsection',
        ),
        migrations.AlterField(
            model_name='questionset',
            name='section',
            field=models.ForeignKey(help_text='The section this questionset belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='questionsets', to='questions.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='title_de',
            field=models.CharField(help_text='The German title for this questionset.', max_length=256, verbose_name='Title (de)'),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='title_en',
            field=models.CharField(help_text='The English title for this questionset.', max_length=256, verbose_name='Title (en)'),
        ),
        migrations.DeleteModel(
            name='Subsection',
        ),
    ]
