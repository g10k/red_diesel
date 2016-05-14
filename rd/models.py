# encoding: utf-8
from django.db import models
from slugify import Slugify, CYRILLIC
slugify_ru = Slugify(pretranslate=CYRILLIC)
# Create your models here.




class Detal(models.Model):
    inner_articul = models.CharField(u'Внутренний артикул', max_length=255)
    articul = models.CharField(u'Артикул', max_length=255, db_index=True)
    name = models.TextField(u'Название')
    cost = models.CharField(u'Цена', max_length=255)
    test = models.TextField(u'Текст', blank=True)
    nalichie = models.CharField(u'Наличие', max_length=255, blank=True)
    proizvoditel = models.CharField(u'Производитель', max_length=255, blank=True)
    engine = models.CharField(u'Двигатель', max_length=255, blank=True)
    automobile = models.CharField(u'Автомобиль', max_length=255, blank=True)
    related_details = models.ManyToManyField('Detal', verbose_name=u'Связанные детали', null=True, blank=True)
    url = models.CharField(u'Ручной url', max_length=400)
    title = models.CharField(u'title', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)
    header = models.CharField(u'заголовок', max_length=255, blank=True)
    engine_categories = models.ManyToManyField('EngineCategoryDetail', blank=True, null=True)
    car_categories = models.ManyToManyField('CarCategoryDetail', blank=True, null=True)


    def __unicode__(self):
        return '%s %s' % (self.articul, self.name)

    class Meta:
        ordering = ['name']
        verbose_name = u'Деталь'
        verbose_name_plural = u'Деталь'

    def get_cost(self):
        try:
            cost = int(float(self.cost))
        except :
            cost = None
        return cost

    def get_articul(self):
        articul = self.articul
        first_articul = articul.split(',')[0]
        return unicode(first_articul)

    def get_full_url(self):
        return 'www.red-diesel.ru/zapchasti-cummins/%s' % self.get_absolute_url()

    def get_absolute_url(self):
        # if self.url:
        #     return self.url
        return slugify_ru('_'.join([self.articul, self.name, self.engine, self.proizvoditel])).lower()


class Photo(models.Model):
    sort = models.IntegerField(default=1)
    title = models.CharField(u'Подпись', blank=True, max_length=255)
    image = models.ImageField(verbose_name=u'путь к картинке')
    detal = models.ForeignKey(Detal, related_name='photos')

    class Meta:
        ordering = ['sort',]


class EngineCategoryDetail(models.Model):
    name = models.CharField(u'Категория', max_length=255, blank=True)
    title = models.CharField(u'title', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)
    keywords = models.CharField(u'keywords', max_length=255, blank=True)
    header = models.CharField(u'heading', max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория двигателя'


class EngineCategoryDetailPhoto(models.Model):
    sort = models.IntegerField(default=1)
    title = models.CharField(u'Подпись', blank=True, max_length=255)
    image = models.ImageField(verbose_name=u'путь к картинке')
    category_detal = models.ForeignKey(EngineCategoryDetail, related_name='photos')

    class Meta:
        ordering = ['sort', ]

class CarCategoryDetail(models.Model):
    name = models.CharField(u'Категория', max_length=255, blank=True)
    title = models.CharField(u'title', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)
    keywords = models.CharField(u'keywords', max_length=255, blank=True)
    header = models.CharField(u'heading', max_length=255, blank=True)

    class Meta:
        verbose_name = u'Категория машины'

    def __unicode__(self):
        return self.name


class CarCategoryDetailPhoto(models.Model):
    sort = models.IntegerField(default=1)
    title = models.CharField(u'Подпись', blank=True, max_length=255)
    image = models.ImageField(verbose_name=u'путь к картинке')
    category_detal = models.ForeignKey(CarCategoryDetail, related_name='photos')
    class Meta:
        ordering = ['sort',]


def get_detail_by_url(url):
    if Detal.objects.filter(url=url):
        return Detal.objects.filter(url=url).first()
    artikul = url.split('-')[0]
    if Detal.objects.filter(articul=artikul):
       return Detal.objects.filter(articul=artikul).first()
    return Detal.objects.filter(articul__icontains=artikul).first()
