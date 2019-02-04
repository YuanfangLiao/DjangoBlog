import base64
import os
import random
import logging
import uuid

import markdown
from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, ProtectedError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

# 加载主页
from DjBlog import settings
from DjBlog.settings import BASE_DIR
from blog.models import CarouselModel, BlogPostModel, Nav, Swipers
from society.models import Comment
from users.functions import check_logined, get_uid, only_admin_go, get_biyaode_dict
from users.models import UserModel
from users.functions import get_User_Model


def index(request):
    sessionid = request.COOKIES.get('sessionid')

    if request.session.session_key == sessionid:
        uid = request.session.get('user_id')
        user = UserModel.objects.filter(user_id=uid).first()
        data = {'uid': uid, 'user': user}

    else:
        data = {'uid': None}

    # 博客分类信息，按个数排名 文章信息，导航栏信息
    carouses = CarouselModel.objects.all().order_by('-total_number')
    all_blogs = BlogPostModel.objects.filter(status=0).order_by('-create_time')
    tags = []
    for blog in all_blogs:
        tags += blog.get_tags()
    # 去重
    tags = list(set(tags))
    navs = Nav.objects.all()
    paginator = Paginator(all_blogs, 6)
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

    # 加载轮播图
    swipers = Swipers.objects.all()

    if swipers:
        data['swipers'] = swipers

    data['carouses'] = carouses
    data['blogs'] = blogs
    data['navs'] = navs
    data['tags'] = tags
    data['now_page'] = now_page
    data['num_pages'] = paginator.num_pages
    data['which_page'] = 'index'

    response = render(request, 'index.html', data)
    return response


# 通过不同分类方式展现博客
def order_blog(request, require_type, order_type):
    sessionid = request.COOKIES.get('sessionid')

    if request.session.session_key == sessionid:
        uid = request.session.get('user_id')
        user = UserModel.objects.filter(user_id=uid).first()
        data = {'uid': uid, 'user': user}

    else:
        data = {'uid': None}

    # 博客分类信息，按个数排名 文章信息，导航栏信息
    carouses = CarouselModel.objects.all().order_by('-total_number')
    exactly_all_blogs = BlogPostModel.objects.all().filter(status=0)
    if require_type == 'default':
        all_blogs = BlogPostModel.objects.all().filter(status=0)
    else:
        all_blogs = BlogPostModel.objects.all().filter(status=0).filter(carousel_id=require_type)

    if order_type == 'zan':
        all_blogs.order_by('-zan_times')
    elif order_type == 'time':
        all_blogs.order_by('-create_time')
    elif order_type == 'views':
        all_blogs.order_by('-view_times')
    else:
        all_blogs.order_by('-create_time')

    tags = []
    for blog in exactly_all_blogs:
        tags += blog.get_tags()
    # 去重
    tags = list(set(tags))
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

    data['carouses'] = carouses
    data['blogs'] = blogs
    data['navs'] = navs
    data['tags'] = tags
    data['now_page'] = now_page
    data['num_pages'] = paginator.num_pages
    data['require_type'] = require_type
    data['order_type'] = order_type
    data['which_page'] = 'all_blog'

    return render(request, 'blog/order_blog.html', data)


def blog_detail(request, blog_id):
    if request.method == 'GET':
        # 导航
        navs = Nav.objects.all()
        user = get_User_Model(request)
        # 博客
        blog = BlogPostModel.objects.all().filter(pk=blog_id).first()
        blog.view_times = blog.view_times + 1
        blog.save()

        # 加载博客评论
        comments = Comment.objects.filter(comment_to_which_blog=blog).order_by('comment_time')

        data = {}
        tags = blog.get_tags()
        data['comments'] = comments
        data['navs'] = navs
        data['blog'] = blog
        data['user'] = user
        data['tags'] = tags
        if user:
            if user.user_img:
                imgUrl = '/static/upload/' + user.user_img.url
                data['imgUrl'] = imgUrl
        print(blog.update_time)
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


@only_admin_go
@check_logined
def post_new_blog(request):
    # 获取所有分类数据
    carousels = CarouselModel.objects.all()

    uid = get_uid(request)
    navs = Nav.objects.all()

    data = {}
    # data['post'] = post
    data['uid'] = uid
    data['carousels'] = carousels
    data['navs'] = navs
    return render(request, 'blog/post_new_blog.html', context=data)


@only_admin_go
@check_logined
def edit_blog(request):
    if request.method == "GET":
        blog_id = request.GET.get('blog_id')
        blog = BlogPostModel.objects.filter(id=blog_id).first()
        uid = get_uid(request)
        user = get_User_Model(request)
        data = {}
        data['uid'] = uid
        data['user'] = user
        data['blog'] = blog
        data['navs'] = Nav.objects.all()
        carousels = CarouselModel.objects.all()
        data['carousels'] = carousels
        return render(request, 'blog/edit_blog.html', context=data)


# 删除博客
@check_logined
def del_blog(request):
    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        my_method = request.POST.get('del_method')
        blog = BlogPostModel.objects.filter(id=blog_id).first()
        # 如果是完全删除，就改为3 彻底删除
        print(my_method)
        if my_method == "true":
            blog.status = 3
        else:
            blog.status = 2

        try:
            blog.save()
            carousel = CarouselModel.objects.all().filter(pk=blog.carousel_id).first()
            carousel.total_number = BlogPostModel.objects.filter(carousel_id=carousel.title).filter(status=0).count()
            return JsonResponse({'code': 200})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})


# 恢复博客
@only_admin_go
@check_logined
def recovery_blog(request):
    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        blog = BlogPostModel.objects.filter(id=blog_id).first()
        blog.status = 0
        try:
            blog.save()
            carousel = CarouselModel.objects.all().filter(pk=blog.carousel_id).first()
            carousel.total_number = BlogPostModel.objects.filter(carousel_id=carousel.title).filter(status=0).count()
            return JsonResponse({'code': 200})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': str(e)})


# 发布博文
@only_admin_go
@check_logined
def do_post_new_blog(request):
    if request.method == "POST":

        blog_title = request.POST.get('blog_title')
        eng_title = request.POST.get('eng_title')
        blog_content = request.POST.get('blog_content')
        blog_tags = request.POST.get('blog_tags')
        blog_carousel = request.POST.get('blog_carousel')
        post_or_draft = request.POST.get('post_or_draft')
        # 如果是编辑博客
        if request.POST.get('blog_id'):
            blog_id = request.POST.get('blog_id')
            blog = BlogPostModel.objects.filter(pk=blog_id).first()
            old_carousel = blog.carousel_id
            blog.title = blog_title
            blog.content = blog_content
            blog.tags = blog_tags
            blog.carousel_id = blog_carousel
            # 如果仍然存入草稿箱
            if post_or_draft == '存入草稿':
                blog.status = 1
            else:
                blog.status = 0
            summmary = ''.join(blog_content.split())
            # 如果文字长度大于30，摘要为前30个字，如果小于30，就为文章本身
            if len(summmary) >= 100:
                blog.summary = summmary[:100]
            else:
                blog.summary = summmary
            # 如果有英文标题
            if eng_title:
                blog.en_title = eng_title
            try:
                blog.save()
                # 刷新分类数据
                carousel_count_old = BlogPostModel.objects.filter(carousel_id=old_carousel).filter(status=0).count()
                carouse_old = CarouselModel.objects.filter(pk=old_carousel).first()
                carouse_old.total_number = carousel_count_old
                carouse_old.save()
                carousel_count = BlogPostModel.objects.filter(carousel_id=blog_carousel).filter(status=0).count()
                carouse = CarouselModel.objects.filter(pk=blog_carousel).first()
                carouse.total_number = carousel_count
                carouse.save()
                return JsonResponse({'code': 200})
            except Exception as e:
                print('服务器错误', str(e))
                return JsonResponse({'code': 501, 'msg': str(e)})

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

        if post_or_draft == '存入草稿':
            new_blog.status = 1

        try:
            new_blog.save()
            carousel_count = BlogPostModel.objects.filter(carousel_id=blog_carousel).filter(status=0).count()
            carouse = CarouselModel.objects.filter(pk=blog_carousel).first()
            carouse.total_number = carousel_count
            carouse.save()
            return JsonResponse({'code': 200})
        except Exception as e:
            print('服务器错误', str(e))
            return JsonResponse({'code': 501, 'msg': str(e)})


# 写博客上传图片
@only_admin_go
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


# 搜索函数
def search(request):
    if request.method == "GET":
        kw = request.GET['kw']
        # 请求为空返回空
        if kw:
            # 先尝试获取有没有搜到名字一样的author
            authors = UserModel.objects.filter(user_id__contains=kw)
            carousels = CarouselModel.objects.filter(title__contains=kw)
            # 找到任意一个内容里面有要搜索内容的blog
            blogs = BlogPostModel.objects.filter(status=0).filter(
                Q(author__in=authors) | Q(title__contains=kw) | Q(en_title__contains=kw) |
                Q(tags__contains=kw) | Q(content__contains=kw) | Q(carousel__in=carousels))

            uid = get_uid(request)
            navs = Nav.objects.all()
            data = {'uid': uid, 'navs': navs, 'kw': kw}
            if blogs:
                # 分页操作暂缓开放
                # paginator = Paginator(blogs, 6)
                # page = request.GET.get('page')
                # try:
                #     blogs = paginator.page(page)
                #     now_page = page
                # except PageNotAnInteger:
                #     blogs = paginator.page(1)
                #     now_page = 1
                # except EmptyPage:
                #     blogs = paginator.page(paginator.num_pages)
                #     now_page = paginator.num_pages
                data['blogs'] = blogs
            return render(request, 'blog/search_article.html', context=data)
        else:
            uid = get_uid(request)
            navs = Nav.objects.all()
            kw = kw
            data = {'uid': uid, 'navs': navs, 'kw': kw}
            return render(request, 'blog/search_article.html', context=data)


# 管理分类信息的函数
@check_logined
def edit_carousel(request):
    if request.method == "POST":
        edit_method = request.POST.get('edit_method')
        if edit_method == 'add':
            carousel_name = request.POST.get('carousel_name')
            carousel_summary = request.POST.get('carousel_summary')
            new_carousel = CarouselModel()
            new_carousel.title = carousel_name
            new_carousel.summary = carousel_summary
            try:
                new_carousel.save()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})
        if edit_method == 'edit_title':
            old_title = request.POST.get('old_title')
            new_title = request.POST.get('new_title')

            # 先实现一个新的分类
            new_carousel = CarouselModel()
            old_carousel = CarouselModel.objects.filter(pk=old_title).first()
            new_carousel.title = new_title
            new_carousel.summary = old_carousel.summary
            new_carousel.total_number = old_carousel.total_number
            new_carousel.create_time = old_carousel.create_time

            try:
                new_carousel.save()
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})

            # 找到所有旧的博客
            all_blogs_with_old_carousel = BlogPostModel.objects.filter(carousel_id=old_carousel)
            for blog in all_blogs_with_old_carousel:
                blog.carousel_id = new_title

                try:
                    blog.save()
                except Exception as e:
                    print(e)
                    return JsonResponse({'code': 500})

            # 删除旧的标题
            try:
                old_carousel.delete()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})
        if edit_method == 'edit_summary':
            old_title = request.POST.get('old_title')
            new_summary = request.POST.get('new_summary')
            carousel = CarouselModel.objects.filter(pk=old_title).first()
            carousel.summary = new_summary
            try:
                carousel.save()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})
        if edit_method == 'del':
            title = request.POST.get('title')
            carousel = CarouselModel.objects.filter(pk=title).first()

            try:
                carousel.delete()
                return JsonResponse({'code': 200})
            except ProtectedError as e:
                print('外键保护')
                return JsonResponse({'code': 501, 'msg': '请不要删除仍然有博客的分类'})
            except Exception as e:
                print(str(e))
                return JsonResponse({'code': 500, 'msg': '服务器错误'})


@check_logined
def edit_nav(request):
    if request.method == "POST":
        edit_method = request.POST.get('edit_method')
        if edit_method == 'add':
            nav_name = request.POST.get('nav_name')
            nav_url = request.POST.get('nav_url')
            new_nav = Nav()
            new_nav.name = nav_name
            new_nav.url = nav_url
            try:
                new_nav.save()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})
        if edit_method == 'del':
            nav_id = request.POST.get('id')
            nav = Nav.objects.filter(pk=nav_id).first()
            try:
                nav.delete()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(str(e))
                return JsonResponse({'code': 500, 'msg': '服务器错误'})
        if edit_method == 'edit_url':
            nav_id = request.POST.get('id')
            nav = Nav.objects.filter(pk=nav_id).first()
            new_url = request.POST.get('new_url')
            nav.url = new_url
            try:
                nav.save()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})
        if edit_method == 'edit_name':
            nav_id = request.POST.get('id')
            nav = Nav.objects.filter(pk=nav_id).first()
            new_name = request.POST.get('new_name')
            nav.name = new_name
            try:
                nav.save()
                return JsonResponse({'code': 200})
            except Exception as e:
                print(e)
                return JsonResponse({'code': 500})


def aboutme(request):
    data = get_biyaode_dict(request)

    return render(request, 'blog/aboutme.html', data)


def dianzan(request):
    blog_id = request.GET.get('blog_id')
    blog = BlogPostModel.objects.all().filter(pk=blog_id).first()
    # blog = BlogPostModel()
    zan_times = blog.zan_times
    zan_times += 1
    data = {}
    try:
        blog.zan_times = zan_times
        blog.save()
        data['code'] = 200
        data['zan_times'] = zan_times
        return JsonResponse(data)
    except Exception as e:
        print(str(e))
        data['code'] = 500
        return JsonResponse(data)


def do_create_swiper(request):
    # 本地保存头像
    data = request.POST['tx']
    if not data:
        return HttpResponse(u"上传轮播图错误，图片为空", status=500)

    imgData = base64.b64decode(data)
    filename = "swiper_1024x576_{}.png".format(uuid.uuid4())
    static_root = getattr(settings, 'STATIC_ROOT', None)
    filedir = os.path.join(static_root, 'upload/swipers')

    print(filedir)
    path = os.path.join(filedir, filename)

    file = open(path, "wb+")
    file.write(imgData)
    file.flush()
    file.close()

    # 修改头像分辨率
    im = Image.open(path)
    out = im.resize((1024, 576), Image.ANTIALIAS)
    try:
        out.save(path)
        swiper = Swipers()
        swiper.swiper_img_url = '/static/upload/swipers/' + filename
        swiper.save()
    except Exception as e:
        print(e)
        return HttpResponse(u"上传轮播图失败!\n错误代码:" + str(e))

    return HttpResponse(u"上传轮播图成功!刷新页面\n可能会有缓存！")


def edit_swiper(request):
    if request.method == "POST":
        method = request.POST.get('method')
        data = {}
        if method == 'edit':
            swiper_id = request.POST.get('swiper_id')
            swiper_title = request.POST.get('swiper_title')
            swiper_url = request.POST.get('swiper_url')
            # 如果title或url有值的变化，就修改，否则退出
            if swiper_title or swiper_url:
                swiper = Swipers.objects.all().filter(pk=swiper_id).first()
                if swiper_title:
                    swiper.swiper_title = swiper_title
                if swiper_url:
                    swiper.swiper_url = swiper_url
                try:
                    swiper.save()
                    data['code'] = 200
                    data['msg'] = '保存成功'
                    return JsonResponse(data)
                except Exception as e:
                    print(str(e))
                    data['code'] = 500
                    data['msg'] = '数据库保存失败'
                    return JsonResponse(data)
            else:
                data['code'] = 200
                data['msg'] = '没有任何修改'
                return JsonResponse(data)
        elif method == 'del':
            swiper_id = request.POST.get('swiper_id')
            swiper = Swipers.objects.all().filter(pk=swiper_id).first()
            img_url = swiper.swiper_img_url
            real_url = BASE_DIR + img_url
            print(real_url)
            if real_url:
                os.remove(real_url)
            try:
                swiper.delete()
                data['code'] = 200
                data['msg'] = '删除成功'
                return JsonResponse(data)
            except Exception as e:
                print(str(e))
                data['code'] = 500
                data['msg'] = '数据库删除失败'
                return JsonResponse(data)
