from django.db import models


# Create your models here.


class UserModel(models.Model):
    user_id = models.CharField(primary_key=True, max_length=32)
    user_passwd = models.CharField(max_length=32, null=False)
    user_phone = models.CharField(max_length=11, unique=True, null=True)
    user_email = models.CharField(max_length=64, unique=True)
    user_sex = models.BooleanField(default=1)
    user_img = models.ImageField(upload_to='users', null=True)
    user_is_admin = models.BooleanField(default=0)

    class Meta:
        db_table = 'djblog_user'
