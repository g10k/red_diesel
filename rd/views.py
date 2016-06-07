# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

import rd.models
# Create your views here.

import rd.forms
# def get_dict_with_details(file):



import xlrd

def excel_to_list(excel_file, datemode=False):
    """
        преобразует экспель файл в список списков
        excel_file - экселевский файл
    """
    book = xlrd.open_workbook(file_contents=excel_file.read())
    sheet = book.sheets()[0]
    ncols = sheet.ncols # количество столбцов
    nrows = sheet.nrows # количество строк
    data = []
    for row in xrange(0, nrows): # идем по строке
        row_data = []
        for col in range(0, ncols): # потом идем по столбцам строки row
            row_data.append(sheet.row(row)[col].value)
        data.append(row_data)

    return data, book.datemode if datemode else None


class DetailFromExcel(object):
    pass
from operator import eq

def prepare_excel_row(excel_row):
    cost = excel_row[6]
    try:
        cost = unicode(int(round(float(cost))))
    except:
        pass

    articul = excel_row[1]
    try:
        articul = int(articul)
    except:
        pass
    articul = unicode(articul)
    name = unicode(excel_row[2])
    excel_row[1] = articul
    excel_row[2] = name
    excel_row[6] = cost
    return excel_row


def clean_articul(value):
        try:
            value = unicode(int(value))
        except:
            pass
        return value
def clean_cost(value):
        try:
            value = unicode(int(round(float(value))))
        except:
            pass
        return value

from collections import OrderedDict
OrderedDict()
EXCEL_KEYS = OrderedDict([
    (u'Внутренняя нумерация', {'clean': lambda value: value, 'field': 'inner_articul', 'is_primary': True}),
    (u'Артикул', {'clean': clean_articul, 'field': 'articul'}),
    (u'Название', {'clean': lambda value: unicode(value), 'field': 'name'}),
    (u'Производитель', {'clean': lambda value: value, 'field': 'proizvoditel'}),
    (u'Двигатель', {'clean': lambda value: value, 'field': 'engine'}),
    (u'Авто', {'clean': lambda value: value, 'field': 'automobile'}),
    (u'Цена RED Diesel', {'clean': clean_cost, 'field': 'cost'}),
    (u'Наличие на складе', {'clean': lambda value: value, 'field': 'nalichie'}),
    (u'Категория Двигатель', {'clean': lambda value: value, 'field': 'engine_categories','m2m':'name'}),
    (u'Категория Авто', {'clean': lambda value: value, 'field': 'car_categories','m2m':'name'})
])

class ExcelComparasion(object):

    # @staticmethod
    # def clean_articul(value):
    #     try:
    #         value = int(value)
    #     except:
    #         pass
    #     return value

    # @staticmethod
    # def clean_cost(value):
    #     try:
    #         value = unicode(int(round(float(value))))
    #     except:
    #         pass
    #     return value
    keys = EXCEL_KEYS
    def __init__(self, excel_data):
        self.excel_data = excel_data
        self.set_headers()
        self.new_objects = []
        self.difference_objects = []

    def set_headers(self):
        excel_header_row = self.excel_data[0]
        self.headers = dict([(key, excel_header_row.index(key)) for key in self.keys.keys()])

    def get_header_index(self, header_name):
        return self.headers.get(header_name)

    def get_value_by_name(self, name, excel_row):
        return self.keys[name]['clean'](excel_row[self.get_header_index(name)])

    def get_values(self, excel_row):
        inner_articul = self.get_value_by_name(u'Внутренняя нумерация', excel_row)
        articul = self.get_value_by_name(u'Артикул', excel_row)
        name = self.get_value_by_name(u'Название', excel_row)
        proizvoditel = self.get_value_by_name(u'Производитель', excel_row)
        engine = self.get_value_by_name(u'Двигатель', excel_row)
        car = self.get_value_by_name(u'Авто', excel_row)
        cost = self.get_value_by_name(u'Цена RED Diesel', excel_row)
        nalichie = self.get_value_by_name(u'Наличие на складе', excel_row)
        engine_category = self.get_value_by_name(u'Категория Двигатель', excel_row)
        car_category = self.get_value_by_name(u'Категория Авто', excel_row)

        return inner_articul, articul, name, proizvoditel, engine, car, cost, nalichie,engine_category,car_category

    def compare(self):
        co_list = []
        for excel_row in self.excel_data[1:]:
            co = CompareObject(excel_row)
            co_list.append(co)
        new_objects = [co for co in co_list if co.is_new]
        difference_objects = [co for co in co_list if any(co.differences.values())]
        self.difference_objects = difference_objects
        self.new_objects = new_objects

class CompareObject(object):
    keys = EXCEL_KEYS
    is_new = False
    def __init__(self, excel_row):
        self.excel_row = excel_row
        self.differences = OrderedDict()
        index_of_primary, primary_key_data = [(index, key_data) for index, (field_name, key_data) in enumerate(self.keys.items()) if key_data.get('is_primary')][0]
        found_instances = rd.models.Detal.objects.filter(**{primary_key_data['field']: excel_row[index_of_primary]})
        if found_instances:
            self.instance = found_instances[0]
            self.compare_values()
        else:
            # TODO: СОздать новый
            new_instance_values = dict([(key_data['field'], excel_value) for (key, key_data), excel_value in zip(self.keys.items(), excel_row) if not key_data.get('m2m')] )
            detal = rd.models.Detal(**new_instance_values)
            self.instance = detal
            self.is_new = True

    def compare_values(self):
        assert len(self.excel_row) == len(self.keys)
        for excel_value, (column_name, key_data) in zip(self.excel_row, self.keys.items()):
            if isinstance(excel_value, basestring):
                excel_value = excel_value.strip()
            if key_data.get('m2m'):
                model = getattr(self.instance, key_data['field']).model

                instance_set = set([rel_object_dict.get(key_data['m2m']) for rel_object_dict in getattr(self.instance, key_data['field']).values()])
                excel_set = set([v.strip() for v in excel_value.split(',') if v])
                instance_value = u', '.join([rel_object_dict.get(key_data['m2m']) for rel_object_dict in getattr(self.instance, key_data['field']).order_by('-name').values()])
                # instance_set = instance_value.

                if instance_set ^ excel_set:
                    self.differences[key_data['field']] = {'excel_value': excel_value, 'instance_value': instance_value, 'column_name': column_name, 'm2m': key_data['m2m'], 'field':key_data['field']}
                else:
                    self.differences[key_data['field']] = None
            else:
                excel_value = key_data['clean'](excel_value)
                instance_value = getattr(self.instance, key_data['field'])
                if instance_value != excel_value:
                    self.differences[key_data['field']] = {'excel_value': excel_value, 'instance_value': instance_value, 'column_name' : column_name}
                else:
                    self.differences[key_data['field']] = None

    def compare_categories(self):
        pass


model_keys = ['inner_articul', 'articul', 'name', 'proizvoditel', 'engine', 'automobile', 'cost', 'nalichie']
def load(excel_data):
    # model_keys = ['inner_articul', 'articul', 'name', 'proizvoditel', 'engine', 'automobile', 'cost', 'nalichie']
    new_objects = []
    difference_objects = []
    for excel_row in excel_data:
        if not excel_row[0] or excel_row[0] == u'Внутренняя нумерация':
            continue
        prepare_excel_row(excel_row)
        detail_insance = rd.models.Detal.objects.create_or_update(**dict(zip(model_keys, excel_row)))
    # return new_objects, difference_objects

@login_required(login_url='/admin')
def excel_upload(request):
    c = {}
    form = rd.forms.UploadExcel(request.POST, request.FILES)
    if form.is_valid():
        result = []
        f = form.cleaned_data['excel_file']
        l = excel_to_list(f)
        # print request.POST

        excel_comparasion = ExcelComparasion(l[0])
        excel_comparasion.compare()
        new_objects = excel_comparasion.new_objects
        difference_objects = excel_comparasion.difference_objects

        # find_engines_and_groups(l[0])
        c['new_objects'] = new_objects
        c['difference_objects'] = difference_objects

        if request.POST.get('load'):

            for co in difference_objects:
                difference_dict = dict([(field_name, differences)for field_name, differences in co.differences.items() if differences])
                for field_name, difference_data in difference_dict.items():
                    if not difference_data.get('m2m'):
                        setattr(co.instance, field_name, difference_data.get('excel_value'))
                    else:
                        # Сделать m2m изменение
                        names = [name.strip() for name in difference_data.get('excel_value').split(',')]
                        related_manager = getattr(co.instance, difference_data.get('field'))
                        related_manager.through.objects.filter(detal=co.instance).delete()
                        related_objects = related_manager.model.objects.filter(**{difference_data.get('m2m') + '__in': names}).distinct()
                        for rel_object in related_objects:
                            getattr(co.instance, difference_data.get('field')).add(rel_object)
                co.instance.save()

            # for object in difference_objects:
            #     for key, value in zip(model_keys, object.difference_row):
            #         if value:
            #             setattr(object, key, value)
            #     object.save()
            #
            # for object in new_objects:
            #     object.save()

        c['all_excel_data'] = l[0]
        result.append({
            'instance': 1,
            'difference': None, #[] or None
        })

    c['details'] = rd.models.Detal.objects.all()
    c['form'] = form
    return render(request, 'rd/excel_upload.html', c)
# form = forms.WorkerImportXls(request.POST or None, request.FILES or None, instance=worker_import)



@login_required(login_url='/admin')
def update_urls(request):
    c = {}
    # form = rd.forms.UploadExcel(request.POST, request.FILES)
    urls = []

    if 'load' in request.POST:
        updated_urls = []
        for detail in rd.models.Detal.objects.all():
            if detail.url != detail.get_absolute_url():
                detail.old_url = detail.url
                detail.url = detail.get_absolute_url()
                detail.save()
                updated_urls.append(detail)

        c['updated_urls'] = updated_urls

    else:

        for detail in rd.models.Detal.objects.all():
            if detail.url != detail.get_absolute_url():
                urls.append(detail)
    c['urls'] = urls


    return render(request, 'rd/update_urls.html', c)
# form = forms.WorkerImportXls(request.POST or None, request.FILES or None, instance=worker_import)