from django.contrib import admin
from .models import ProfileModel, CommentsModel, ContactMessagesModel


# Register your models here.

@admin.register(ProfileModel)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'language', 'language_level', 'age')
    list_filter = ['language', 'language_level', 'age']


@admin.register(CommentsModel)
class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'create_date', 'approved')
    list_filter = ('approved', 'create_date')
    search_fields = ('user', 'comment')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(ContactMessagesModel)
class ContactMessagesModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message', 'create_date', 'replied')
    list_filter = ('replied', 'create_date')
    actions = ['reply_to_message']

    def reply_to_message(self, request, queryset):
        queryset.update(replied=True)