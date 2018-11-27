from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

import blog
from society.models import Comment
from users.functions import check_logined
from users.functions import get_User_Model


@check_logined
def add_comment_to_blog(request):
    if request.method == "POST":
        user = get_User_Model(request)
        comment_detail = request.POST.get('comment')
        post_type = request.POST.get('post_type')
        blog_id = request.POST.get('article_id')
        comment = Comment()
        comment.comment_creater = user
        comment.comment_detail = comment_detail
        comment.comment_to_which_blog_id = blog_id
        # 如果为对博客的评论，type为0 否则type表示评论的id
        if post_type == "0":
            comment.comment_type = 0
        else:
            comment.comment_type = 1
            comment.comment_is_not_read = 1
            comment.comment_to_which_Comment = post_type

        try:
            comment.save()
            return redirect(reverse('blog:blog_detail', args=(blog_id,)))
        except Exception as e:
            print(str(e))
            return HttpResponse('评论失败')


@check_logined
def del_comment(request, comment_id):
    print(comment_id)
    comment = Comment.objects.filter(pk=comment_id).first()
    blog_id = comment.comment_to_which_blog_id
    try:
        comment.delete()
        return redirect(reverse('blog:blog_detail', args=(blog_id,)))
    except Exception as e:
        print(str(e))
        return HttpResponse('删除失败')


@check_logined
def ajax_del_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.filter(pk=comment_id).first()
        try:
            comment.delete()
            return JsonResponse({'code': 200})
        except Exception as e:
            print(str(e))
            return JsonResponse({'code': 501, 'msg': '删除失败'})


@check_logined
def ajax_yidu_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.filter(pk=comment_id).first()
        comment.comment_is_not_read = 0
        try:
            comment.save()
            return JsonResponse({'code': 200})
        except Exception as e:
            print(str(e))
            return JsonResponse({'code': 501, 'msg': '删除失败'})


@check_logined
def ajax_weidu_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.filter(pk=comment_id).first()
        comment.comment_is_not_read = 1
        try:
            comment.save()
            return JsonResponse({'code': 200})
        except Exception as e:
            print(str(e))
            return JsonResponse({'code': 501, 'msg': '删除失败'})
