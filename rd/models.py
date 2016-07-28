# encoding: utf-8
from django.core.urlresolvers import reverse
from django.db import models
from slugify import Slugify, CYRILLIC
slugify_ru = Slugify(pretranslate=CYRILLIC)
# Create your models here.

class ExcludeDeletedManager(models.Manager):
    """
        Кастомный менеджер заяпросов, исключающий записи помеченные как удаленные (dd != None)
    """
    def get_queryset(self):
        # исключаем из выдачи объекты, помеченные как удаленные
        return super(ExcludeDeletedManager, self).get_queryset().exclude(dd__isnull=False)




class Detail(models.Model):
    inner_articul = models.CharField(u'Внутренний артикул', max_length=255)
    articul = models.CharField(u'Артикул', max_length=255, db_index=True)
    name = models.TextField(u'Название')
    cost = models.CharField(u'Цена', max_length=255)
    test = models.TextField(u'Текст', blank=True)
    nalichie = models.CharField(u'Наличие', max_length=255, blank=True)
    proizvoditel = models.CharField(u'Производитель', max_length=255, blank=True)
    engine = models.CharField(u'Двигатель', max_length=255, blank=True)
    automobile = models.CharField(u'Автомобиль', max_length=255, blank=True)
    related_details = models.ManyToManyField('Detail', verbose_name=u'Связанные детали', null=True, blank=True)
    old_url = models.CharField(u'Старый url', max_length=400, blank=True)
    url = models.CharField(u'Ручной url', max_length=400)
    title = models.CharField(u'title', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)
    header = models.CharField(u'заголовок', max_length=255, blank=True)
    engines = models.ManyToManyField('EngineCategory', blank=True, null=True)
    cars = models.ManyToManyField('CarCategory', blank=True, null=True)
    category = models.ForeignKey('DetailCategory', verbose_name=u'Категория товара', blank=True, null=True, related_name='details')

    sort = models.IntegerField(default=1)

    dc = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    dm = models.DateTimeField(auto_now=True, verbose_name=u'Последнее изменение', db_index=True)
    dd = models.DateTimeField(u'Дата удаления',null=True, editable=False, db_index=True)

    objects = ExcludeDeletedManager()  # переопределение стандартного менеджера
    standard_objects = models.Manager()  # предусмотрим возможность использования стандартного менеджера

    def __unicode__(self):
        return '%s %s' % (self.articul, self.name)

    class Meta:
        ordering = ['name',]
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

    def get_url_with_domain(self):
        return 'www.red-diesel.ru' + self.get_absolute_url()

    def get_absolute_url(self):
        engines = '-'.join(self.engines.values_list('name', flat=True))
        detail_url = slugify_ru('_'.join([self.articul, self.name, engines, self.proizvoditel])).lower()
        reverse('detail', args=(detail_url,))
        return reverse('detail', args=(detail_url,))

    def get_related_details(self):
        if self.category:
            return self.category.details.filter(engines__in=self.engines.all()).exclude(id=self.id).order_by('?')[:4]
        else:
            return Detail.objects.none()


class DetailCategory(models.Model):
    name = models.CharField(u'Название', max_length=255)
    sort = models.IntegerField(default=1)
    related_category = models.ForeignKey('self', blank=True, null=True)

    dc = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    dm = models.DateTimeField(auto_now=True, verbose_name=u'Последнее изменение', db_index=True)
    dd = models.DateTimeField(u'Дата удаления',null=True, editable=False, db_index=True)

    objects = ExcludeDeletedManager()  # переопределение стандартного менеджера
    standard_objects = models.Manager()  # предусмотрим возможность использования стандартного менеджера

    def __unicode__(self):
        return '%s' % (self.name,)

    class Meta:
        ordering = ['name', ]
        verbose_name = u'Категория деталей'
        verbose_name_plural = u'Категории деталей'

class Photo(models.Model):
    sort = models.IntegerField(default=1)
    title = models.CharField(u'Подпись', blank=True, max_length=255)
    image = models.ImageField(verbose_name=u'путь к картинке')
    detal = models.ForeignKey(Detail, related_name='photos')

    class Meta:
        ordering = ['-sort',]

class EngineCategory(models.Model):
    url = models.CharField(u'Ручной url', max_length=400, blank=True)
    name = models.CharField(u'Категория', max_length=255, blank=False)
    title = models.CharField(u'title', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)
    about_html = models.TextField(u'html', blank=True)
    keywords = models.CharField(u'keywords', max_length=255, blank=True)
    header = models.CharField(u'heading', max_length=255, blank=True)

    sort = models.IntegerField(default=1)

    dc = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    dm = models.DateTimeField(auto_now=True, verbose_name=u'Последнее изменение', db_index=True)
    dd = models.DateTimeField(u'Дата удаления',null=True, editable=False, db_index=True)

    objects = ExcludeDeletedManager()  # переопределение стандартного менеджера
    standard_objects = models.Manager()  # предусмотрим возможность использования стандартного менеджера

    def get_absolute_url(self):
        if self.url:
            return reverse('engines_detail', args=(self.url,))
        else:
            return reverse('engines_detail', args=(self.name,))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Категория двигателя'
        verbose_name_plural = u'Категории двигателей'
        ordering = ['-sort', ]


class EngineCategoryPhoto(models.Model):
    sort = models.IntegerField(default=1)
    title = models.CharField(u'Подпись', blank=True, max_length=255)
    image = models.ImageField(verbose_name=u'путь к картинке', upload_to='dvigateli-cummins/' )
    category_detal = models.ForeignKey(EngineCategory, related_name='photos')

    class Meta:
        ordering = ['-sort', ]

class CarCategory(models.Model):
    url = models.CharField(u'Ручной url', max_length=400, blank=True)
    name = models.CharField(u'Категория', max_length=255, blank=False)
    title = models.CharField(u'title', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)
    about_html = models.TextField(u'html', blank=True)
    keywords = models.CharField(u'keywords', max_length=255, blank=True)
    header = models.CharField(u'heading', max_length=255, blank=True)

    sort = models.IntegerField(default=1)

    dc = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    dm = models.DateTimeField(auto_now=True, verbose_name=u'Последнее изменение', db_index=True)
    dd = models.DateTimeField(u'Дата удаления',null=True, editable=False, db_index=True)


    objects = ExcludeDeletedManager()  # переопределение стандартного менеджера
    standard_objects = models.Manager()  # предусмотрим возможность использования стандартного менеджера

    def get_absolute_url(self):
        if self.url:
            return reverse('trucks_detail', args=(self.url,))
        else:
            return reverse('trucks_detail', args=(self.name,))

    class Meta:
        verbose_name = u'Категория машины'
        verbose_name_plural = u'Категории машины'
        ordering = ['-sort', ]

    def __unicode__(self):
        return self.name


class CarCategoryPhoto(models.Model):
    sort = models.IntegerField(default=1)
    title = models.CharField(u'Подпись', blank=True, max_length=255)
    image = models.ImageField(verbose_name=u'путь к картинке', upload_to='car-categories/')
    category_detal = models.ForeignKey(CarCategory, related_name='photos')

    class Meta:
        ordering = ['-sort',]


def get_detail_by_url(url):
    if Detail.objects.filter(url=url):
        return Detail.objects.filter(url=url).first()
    return None


def get_detail_by_old_url(url):
    if Detail.objects.filter(old_url=url):
        return Detail.objects.filter(old_url=url).first()
    return None


def get_car_by_url(url):
    if CarCategory.objects.filter(url='').filter(name=url):
        return CarCategory.objects.filter(url='').filter(name=url).first()
    elif CarCategory.objects.filter(url=url):
        return CarCategory.objects.filter(url=url).first()

def get_engine_by_url(url):
    if EngineCategory.objects.filter(url='').filter(name=url):
        return EngineCategory.objects.filter(url='').filter(name=url).first()
    elif EngineCategory.objects.filter(url=url):
        return EngineCategory.objects.filter(url=url).first()



