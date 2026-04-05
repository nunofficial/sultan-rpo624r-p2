from django.contrib import admin
from .models import Category, City, Ad, Favorite, Banner, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'city', 'price', 'is_moderated', 'created_at')
    list_editable = ('is_moderated',)
    list_filter = ('is_moderated', 'category', 'city', 'is_top')
    search_fields = ('title', 'author__username', 'description')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'link')
    list_editable = ('is_active',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ad', 'author', 'rating', 'created_at')
    list_filter = ('rating',)