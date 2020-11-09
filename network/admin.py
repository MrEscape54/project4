from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from network.models import User, Profile, Post

admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']

admin.site.register(Post)