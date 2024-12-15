from django.contrib import admin
from .models import Category, SubCategory, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ['name', 'category__name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory')
    search_fields = ['name', 'category__name']
    list_filter = ('category', 'subcategory')

    def has_module_permission(self, request):
        """Allow only superusers to see the admin module."""
        return request.user.is_superuser
