from django.shortcuts import redirect


# 判断有没有登陆
def get_uid(request):
    session_id = request.COOKIES.get('sessionid')
    if request.session.session_key == session_id:
        uid = request.session.get('user_id')
        return uid
    return None


# 判断有没有登陆的装饰器
def check_logined(func):
    def inner(request):
        uid = get_uid(request)
        if not uid:
            return redirect('/users/login_page/')
        else:
            res = func(request)
            return res
    return inner
