from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

import blog
from society.models import Comment
from users.functions import check_logined
from users.views import get_User_Model


@check_logined
def add_comment_to_blog(request):
    if request.method == "POST":
        user = get_User_Model(request)
        comment_detail = request.POST.get('comment')
        blog_id = request.POST.get('article_id')
        comment = Comment()
        comment.comment_type = 0
        comment.comment_to_which_blog_id = blog_id
        comment.comment_creater = user
        comment.comment_detail = comment_detail

        try:
            comment.save()
            return redirect(reverse('blog:blog_detail', args=(blog_id,)))
        except Exception as e:
            print(str(e))
            return HttpResponse('评论失败')


def add_comment_to_comment(request):
    pass
