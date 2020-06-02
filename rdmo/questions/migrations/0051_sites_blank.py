# Generated by Django 2.2.9 on 2020-02-14 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0050_data_migration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='sites',
            field=models.ManyToManyField(blank=True, help_text='The sites this catalog belongs to (in a multi site setup).', to='sites.Site', verbose_name='Sites'),
        ),
    ]