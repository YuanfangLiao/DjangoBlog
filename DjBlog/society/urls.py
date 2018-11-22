from django.urls import path, include, re_path

from society import views

app_name = 'society'

urlpatterns = [
    path('add_comment_to_blog/', views.add_comment_to_blog, name='add_comment_to_blog'),
    path('add_comment_to_blog/', views.add_comment_to_comment, name='add_comment_to_comment'),
]
