# Generated by Django 2.1.3 on 2018-11-15 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181113_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Swipers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('swiper_img_url', models.TextField(max_length=100)),
                ('swiper_url', models.TextField(max_length=100, null=True)),
                ('swiper_title', models.TextField(max_length=100, null=True)),
            ],
        ),
    ]
