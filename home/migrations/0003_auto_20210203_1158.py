# Generated by Django 3.1.5 on 2021-02-03 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_auto_20210203_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='socialuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
