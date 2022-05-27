from django.contrib import admin
from .models import ProfileModel
# Register your models here.


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'language', 'language_level', 'age')
    list_filter = ['language', 'language_level', 'age']




admin.site.register(ProfileModel, ProfileModelAdmin)
