# Generated by Django 3.1.5 on 2021-02-09 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mixes', '0003_auto_20210204_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='owner',
        ),
    ]
