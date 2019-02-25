from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posed')
    list_filter = ('date_posed', 'author')


admin.site.register(Post, PostAdmin)


