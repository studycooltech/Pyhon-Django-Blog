from django.contrib import admin
# App Model
from .models import Post, Category,Profile,Tags,Contact,Comment,SubComment,Banner


class PostAdmin(admin.ModelAdmin):
    """Customizing Admin Interface"""
    list_editable = ['draft']
    list_display_links = ['title']
    list_filter = ['updated', 'created']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title', 'category', 'published', 'updated', 'draft',
                    'image']


# Register the custom Admins
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Profile)
admin.site.register(Post, PostAdmin)

admin.site.register(Contact)
admin.site.register(Comment)
admin.site.register(SubComment)
admin.site.register(Banner)