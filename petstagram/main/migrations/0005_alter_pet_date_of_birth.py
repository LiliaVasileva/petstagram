# Generated by Django 4.0.3 on 2022-04-06 14:06

import datetime
from django.db import migrations, models
import petstagram.common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_petphoto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, validators=[
                petstagram.common.validators.MinDateValidator(datetime.date(1920, 1, 1))]),
        ),
    ]
