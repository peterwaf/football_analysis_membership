from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','image','slug','author','created_on','content','status','content_type','league')
    search_fields = ('title','league')
    list_filter = ("status",)
    prepopulated_fields = {'slug': ('title',)} #auto complete the slug field
admin.site.register(Post,PostAdmin)