import base64
import hashlib
import io
import logging
import os
import random
import re

from PIL import Image, ImageDraw, ImageFont
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from DjBlog import settings
from blog.models import Nav, BlogPostModel, CarouselModel, Swipers
from society.models import Comment
from users.functions import get_uid, check_logined, get_biyaode_dict, get_User_Model
from users.models import UserModel
from users.sendEmail import EmailSender

logger = logging.getLogger(__name__)


def permission_denied(request, exception):
    data = get_biyaode_dict(request)
    return render(request, '403.html', context=data)


def page_not_found(request, exception):
    data = get_biyaode_dict(request)
    return render(request, '404.html', context=data)


def page_error(request):
    data = get_biyaode_dict(request)
    return render(request, '500.html', context=data)


# 去注册界面
def go_register_page(request):
    return render(request, 'users/register_page.html',context={
        'navs': Nav.objects.all(),
    })


# 注册
def do_register(request):
    new_user_id = request.POST.get('user_id')
    new_user_passwd = request.POST.get('user_passwd')
    new_user_email = request.POST.get('user_email')
    new_user_sex = request.POST.get('user_sex')

    new_user = UserModel()
    new_user.user_id = new_user_id

    # 创建一个MD5对象
    MD5 = hashlib.md5()
    # 将一个二进制数据进行md5处理，生成一个128位的二进制数据
    MD5.update(new_user_passwd.encode('utf-8'))
    # 转换为32位18进制，赋值给密码
    new_user_passwd = MD5.hexdigest()
    new_user.user_passwd = new_user_passwd
    new_user.user_email = new_user_email
    new_user.user_sex = new_user_sex
    new_user.user_img = "users/favicon.png"

    try:
        new_user.save()
        return HttpResponse('success')

    except Exception as ex:
        print('Error while create user' + str(ex))
        return HttpResponse('error' + str(ex))


# 检查用户是否存在
def check_user_exist(request):
    user_id = request.POST.get('user_id')

    user_exist = UserModel.objects.filter(user_id=user_id)
    # 如果用户存在
    if user_exist:
        return HttpResponse("exist")
    return HttpResponse(user_id)


# 检查email是否存在
def check_email_exist(request):
    user_email = request.POST.get('user_email')

    user_exist = UserModel.objects.filter(user_email=user_email)
    # 如果用户存在
    if user_exist:
        return HttpResponse("exist")
    return HttpResponse(user_email)


# 去登陆界面
def go_login_page(request):
    sessionID = request.COOKIES.get('sessionID')
    print(sessionID)
    if request.session.exists(sessionID):
        uid = request.session.get('user_id')

        return render(request, 'users/login_page.html', context={
            'uid': uid,
            'navs': Nav.objects.all(),
        })
    else:
        return render(request, 'users/login_page.html', context={
            'navs': Nav.objects.all(),
        })


# 登陆操作
def do_login(request):
    # 准备数据

    your_user_id = request.POST.get('user_id')
    your_user_passwd = request.POST.get('user_passwd')
    your_verificaiton_code = request.POST.get('your_verificaiton_code')
    # 先验证验证码
    true_verificaiton_code = request.session.get('verCode')
    if not your_verificaiton_code.lower() == true_verificaiton_code.lower():
        return HttpResponse('验证码错误')

    # 查询有没有这个用户名的用户，没有的话返回用户名错误
    rel_user = UserModel.objects.all().filter(user_id=your_user_id).first()
    if not rel_user:
        return HttpResponse("没有该用户")

    # 检验密码啦
    MD5 = hashlib.md5()
    MD5.update(your_user_passwd.encode('utf-8'))
    your_user_passwd = MD5.hexdigest()
    if not your_user_passwd == rel_user.user_passwd:
        return HttpResponse("密码错误，请重试")

    # 走到这里验证成功了，开始存session
    request.session['user_id'] = rel_user.user_id
    request.session['user_passwd'] = rel_user.user_passwd
    # 设置session过期时间 一天后过期60 * 60 * 24
    request.session.set_expiry(60 * 60 * 24)

    # 把sessionid存到cookie中
    response = HttpResponse('success')
    # response.set_cookie('sessionID', request.session.session_key, expires=60 * 60 * 24)

    return response


# 生成验证码
def get_verification_code(request):
    # 创建一个画布
    # model 画布模式，'RGB'
    # size
    image = Image.new('RGB', (160, 70), color=create_color())

    # 创建一个画笔
    image_draw = ImageDraw.Draw(image, 'RGB')

    image_font = ImageFont.truetype(
        'static/fonts/' + random.choice(['ADOBEARABIC-BOLD.OTF', 'ADOBEARABIC-BOLDITALIC.OTF',
                                         'ADOBEARABIC-ITALIC.OTF', 'ADOBEARABIC-REGULAR.OTF']), size=50)

    # 画
    # xy,画的起始位置（坐标）
    # text 画的内容
    # fill = None，
    # font = None，
    char_source = '123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    verCode = ''
    for i in range(4):
        # 随机选一个字母
        ch = random.choice(char_source)
        image_draw.text((20 + (i * 30), 10), ch, font=image_font, fill=create_color())
        verCode += ch

    # 服务器session中保存一份验证码
    request.session['verCode'] = verCode
    # 设置过期时间 单位秒
    request.session.set_expiry(60)

    # 给验证码图片画一些点，使其模糊
    for i in range(2000):
        x = random.randrange(0, 160)
        y = random.randrange(0, 70)
        image_draw.point((x, y), fill=create_color())

    # 创建一个字节流
    byteIO = io.BytesIO()

    # 把图片保存到字节流中去
    image.save(byteIO, 'png')

    return HttpResponse(byteIO.getvalue(), 'image/png')


# 生成一个随机色
def create_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return (red, green, blue)


# 去用户中心
# @login_required
@check_logined
def go_personal_center(request):
    uid = get_uid(request)
    user = get_User_Model(request)
    navs = Nav.objects.all()

    all_my_posted_comments = Comment.objects.filter(comment_creater=user)
    all_my_blogs = BlogPostModel.objects.all().filter(author=user)
    my_comments_num = Comment.objects.all().filter(comment_is_not_read=True). \
        filter(Q(comment_to_which_Comment__in=all_my_posted_comments) |
               Q(comment_to_which_blog__in=all_my_blogs)).count()
    data = {
        'uid': uid,
        'user': user,
        'navs': navs,
        'my_comments_num': my_comments_num
    }
    if user.user_img:
        imgUrl = '/static/upload/' + user.user_img.url
        data['imgUrl'] = imgUrl

    return render(request, 'users/base_personal_center.html', data)


# 登出
def do_log_out(request):
    response = redirect(reverse('blog:index'))
    response.delete_cookie('sessionid')
    request.session.flush()

    return response


# 用于管理用户中心中去到不同页面
def go_user_center_somewhere(request, somewhere1, somewhere2=''):
    user = get_User_Model(request)

    data = {"user": user, }
    return render(request, 'users/' + somewhere1 + '/' + somewhere2, context=data)


# 管理文章
@check_logined
def manage_article(request):
    if request.method == "GET":
        user = get_User_Model(request)
        where = request.GET.get('where')
        # 判断文章状态
        if where == 'deleted':
            blogs = BlogPostModel.objects.filter(status=2).filter(author=user).order_by('-create_time')
        elif where == 'drafts':
            blogs = BlogPostModel.objects.filter(status=1).filter(author=user).order_by('-create_time')
        else:
            blogs = BlogPostModel.objects.filter(status=0).filter(author=user).order_by('-create_time')

        data = {"user": user,
                'blogs': blogs
                }
        return render(request, 'users/manage_article.html', context=data)


# 进行修改头像操作
@check_logined
def do_change_img(request):
    user = get_User_Model(request)

    # 本地保存头像
    data = request.POST['tx']
    if not data:
        logger.error(
            u'[UserControl]轮播图上传头像为空:[%s]'.format(
                request.user.username
            )
        )
        return HttpResponse(u"上传头像错误，图片为空", status=500)

    imgData = base64.b64decode(data)
    filename = "tx_100x100_{}.png".format(user.user_id)
    static_root = getattr(settings, 'STATIC_ROOT', None)
    filedir = os.path.join(static_root, 'upload/users')

    print(filedir)
    path = os.path.join(filedir, filename)

    file = open(path, "wb+")
    file.write(imgData)
    file.flush()
    file.close()

    # 修改头像分辨率
    im = Image.open(path)
    out = im.resize((100, 100), Image.ANTIALIAS)
    try:
        out.save(path)
        user.user_img = 'users/' + filename
        user.save()
    except Exception as e:
        print(e)
        return HttpResponse(u"上传头像失败!\n错误代码:" + str(e))

    return HttpResponse(u"上传头像成功!刷新页面\n可能会有缓存！")


# 进行修改性别操作
@check_logined
def do_change_sex(request):
    user = get_User_Model(request)
    sex = int(request.POST.get('sex'))
    user.user_sex = sex
    user.save()
    return JsonResponse({'code': 200})


# 进行修改邮箱操作
@check_logined
def do_change_email(request):
    # 获得正确的验证码
    true_verification_code = request.COOKIES.get('email_sender_verification_code')
    your_verification_code = request.POST.get('verification_code')
    your_new_email = request.POST.get('user_email')
    print(true_verification_code)
    if true_verification_code != your_verification_code:
        return JsonResponse({'code': 403, 'message': '验证码错误'})
    user = get_User_Model(request)
    if not user:
        # 服务器出现问题，如session错误
        return JsonResponse({'code': 500, 'message': '用户未登录或者服务器出现了问题'})
    user.user_email = your_new_email
    user.save()
    return JsonResponse({'code': 200, 'message': '修改邮箱成功'})


# 进行修改密码操作
@check_logined
def do_change_password(request):
    user = get_User_Model(request)

    old_user_passwd = request.POST.get('old_user_passwd')
    user_passwd = request.POST.get('user_passwd')
    confirm_passwd = request.POST.get('confirm_passwd')
    # 验证密码合法性
    if not re.match('^[a-zA-Z0-9_\.]{6,31}$', user_passwd):
        return JsonResponse({'code': 403, 'message': '密码只能包含字母、数字、下划线和点、长度为6-30个字符'})

    # 检验密码啦
    MD5 = hashlib.md5()
    MD5.update(old_user_passwd.encode('utf-8'))
    old_user_passwd = MD5.hexdigest()
    MD5_1 = hashlib.md5()
    MD5_1.update(user_passwd.encode('utf-8'))
    user_passwd = MD5_1.hexdigest()
    MD5_2 = hashlib.md5()
    MD5_2.update(confirm_passwd.encode('utf-8'))
    confirm_passwd = MD5_2.hexdigest()

    if user:
        # 验证旧密码是否正确
        if user.user_passwd == old_user_passwd:

            # 再次验证两次验证码是不是一样的
            if user_passwd == confirm_passwd:
                # 如果和原密码相同返回更改失败
                if user_passwd == user.user_passwd:
                    return JsonResponse({'code': 403, 'message': '请输入和原密码不一样的新密码'})

                # 拦截数据库错误
                try:
                    user.user_passwd = user_passwd
                    user.save()
                except Exception as ex:
                    print('ERROR:' + str(ex))
                    return JsonResponse({'code': 500, 'message': '数据库错误' + str(ex)})
                return JsonResponse({'code': 200, 'message': '更换密码成功'})
            else:
                # 两次输入的密码不一样
                return JsonResponse({'code': 403, 'message': '两次密码输入不一样，请输入两次相同的新密码'})
        else:
            # 身份验证错误
            return JsonResponse({'code': 401, 'message': '用户密码错误'})
    else:
        # 服务器出现问题，如session错误
        return JsonResponse({'code': 500, 'message': '用户未登录或者服务器出现了问题'})


@check_logined
def go_my_comment(request):
    user = get_User_Model(request)
    data = {"user": user}
    my_comments = Comment.objects.filter(comment_creater=user).order_by('-comment_time')
    all_comments = Comment.objects.all()
    data['my_comments'] = my_comments
    data['all_comments'] = all_comments
    return render(request, 'users/my_comment.html', context=data)


@check_logined
def go_my_message(request):
    user = get_User_Model(request)
    data = {"user": user}
    # 这里要的是未读信息
    all_my_posted_comments = Comment.objects.all().filter(comment_creater=user)
    all_my_blogs = BlogPostModel.objects.all().filter(author=user)
    my_comments = Comment.objects.all(). \
        filter(Q(comment_to_which_Comment__in=all_my_posted_comments) |
               Q(comment_to_which_blog__in=all_my_blogs)). \
        order_by('-comment_time')
    all_comments = Comment.objects.all()
    data['my_comments'] = my_comments
    data['all_comments'] = all_comments
    return render(request, 'users/my_message.html', context=data)


# 用于发送邮箱验证码
def do_send_email_verification_code(request):
    your_email = request.POST.get('your_email_address')
    # print(your_email)
    # 初始化邮件发送器对象
    email_sender = EmailSender(your_email)
    # 生成的验证码
    email_sender_verification_code = email_sender.get_verification_code()

    try:
        email_sender.send_emails()
        response = JsonResponse({'code': '200'})
        # 保存生成的验证码到cookie里,15分钟过期
        response.set_cookie('email_sender_verification_code', email_sender_verification_code, expires=60 * 15)
        print(email_sender_verification_code)
        return response

    except Exception as ex:
        print('error' + str(ex))
        return JsonResponse({'code': '501', 'msg': '发送邮件错误'})


# 管理分类表
@check_logined
def manage_carousel(request):
    carousels = CarouselModel.objects.all().order_by('total_number')
    data = {}
    data['carousels'] = carousels
    return render(request, 'users/manage_carousel.html', context=data)


@check_logined
def manage_nav(request):
    navs = Nav.objects.all().order_by('name')
    data = {}
    data['navs'] = navs
    return render(request, 'users/manage_nav.html', context=data)


@check_logined
def manage_swiper(request):
    swipers = Swipers.objects.all()
    data = {}
    data['swipers'] = swipers
    return render(request, 'users/manage_swiper.html', context=data)
