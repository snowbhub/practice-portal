from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):

    search_fields=('email',)

# admin.site.register(Profile)
admin.site.register(User,UserAdmin)