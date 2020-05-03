from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','image','slug','author','created_on','content','status',)
    search_fields = ('title',)

admin.site.register(Post,PostAdmin)