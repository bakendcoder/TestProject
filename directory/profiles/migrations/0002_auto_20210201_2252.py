# Generated by Django 3.1.5 on 2021-02-01 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherprofile',
            name='profile_picture',
            field=models.FileField(default='default_picture.jpeg', max_length='128', upload_to='teachers/'),
        ),
    ]