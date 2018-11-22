# Generated by Django 2.1.3 on 2018-11-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('user_id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('user_passwd', models.CharField(max_length=32)),
                ('user_phone', models.CharField(max_length=11, null=True, unique=True)),
                ('user_email', models.CharField(max_length=64, unique=True)),
                ('user_sex', models.BooleanField(default=1)),
                ('user_img', models.ImageField(null=True, upload_to='users')),
                ('user_is_admin', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'djblog_user',
            },
        ),
    ]
