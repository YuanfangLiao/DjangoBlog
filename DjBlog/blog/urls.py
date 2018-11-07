from django.urls import path, include, re_path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post_new_blog', views.post_new_blog, name='post_new_blog'),
    path('do_post_new_blog', views.do_post_new_blog, name='do_post_new_blog'),
    path('blog_img_upload', views.blog_img_upload, name='blog_img_upload'),
    path('test', views.test, name='test'),
    path('changetx', views.changetx, name='changetx'),
    re_path(r'^search/', views.search, name='search'),

    path('blog_detail/<int:blog_id>', views.blog_detail, name='blog_detail')

]
