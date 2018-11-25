from django.urls import path, include, re_path

from society import views

app_name = 'society'

urlpatterns = [
    path('add_comment_to_blog/', views.add_comment_to_blog, name='add_comment_to_blog'),
    path('del_comment/<int:comment_id>', views.del_comment, name='del_comment'),
    path('ajax_del_comment', views.ajax_del_comment, name='ajax_del_comment'),
    path('ajax_yidu_comment', views.ajax_yidu_comment, name='ajax_yidu_comment'),
    path('ajax_weidu_comment', views.ajax_weidu_comment, name='ajax_weidu_comment'),
]
