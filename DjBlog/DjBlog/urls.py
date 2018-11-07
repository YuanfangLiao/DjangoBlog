"""DjBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import blog.views
from django.views import static
from DjBlog import settings
from blog import urls as blog_url
from users import urls as users_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog.views.index),
    path('blog/', include((blog_url, 'blog'), namespace='blog')),
    path('users/', include((users_url, 'users'), namespace='users')),

    # 增加以下一行，以识别静态资源
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')

]
