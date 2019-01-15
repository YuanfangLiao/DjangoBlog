from django.shortcuts import redirect

# 判断有没有登陆
from blog.models import Nav, BlogPostModel
from society.models import Comment
from users.models import UserModel


def get_uid(request):
    session_id = request.COOKIES.get('sessionid')
    if request.session.session_key == session_id:
        uid = request.session.get('user_id')
        return uid
    return None


# 获取用户对象
def get_User_Model(request):
    session_id = request.COOKIES.get('sessionid')
    if request.session.session_key == session_id:
        uid = request.session.get('user_id')
        User = UserModel.objects.all().filter(user_id=uid).first()
        return User
    return None


# 判断有没有登陆的，只有登陆能进行操作的闭包（用于装饰器）
def check_logined(func):
    def inner(request, *args, **kwargs):
        uid = get_uid(request)
        if not uid:
            return redirect('/users/login_page/')
        else:
            res = func(request, *args, **kwargs)
            return res

    return inner


# 判断是不是管理员,只有管理员能进行操作的闭包（用于装饰器）
def only_admin_go(func):
    def inner(request, *args, **kwargs):
        user = get_User_Model(request)
        if user.user_is_admin == 0:
            return redirect('/users/go_personal_center/')
        else:
            res = func(request, *args, **kwargs)
            return res

    return inner


def get_biyaode_dict(request):
    uid = get_uid(request)
    user = get_User_Model(request)
    navs = Nav.objects.all()
    data = {}
    data['uid'] = uid
    data['user'] = user
    data['navs'] = navs
    return data


# 刷新博客评论数量 添加或删除
def refresh_blog_comment_num(blog_id, method='add'):
    blog = BlogPostModel.objects.filter(pk=blog_id).first()
    if method == 'add':
        blog.comment_num += 1
        blog.save()
    elif method == 'minus' and blog.comment_num >= 1:
        blog.comment_num -= 1
        blog.save()
    else:
        raise Exception('添加/减少评论次数操作不合法')


# 刷新所有的博客评论数量
def refresh_all_blog_comment_num():
    blogs = BlogPostModel.objects.all()
    for blog in blogs:
        num = Comment.objects.filter(comment_to_which_blog_id=blog.id).count()
        blog.comment_num = num
        blog.save()
