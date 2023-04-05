from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from catalog.models import User, Director, Country, Film

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(Director, ModelAdmin)
admin.site.register(Country, ModelAdmin)
admin.site.register(Film, ModelAdmin)
