from django.urls import path, include, re_path

from users import views

app_name = 'users'
urlpatterns = [
    path('register_page/', views.go_register_page, name='go_register_page'),
    path('login_page/', views.go_login_page, name='go_login_page'),
    path('do_register/', views.do_register, name='do_register'),
    path('do_login/', views.do_login, name='do_login'),
    path('do_log_out/', views.do_log_out, name='do_log_out'),
    path('check_user_exist/', views.check_user_exist, name='check_user_exist'),
    path('check_email_exist/', views.check_email_exist, name='check_email_exist'),
    path('go_personal_center/', views.go_personal_center, name='go_personal_center'),
    path('manage_article/', views.manage_article, name='manage_blog'),

    # 正则匹配
    re_path(r'^get_verification_code/', views.get_verification_code, name='get_verification_code'),

    # 下面是个人中心界面的路由
    # 用于去到个人中心不同的页面
    path('go_user_center_somewhere/<str:somewhere1>/', views.go_user_center_somewhere, name='go_user_center_somewhere'),
    path('go_user_center_somewhere/<str:somewhere1>/<str:somewhere2>/', views.go_user_center_somewhere, name='go_user_center_somewhere2'),

    path('do_change_img/', views.do_change_img, name='do_change_img'),
    path('do_change_password/', views.do_change_password, name='do_change_password'),
    path('do_change_email/', views.do_change_email, name='do_change_email'),
    path('do_change_sex/', views.do_change_sex, name='do_change_sex'),

    path('go_my_comment/', views.go_my_comment, name='go_my_comment'),

    path('go_my_message/', views.go_my_message, name='go_my_message'),
    # 发送邮箱验证码
    path('do_send_email_verification_code/', views.do_send_email_verification_code, name='do_send_email_verification_code'),


]
