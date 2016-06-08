from django.contrib import admin
from rd.models import Detail, Photo, EngineCategory, CarCategory, EngineCategoryPhoto, CarCategoryPhoto
# Register your models here.



class PhotoInline(admin.TabularInline):
    model = Photo


class DetailAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]

    list_filter = ('cars', 'engines')
    filter_horizontal = ('related_details',)

class EnginePhotoInline(admin.TabularInline):
    model = EngineCategoryPhoto

class CategoryPhotoInline(admin.TabularInline):
    model = CarCategoryPhoto


class EngineCategoryAdmin(admin.ModelAdmin):
    inlines = [
        EnginePhotoInline
    ]

class CarCategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryPhotoInline
    ]

admin.site.register(Detail, DetailAdmin)
admin.site.register(EngineCategory, EngineCategoryAdmin)
admin.site.register(CarCategory, CarCategoryAdmin)