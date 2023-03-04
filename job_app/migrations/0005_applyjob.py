# Generated by Django 4.1.1 on 2022-10-19 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_app', '0004_delete_user_logmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='applyjob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=50)),
                ('jtitle', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('quali', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('uexp', models.CharField(choices=[('0-1', '0-1'), ('1-2', '1-2'), ('2-3', '2-3'), ('3-4', '3-4'), ('4-5', '4-5'), ('5-6', '5-6'), ('6-7', '6-7'), ('7-8', '7-8')], max_length=30)),
                ('resume', models.ImageField(upload_to='job_app/static/cvs')),
            ],
        ),
    ]
