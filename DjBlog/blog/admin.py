from django.contrib import admin

# Register your models here.
# admin.site.register()
from blog.models import Nav, CarouselModel, BlogPostModel

admin.site.register(Nav)
admin.site.register(CarouselModel)
admin.site.register(BlogPostModel)