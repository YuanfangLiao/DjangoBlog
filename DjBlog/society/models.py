from django.db import models

# Create your models here.

# 评论表
from django.db.models import CASCADE

from blog.models import BlogPostModel
from users.models import UserModel

STATUS = {
    0: u'对文章的评论',
    1: u'对评论的评论',
}


class Comment(models.Model):
    comment_type = models.IntegerField(default=0)
    comment_to_which_blog = models.ForeignKey(BlogPostModel, on_delete=CASCADE, null=False)
    # 如果是对评论的评论，则保存原评论的id
    comment_to_which_Comment = models.IntegerField(null=True)
    # 评论的作者
    comment_creater = models.ForeignKey(UserModel,on_delete=CASCADE)
    comment_detail = models.TextField(null=False, max_length=200)

    comment_time = models.DateTimeField(auto_now=True)
    comment_zan_times = models.IntegerField(default=0)
    comment_is_not_read = models.BooleanField(default=0)
