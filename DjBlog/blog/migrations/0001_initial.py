# Generated by Django 2.1.1 on 2018-10-18 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='作者')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('en_title', models.CharField(max_length=100, verbose_name='英文标题')),
                ('tags', models.CharField(blank=True, help_text='用逗号分隔', max_length=200, null=True, verbose_name='标签')),
                ('summary', models.TextField(verbose_name='摘要')),
                ('content', models.TextField(verbose_name='正文')),
                ('view_times', models.IntegerField(default=0)),
                ('zan_times', models.IntegerField(default=0)),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('rank', models.IntegerField(default=0, verbose_name='排序')),
                ('status', models.IntegerField(choices=[(0, '正常'), (1, '草稿'), (2, '删除')], default=0, verbose_name='状态')),
                ('pub_time', models.DateTimeField(default=False, verbose_name='发布时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='CarouselModel',
            fields=[
                ('title', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='标题')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='摘要')),
                ('total_number', models.IntegerField(default=0, verbose_name='总数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='导航条内容')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='指向地址')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AddField(
            model_name='blogpostmodel',
            name='carousel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.CarouselModel', verbose_name='分类'),
        ),
    ]
