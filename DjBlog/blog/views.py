import os
import random

import markdown
from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

# 加载主页
from DjBlog import settings
from blog.models import CarouselModel, BlogPostModel, Nav
from users.functions import check_logined, get_uid
from users.models import UserModel


def index(request):
    sessionid = request.COOKIES.get('sessionid')

    if request.session.session_key == sessionid:
        uid = request.session.get('user_id')
        user = UserModel.objects.filter(user_id=uid).first()
        data = {'uid': uid, 'user': user}

    else:
        data = {'uid': None}

    # 博客分类信息，按个数排名 文章信息，导航栏信息
    carouses = CarouselModel.objects.all().order_by('total_number')
    all_blogs = BlogPostModel.objects.all().order_by('-create_time')
    tags = []
    for blog in all_blogs:
        tags += blog.get_tags()
    navs = Nav.objects.all()
    paginator = Paginator(all_blogs, 5)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
        now_page = page
    except PageNotAnInteger:
        blogs = paginator.page(1)
        now_page = 1
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
        now_page = paginator.num_pages

    print(tags)
    data['carouses'] = carouses
    data['blogs'] = blogs
    data['navs'] = navs
    data['tags'] = tags
    data['now_page'] = now_page
    data['num_pages'] = paginator.num_pages

    response = render(request, 'index.html', data)
    return response


def changetx(request):
    ...


def blog_detail(request, blog_id):
    if request.method == 'GET':
        # 导航
        navs = Nav.objects.all()
        # 博客
        blog = BlogPostModel.objects.all().filter(pk=blog_id).first()
        data = {}
        data['navs'] = navs
        data['blog'] = blog

        post = get_object_or_404(BlogPostModel, pk=blog_id)
        # 记得在顶部引入 markdown 模块
        post.body = markdown.markdown(post.content,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        uid = get_uid(request)
        data['post'] = post
        data['uid'] = uid

        return render(request, 'blog/blog_detail.html', context=data)


@check_logined
def post_new_blog(request):
    # post = get_object_or_404(BlogPostModel, pk=1)
    # 获取所有分类数据
    carousels = CarouselModel.objects.all()

    uid = get_uid(request)
    navs = Nav.objects.all()
    # 记得在顶部引入 markdown 模块
    # post.body = markdown.markdown(post.content,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                               ])
    data = {}
    # data['post'] = post
    data['uid'] = uid
    data['carousels'] = carousels
    data['navs'] = navs
    return render(request, 'blog/post_new_blog.html', context=data)


# 发布博文
@check_logined
def do_post_new_blog(request):
    if request.method == "POST":
        blog_title = request.POST.get('blog_title')
        eng_title = request.POST.get('eng_title')
        blog_content = request.POST.get('blog_content')
        blog_tags = request.POST.get('blog_tags')
        blog_carousel = request.POST.get('blog_carousel')

        uid = get_uid(request)

        new_blog = BlogPostModel()
        new_blog.author_id = uid
        new_blog.title = blog_title
        new_blog.content = blog_content
        new_blog.tags = blog_tags
        new_blog.carousel_id = blog_carousel

        summmary = ''.join(blog_content.split())
        # 如果文字长度大于30，摘要为前30个字，如果小于30，就为文章本身
        if len(summmary) >= 100:
            new_blog.summary = summmary[:100]
        else:
            new_blog.summary = summmary
        # 如果有英文标题
        if eng_title:
            new_blog.en_title = eng_title

        try:
            new_blog.save()
            return JsonResponse({'code': 200})
        except Exception as e:
            print('服务器错误', str(e))
            return JsonResponse({'code': 501, 'msg': str(e)})


# 写博客上传图片
@check_logined
def blog_img_upload(request):
    if request.method == "POST":
        data = request.FILES['editormd-image-file']
        img = Image.open(data)
        width = img.width
        height = img.height
        rate = 1.0  # 压缩率

        # 根据图像大小设置压缩率
        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)  # 新的宽
        height = int(height * rate)  # 新的高

        img.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图

        url = 'blogimg/' + data.name
        name = settings.MEDIA_ROOT + '/' + url
        while os.path.exists(name):
            file, ext = os.path.splitext(data.name)
            file = file + str(random.randint(1, 1000))
            data.name = file + ext
            url = 'blogimg/' + data.name
            name = settings.MEDIA_ROOT + '/' + url
        try:
            img.save(name)
            url = '/static' + name.split('static')[-1]
            return JsonResponse({'success': 1, 'message': '成功', 'url': url})
        except Exception as e:
            return JsonResponse({'success': 0, 'message': '上传失败'})


def test(request):
    post = get_object_or_404(BlogPostModel, pk=1)
    # 记得在顶部引入 markdown 模块
    post.body = markdown.markdown(post.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    uid = get_uid(request)
    return render(request, 'blog/test.html', context={'post': post, 'uid': uid})


def search(request):
    if request.method == "GET":
        kw = request.GET['kw']
        # 请求为空返回空
        if kw:
            # 先尝试获取有没有搜到名字一样的author
            authors = UserModel.objects.filter(user_id__contains=kw)
            carousels = CarouselModel.objects.filter(title__contains=kw)
            blogs = BlogPostModel.objects.filter(
                Q(author__in=authors) | Q(title__contains=kw) | Q(en_title__contains=kw) |
                Q(tags__contains=kw) | Q(content__contains=kw) | Q(carousel__in=carousels))

            uid = get_uid(request)
            navs = Nav.objects.all()
            data = {'uid': uid, 'navs': navs, 'kw': kw}
            if blogs:
                data['blogs'] = blogs
            return render(request, 'blog/search_article.html', context=data)
        else:
            uid = get_uid(request)
            navs = Nav.objects.all()
            kw = kw
            data = {'uid': uid, 'navs': navs, 'kw': kw}
            return render(request, 'blog/search_article.html', context=data)
