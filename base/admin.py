from django.contrib import admin
from .models import *
# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'password']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Listing._meta.fields
        if field.name != "description"
    ]