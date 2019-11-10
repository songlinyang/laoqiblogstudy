from django.contrib import admin
from .models import UserProfile,UserInfo


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","phone",)
    list_filter = ("user",)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user","school","company","profession","address","aboutme","photo")
    list_filter = ("school","company","profession")


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserInfo,UserInfoAdmin)