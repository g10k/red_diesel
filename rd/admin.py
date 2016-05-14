from django.contrib import admin
from rd.models import Detal, Photo, EngineCategoryDetail, CarCategoryDetail
# Register your models here.



class PhotoInline(admin.TabularInline):
    model = Photo


class DetalAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]

    list_filter = ('car_categories', 'engine_categories')
    filter_horizontal = ('related_details',)




admin.site.register(Detal, DetalAdmin)
admin.site.register(EngineCategoryDetail, admin.ModelAdmin)
admin.site.register(CarCategoryDetail, admin.ModelAdmin)