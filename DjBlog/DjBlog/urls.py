from django.conf.urls import url, handler404, handler500, handler403
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import blog.views
from django.views import static
from DjBlog import settings
from blog import urls as blog_url
from users import urls as users_url
from society import urls as society_url
from users.views import page_not_found, page_error, permission_denied

handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog.views.index),
    path('blog/', include((blog_url, 'blog'), namespace='blog')),
    path('users/', include((users_url, 'users'), namespace='users')),
    path('society/', include((society_url, 'users'), namespace='society')),

    # 增加以下一行，以识别静态资源
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),

]
