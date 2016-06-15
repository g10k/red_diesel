from django.contrib import admin
from rd.models import Detail, Photo, EngineCategory, CarCategory, EngineCategoryPhoto, CarCategoryPhoto, DetailCategory
# Register your models here.

from django import forms
from tinymce.widgets import TinyMCE

class PhotoInline(admin.TabularInline):
    model = Photo

class DetailAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]
    list_filter = ('cars', 'engines', 'nalichie', 'category')
    filter_horizontal = ('related_details',)
    list_display = ('name', 'inner_articul', 'articul', 'cost','nalichie')
    search_fields = ('name',)

class EnginePhotoInline(admin.TabularInline):
    model = EngineCategoryPhoto

class CategoryPhotoInline(admin.TabularInline):
    model = CarCategoryPhoto

class EngineForm(forms.ModelForm):
    about_html = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}), required=False)
    class Meta:
        model = EngineCategory
        fields = '__all__'

class EngineCategoryAdmin(admin.ModelAdmin):
    form = EngineForm
    list_display = ('name', 'sort')
    list_editable = ('sort',)
    search_fields = ('name',)
    inlines = [
        EnginePhotoInline
    ]

class CarForm(forms.ModelForm):
    about_html = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}),required=False)
    class Meta:
        model = CarCategory
        fields = '__all__'

class CarCategoryAdmin(admin.ModelAdmin):
    form = CarForm
    list_display = ('name', 'sort')
    list_editable = ('sort',)
    search_fields = ('name',)
    inlines = [
        CategoryPhotoInline
    ]

admin.site.register(Detail, DetailAdmin)
admin.site.register(EngineCategory, EngineCategoryAdmin)
admin.site.register(CarCategory, CarCategoryAdmin)
admin.site.register(DetailCategory)