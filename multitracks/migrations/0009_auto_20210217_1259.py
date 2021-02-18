# Generated by Django 3.1.2 on 2021-02-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multitracks', '0008_auto_20210201_1804'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Band',
            new_name='Artist',
        ),
        migrations.RenameField(
            model_name='multitrack',
            old_name='band',
            new_name='artist',
        ),
        migrations.AlterField(
            model_name='multitrack',
            name='file_zip',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='multitrack',
            name='preview',
            field=models.URLField(),
        ),
    ]
