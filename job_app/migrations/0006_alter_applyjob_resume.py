# Generated by Django 4.1.1 on 2022-10-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_app', '0005_applyjob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyjob',
            name='resume',
            field=models.ImageField(upload_to='job_app/static'),
        ),
    ]
