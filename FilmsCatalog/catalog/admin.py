from django.contrib import admin
from django.contrib.admin import ModelAdmin
from catalog.models import User, Director, Country, Film

# Register your models here.

admin.site.register(User, ModelAdmin)
admin.site.register(Director, ModelAdmin)
admin.site.register(Country, ModelAdmin)
admin.site.register(Film, ModelAdmin)
