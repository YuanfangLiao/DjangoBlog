"""
Django settings for DjBlog project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2wkpsk_@xes&+vz#ww_^f+2&la78*72%41h!^o9y)4d7cgbeza'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'DjBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DjBlog',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# 设置usermodel
USER_MODEL = 'users.UserModel'

# login页面
LOGIN_URL = '/users/login_page/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')

# 静态资源路径
STATICFILES_DIRS = [
    ("css", os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
    ("js", os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ("img", os.path.join(STATIC_ROOT, 'img').replace('\\', '/')),
    ("fonts", os.path.join(STATIC_ROOT, 'fonts').replace('\\', '/')),
    ("plugins", os.path.join(STATIC_ROOT, 'plugins').replace('\\', '/')),
    ("upload", os.path.join(STATIC_ROOT, 'upload').replace('\\', '/')),
    ("blogimg", os.path.join(STATIC_ROOT, 'upload/blogimg').replace('\\', '/')),
]

# 文件上传路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/upload')
# MEDIA_URL = '/static/'

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# 邮箱设置
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'djblog_admin@163.com'  # 帐号
EMAIL_HOST_PASSWORD = 'Qazwsxedc1'  # 密码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
