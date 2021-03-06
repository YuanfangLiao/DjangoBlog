from django.urls import path, include, re_path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post_new_blog', views.post_new_blog, name='post_new_blog'),
    path('do_post_new_blog', views.do_post_new_blog, name='do_post_new_blog'),
    path('del_blog', views.del_blog, name='del_blog'),
    path('recovery_blog', views.recovery_blog, name='recovery_blog'),
    path('blog_img_upload', views.blog_img_upload, name='blog_img_upload'),
    path('test', views.test, name='test'),
    path('edit_carousel', views.edit_carousel, name='edit_carousel'),
    path('edit_nav', views.edit_nav, name='edit_nav'),
    path('edit_swiper', views.edit_swiper, name='edit_swiper'),
    path('aboutme', views.aboutme, name='aboutme'),
    path('dianzan', views.dianzan, name='dianzan'),
    re_path(r'^edit_blog/', views.edit_blog, name='edit_blog'),
    re_path(r'^search/', views.search, name='search'),

    path('blog_detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('order_blog/<require_type>/<order_type>', views.order_blog, name='order_blog'),

    path('do_create_swiper', views.do_create_swiper, name='do_create_swiper')

]
