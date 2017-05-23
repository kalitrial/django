from django.contrib import admin
from .models import Post, Comment

# Register your models here.
# admin.site.register(Post)

# customizing the way models are displayed

class PostAdmin(admin.ModelAdmin):

    #list_display allows you to set the fields of your model that you want to display in  the admin object list page
    list_display = ('title', 'slug', 'author', 'publish', 'status', )
    list_filter = ('status', 'created', 'publish', 'author',)

    search_fields = ('title', 'body', 'slug')
    prepopulated_fields = {'slug': ('title', )}

    raw_id_fields = ('author', )
    date_hierarchy = 'publish'

    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)