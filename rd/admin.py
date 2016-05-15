from django.contrib import admin
from rd.models import Detal, Photo, EngineCategoryDetail, CarCategoryDetail, EngineCategoryDetailPhoto, CarCategoryDetailPhoto
# Register your models here.



class PhotoInline(admin.TabularInline):
    model = Photo


class DetalAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]

    list_filter = ('car_categories', 'engine_categories')
    filter_horizontal = ('related_details',)

class EnginePhotoInline(admin.TabularInline):
    model = EngineCategoryDetailPhoto

class CategoryPhotoInline(admin.TabularInline):
    model = EngineCategoryDetailPhoto


class EngineCategoryDetailAdmin(admin.ModelAdmin):
    inlines = [
        EnginePhotoInline
    ]

class CarCategoryDetailAdmin(admin.ModelAdmin):
    inlines = [
        CategoryPhotoInline
    ]

admin.site.register(Detal, DetalAdmin)
admin.site.register(EngineCategoryDetail, EngineCategoryDetailAdmin)
admin.site.register(CarCategoryDetail, CarCategoryDetailAdmin)