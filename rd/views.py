# encoding: utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect

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

def simple_clean(val):
    if isinstance(val, basestring):
        val = val.strip()
    if type(val) is not unicode:
        val = val.decode('utf8')
    return val

def clean_articul(value):
    try:
        value = unicode(int(value))
    except:
        pass

    value = simple_clean(value)
    return value

def clean_cost(value):
    try:
        value = unicode(int(round(float(value))))
    except:
        pass
    value = simple_clean(value)
    return value

from collections import OrderedDict, defaultdict

def name_clean(value):
    unicode_value = value if type(value) is unicode else value.decode('utf8')
    return unicode_value.strip().upper()

EXCEL_KEYS = OrderedDict([
    (u'Внутренняя нумерация', {'clean': simple_clean, 'field': 'inner_articul', 'is_primary': True}),
    (u'Артикул', {'clean': clean_articul, 'field': 'articul'}),
    (u'Название', {'clean': simple_clean, 'field': 'name'}),
    (u'Производитель', {'clean': simple_clean, 'field': 'proizvoditel'}),
    (u'Двигатель', {'clean': simple_clean, 'field': 'engine'}),
    (u'Авто', {'clean': simple_clean, 'field': 'automobile'}),
    (u'Цена RED Diesel', {'clean': clean_cost, 'field': 'cost'}),
    (u'Наличие на складе', {'clean': simple_clean, 'field': 'nalichie'}),
    (u'Категория Двигатель', {'clean': simple_clean, 'field': 'engines', 'm2m':'name','m2m_clean': name_clean, 'm2m_model': rd.models.EngineCategory}),
    (u'Категория Авто', {'clean': simple_clean, 'field': 'cars', 'm2m':'name', 'm2m_clean': name_clean, 'm2m_model': rd.models.CarCategory}),
    (u'Категория Товара', {'clean': simple_clean, 'field': 'category', 'fk': 'name', 'fk_clean': name_clean, 'fk_model': rd.models.DetailCategory})
])

class ExcelComparasion(object):
    keys = EXCEL_KEYS
    def __init__(self, excel_data):
        self.excel_data = excel_data
        self.set_headers()
        self.new_objects = []
        self.difference_objects = []

    def set_headers(self):
        excel_header_row = self.excel_data[0]

        headers_dict = {}
        for key in self.keys.keys():
            headers_dict[key] = excel_header_row.index(key)
        self.headers = headers_dict

    def get_header_index(self, header_name):
        return self.headers.get(header_name)

    def get_value_by_name(self, name, excel_row):
        return self.keys[name]['clean'](excel_row[self.get_header_index(name)])

    def load_from_scratch(self):
        start = datetime.datetime.now()
        print 'start at: ', start
        self._delete_all_from_database()
        print 'all deleted for ', datetime.datetime.now() - start

        self._create_groups_from_scratch()
        print 'new_groups finished for', datetime.datetime.now() - start

        for excel_row in self.excel_data[1:]:
            new_detail = NewObject(excel_row)
        print 'new_details finished for', datetime.datetime.now() - start


    def _delete_all_from_database(self):
        rd.models.Detail.objects.all().delete()
        rd.models.CarCategory.objects.all().delete()
        rd.models.EngineCategory.objects.all().delete()

    def _create_groups_from_scratch(self):
        m2m_dict = defaultdict(set)
        for excel_row in self.excel_data[1:]:
            for excel_value, key_info in zip(excel_row, self.keys.values()):
                if key_info.get('m2m'):
                    clean_m2m = key_info.get('m2m_clean')
                    names = [clean_m2m(word) for word in excel_value.split(',') if clean_m2m(word)]

                    m2m_dict[key_info.get('field')].update(names)

        for m2m_field_related, values in m2m_dict.items():
            m2m_model, m2m_field = [(key_info.get('m2m_model'), key_info.get('m2m')) for key_info in self.keys.values() if key_info.get('field') == m2m_field_related][0]
            for value in values:
                if value:
                    m2m_model.objects.create(**{m2m_field: value}).save()

    def _find_deleted_objects(self):
        inner_articul_column_in_excel = self.get_header_index(u'Внутренняя нумерация')
        excel_inner_articules = set([excel_row[inner_articul_column_in_excel] for excel_row in self.excel_data[1:]])
        instances_inner_articules = set(rd.models.Detail.objects.values_list('inner_articul', flat=True))

        art_for_delete = instances_inner_articules - excel_inner_articules
        rd.models.Detail.objects.filter(inner_articul__in=art_for_delete).update(dd=datetime.datetime.now())


    def compare(self):
        co_list = []
        for excel_row in self.excel_data[1:]:
            co = CompareObject(excel_row)
            co_list.append(co)
        new_objects = [co for co in co_list if co.is_new]
        difference_objects = [co for co in co_list if any(co.differences.values())]
        self.difference_objects = difference_objects
        self.new_objects = new_objects

    def update(self):
        self.compare()
        for new_object_co in self.new_objects:
            NewObject(new_object_co.excel_row)

        for diff_obj in self.difference_objects:
            UpdateObject(diff_obj)

        self._find_deleted_objects()

def update_model_m2m(instance, related_field, primary_field, new_value, clean_method):
    """
    :param instance:
    :param related_field: cars
    :param related_model:  rd.models.CarCategory
    :param primary_field:  name модели
    :param new_value:  ГАЗ, ВАЗ, ПАЗ
    """
    related_model = getattr(instance, related_field).model
    names = [clean_method(w) for w in new_value.split(',') if clean_method(w)]
    related_instances = related_model.objects.filter(**{primary_field + "__in": names}).distinct()
    if related_instances.count() < names:
        for n in set(names) - set(related_instances.values_list(primary_field, flat=True)):
            if clean_method(n):
                related_model.objects.create(**{primary_field: clean_method(n)})
    getattr(instance, related_field).clear()
    for rel_instance in related_instances:
        getattr(instance, related_field).add(rel_instance)

def update_model_fk(instance, related_field, primary_field,new_value, clean_method):
    """

    :param instance: detail
    :param related_field:  category
    :param primary_field: name
    :param new_value: 'коленвал'
    :param clean_method:
    :return:
    """
    related_model = instance._meta.get_field_by_name(related_field)[0].related_model().__class__

    # related_model = getattr(instance, related_field).model
    cleaned_excel_value = clean_method(new_value)
    obj, created = related_model.objects.get_or_create(**{primary_field: cleaned_excel_value})
    # exists_objects = related_model.objects.filter(**{primary_field: new_value})
    # if exists_objects:
    setattr(instance, related_field, obj)
    instance.save()
    # else:
    #     related_model.objects.create(**{primary_field: new_value})


class UpdateObject(object):
    keys = EXCEL_KEYS

    def __init__(self, compare_object):
        self.compare_object = compare_object
        self.update()

    def update(self):
        instance = self.compare_object.instance
        for difference_field, diff_values in self.compare_object.differences.items():
            if not diff_values:
                continue
            key_info = diff_values.get('key_info')
            if key_info.get('m2m'):
                primary_field = key_info.get('m2m')
                update_model_m2m(instance, difference_field, primary_field, diff_values.get('excel_value'), key_info.get('m2m_clean'))
            elif key_info.get('fk'):
                # related_field = key_info.get('field')
                primary_field = key_info.get('fk')
                update_model_fk(instance, difference_field, primary_field, diff_values.get('excel_value'), key_info.get('fk_clean'))
            else:
                setattr(instance, difference_field, diff_values['excel_value'])
        instance.save()


class NewObject(object):
    keys = EXCEL_KEYS
    def __init__(self, excel_row):
        detail_instance_params = {}

        # Создаем деталь
        for excel_value, key_info in zip(excel_row, self.keys.values()):
            if key_info.get('m2m') or key_info.get('fk'):
                continue
            detail_instance_params[key_info.get('field')] = key_info.get('clean')(excel_value)
        detail_instance = rd.models.Detail.objects.create(**detail_instance_params)


        # Наполняем Ставим ForeignKey
        for excel_value, key_info in zip(excel_row, self.keys.values()):
            if key_info.get('fk'):
                related_field = key_info.get('field')
                primary_field = key_info.get('fk')
                update_model_fk(detail_instance, related_field, primary_field, excel_value, key_info.get('fk_clean'))

        # Наполняем m2m
        for excel_value, key_info in zip(excel_row, self.keys.values()):
            if key_info.get('m2m'):
                related_field = key_info.get('field')
                primary_field = key_info.get('m2m')
                update_model_m2m(detail_instance, related_field, primary_field, excel_value, key_info.get('m2m_clean'))


class CompareObject(object):
    keys = EXCEL_KEYS
    is_new = False
    def __init__(self, excel_row):
        self.excel_row = excel_row
        self.differences = OrderedDict()
        index_of_primary, primary_key_data = [(index, key_data) for index, (field_name, key_data) in enumerate(self.keys.items()) if key_data.get('is_primary')][0]
        found_instances = rd.models.Detail.objects.filter(**{primary_key_data['field']: excel_row[index_of_primary]})
        if found_instances:
            self.instance = found_instances[0]
            self.compare_values()
        else:
            # TODO: СОздать новый
            new_instance_values = dict([(key_data['field'], excel_value) for (key, key_data), excel_value in zip(self.keys.items(), excel_row) if not (key_data.get('m2m') or key_data.get('fk'))] )
            detal = rd.models.Detail(**new_instance_values)
            self.instance = detal
            self.is_new = True

    def compare_values(self):
        assert len(self.excel_row) == len(self.keys)
        for excel_value, (column_name, key_info) in zip(self.excel_row, self.keys.items()):
            if isinstance(excel_value, basestring):
                excel_value = excel_value.strip()

            if key_info.get('m2m'):
                clean_method = key_info.get('m2m_clean')
                instance_set = set([clean_method(rel_object_dict.get(key_info['m2m'])) for rel_object_dict in getattr(self.instance, key_info['field']).values()])
                excel_set = set([clean_method(v) for v in excel_value.split(',') if v])
                instance_value = u', '.join([rel_object_dict.get(key_info['m2m']) for rel_object_dict in getattr(self.instance, key_info['field']).order_by('-name').values()])
                if instance_set ^ excel_set:
                    self.differences[key_info['field']] = {'excel_value': excel_value, 'instance_value': instance_value, 'column_name': column_name, 'key_info':key_info, 'm2m': key_info['m2m'], 'field':key_info['field']}
                else:
                    self.differences[key_info['field']] = None
            elif key_info.get('fk'):
                clean_method = key_info.get('fk_clean')
                inst_related_obj = getattr(self.instance, key_info['field'])
                cleaned_excel_value = clean_method(excel_value)
                if not inst_related_obj and not cleaned_excel_value:
                    self.differences[key_info['field']] = None
                    continue
                elif not inst_related_obj and cleaned_excel_value:
                    self.differences[key_info['field']] = {'excel_value': excel_value, 'instance_value': '', 'column_name': column_name, 'key_info': key_info, 'fk': key_info['fk'], 'field':key_info['field']}
                else:
                    inst_related_value = getattr(inst_related_obj, key_info['fk'])
                    if inst_related_value != cleaned_excel_value:
                        self.differences[key_info['field']] = {'excel_value': cleaned_excel_value, 'instance_value': inst_related_value, 'column_name': column_name, 'key_info': key_info, 'fk': key_info['fk'], 'field':key_info['field']}
            else:
                excel_value = key_info['clean'](excel_value)
                instance_value = getattr(self.instance, key_info['field'])
                if instance_value != excel_value:
                    self.differences[key_info['field']] = {'excel_value': excel_value, 'instance_value': instance_value, 'column_name' : column_name, 'key_info':key_info}
                else:
                    self.differences[key_info['field']] = None

@login_required(login_url='/admin')
def excel_upload(request):
    c = {}
    form = rd.forms.UploadExcel(request.POST, request.FILES)
    if form.is_valid():
        result = []
        f = form.cleaned_data['excel_file']
        l = excel_to_list(f)
        excel_comparasion = ExcelComparasion(l[0])
        if form.cleaned_data.get('from_scratch'):
            excel_comparasion.load_from_scratch()
            return redirect(reverse('rd.views.excel_upload'))

        if form.cleaned_data.get('compare'):
            excel_comparasion.compare()
            c['new_objects'] = [no.instance for no in excel_comparasion.new_objects]
            c['difference_objects'] = excel_comparasion.difference_objects

        if form.cleaned_data.get('update_all'):
            excel_comparasion.update()
            return redirect(reverse('rd.views.excel_upload'))

        c['all_excel_data'] = l[0]
        result.append({
            'instance': 1,
            'difference': None, #[] or None
        })
    c['EXCEL_KEYS'] = EXCEL_KEYS
    c['details'] = rd.models.Detail.objects.all()
    c['form'] = form
    return render(request, 'rd/excel_upload.html', c)
# form = forms.WorkerImportXls(request.POST or None, request.FILES or None, instance=worker_import)



@login_required(login_url='/admin')
def update_urls(request):
    c = {}
    # form = django_project.forms.UploadExcel(request.POST, request.FILES)
    urls = []

    if 'load' in request.POST:
        updated_urls = []
        for detail in rd.models.Detail.objects.all():
            if detail.url != detail.get_absolute_url():
                detail.old_url = detail.url
                detail.url = detail.get_absolute_url()
                detail.save()
                updated_urls.append(detail)

        c['updated_urls'] = updated_urls

    else:
        for detail in rd.models.Detail.objects.all():
            if detail.url != detail.get_absolute_url():
                urls.append(detail)
    c['urls'] = urls
    return render(request, 'rd/update_urls.html', c)
# form = forms.WorkerImportXls(request.POST or None, request.FILES or None, instance=worker_import)