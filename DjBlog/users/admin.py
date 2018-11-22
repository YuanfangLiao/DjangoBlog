from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group, User

from users.models import UserModel

admin.site.register(UserModel)
admin.site.unregister(Group)
admin.site.unregister(User)

# import xadmin
# from xadmin import views
#
#
# class BaseSettings(object):
#     enable_themes = True  # 使用主题功能
#     use_bootswatch = True
#
#
# xadmin.site.register(views.BaseAdminView, BaseSettings)
