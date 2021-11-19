from django.contrib import admin
from .models import myUser

# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username','email','created_at')
    list_filter = ('created_at',)
    search_fields = ['email']

admin.site.register(myUser, MyUserAdmin)