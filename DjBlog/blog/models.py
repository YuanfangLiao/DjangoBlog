from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING, PROTECT

from DjBlog import settings
from users.models import UserModel

# 文章状态
STATUS = {
    0: u'正常',
    1: u'草稿',
    2: u'删除',
}


# 导航栏
class Nav(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'导航条内容')
    url = models.CharField(max_length=200, blank=True, null=True,
                           verbose_name=u'指向地址')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)


# 分类表
class CarouselModel(models.Model):
    title = models.CharField(max_length=100, primary_key=True, verbose_name=u'标题')
    summary = models.TextField(blank=True, null=True, verbose_name=u'摘要')
    total_number = models.IntegerField(default=0, verbose_name=u'总数')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)


# 博客文章表
class BlogPostModel(models.Model):
    author = models.ForeignKey(settings.USER_MODEL, max_length=100, verbose_name=u'作者', on_delete=PROTECT)
    carousel = models.ForeignKey(CarouselModel, verbose_name=u'分类', on_delete=PROTECT)
    title = models.CharField(max_length=100, verbose_name=u'标题')
    en_title = models.CharField(max_length=100, null=True, verbose_name=u'英文标题')
    tags = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name=u'标签', help_text=u'用逗号分隔')
    summary = models.TextField(verbose_name=u'摘要')
    content = models.TextField(verbose_name=u'正文')
    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)

    is_top = models.BooleanField(default=False, verbose_name=u'置顶')
    rank = models.IntegerField(default=0, verbose_name=u'排序')
    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name='状态')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def get_tags(self):
        self.tags.replace('\ ', ',')
        tags_list = self.tags.split(',')
        while ' ' in tags_list:
            tags_list.remove(' ')
        return tags_list
