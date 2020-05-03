from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','image','slug','author','created_on','content','status')
    

admin.site.register(Post,PostAdmin)