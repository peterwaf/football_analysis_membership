from django.contrib import admin
from .models import Leaguetype
# Register your models here.
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league',)
    search_fields = ('league',)

admin.site.register(Leaguetype,LeagueAdmin)
