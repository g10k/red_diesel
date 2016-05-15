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



def compare(excel_data):
    model_keys = ['inner_articul', 'articul', 'name', 'proizvoditel', 'engine', 'automobile', 'cost', 'nalichie']
    new_objects = []
    difference_objects = []
    for excel_row in excel_data:
        if not excel_row[0] or excel_row[0] == u'Внутренняя нумерация':
            continue
        prepare_excel_row(excel_row)

        detail_insance = rd.models.Detal.objects.filter(inner_articul=excel_row[0])
        if not detail_insance:
            detal = rd.models.Detal(**dict(zip(model_keys, excel_row)))
            new_objects.append(detal)
        else:
            detail_object_with_diff = compare_object_and_excel_data(excel_row)
            if detail_object_with_diff:
                difference_objects.append(detail_object_with_diff)
    return new_objects, difference_objects

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

def compare_object_and_excel_data(excel_row):
    # Ищем отличия, объект точно должен быть с inner_articul
    detail_insance= rd.models.Detal.objects.get(inner_articul=excel_row[0])
    model_keys = ['inner_articul', 'articul', 'name', 'proizvoditel', 'engine', 'automobile', 'cost', 'nalichie']
    instance_values = [getattr(detail_insance, k) for k in model_keys]
    compare_values = map(lambda a: eq(a[0], a[1]), zip(instance_values, excel_row))
    if all(compare_values):
        return None
    difference_row = []
    for is_equal, value in zip(compare_values, excel_row):
        if is_equal:
            difference_row.append('')
        else:
            difference_row.append(value)
    detail_insance.difference_row = difference_row
    return detail_insance


@login_required(login_url='/admin')
def excel_upload(request):
    c = {}
    form = rd.forms.UploadExcel(request.POST, request.FILES)
    if form.is_valid():
        result = []
        f = form.cleaned_data['excel_file']
        l = excel_to_list(f)
        print request.POST

        new_objects, difference_objects = compare(l[0])
        c['new_objects'] = new_objects
        c['difference_objects'] = difference_objects

        if request.POST.get('load'):
            for object in difference_objects:
                for key, value in zip(model_keys, object.difference_row):
                    if value:
                        setattr(object, key, value)
                object.save()

            for object in new_objects:
                object.save()

        c['all_excel_data'] = l[0]
        result.append({
            'instance':1,
            'difference': None, #[] or None
        })

    c['details'] = rd.models.Detal.objects.all()
    c['form'] = form
    return render(request, 'rd/excel_upload.html', c)
# form = forms.WorkerImportXls(request.POST or None, request.FILES or None, instance=worker_import)