# -*- encoding: utf-8 -*-
import json
import operator

from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import BaseFormView
from django.core.mail import mail_admins

import django_project.views
import django_project.forms
import rd.models
from rd.models import get_detail_by_url, get_car_by_url, get_engine_by_url, get_detail_by_old_url

class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before EcmaScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be an json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder)
        super(JsonResponse, self).__init__(content=data, **kwargs)


class CallMessageView(BaseFormView):
    form_class = django_project.forms.CallMessage
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):

        form = self.get_form(self.form_class)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            call_message = form.cleaned_data['call_message']
            mail_admins(
                u'Заказ звонка на сайте',
                message='simple plain text message',
                html_message= u'Номер: «%s»\nСообщение:\n «%s».' % (phone, call_message)
            )


            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'errors': form.errors})

call_message_view = csrf_exempt(CallMessageView.as_view())


class PartsRequestView(BaseFormView):
    form_class = django_project.forms.PartsRequest
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            mail_admins(
                u'Заявка на сайте',
                message='simple plain text message',
                html_message=u'%s' % form.as_p()
            )
            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'errors': form.errors})
parts_request_view = csrf_exempt(PartsRequestView.as_view())


class BuyEngineView(BaseFormView):
    form_class = django_project.forms.BuyEngine
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            engine_model = request.POST.get('engine_model')
            mail_admins(
                u'Заявка на двигатель %s' % engine_model,
                message='simple plain text message',
                html_message=u'%s' % form.as_p()
            )

            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'errors': form.errors})
buy_engine = csrf_exempt(BuyEngineView.as_view())

class QuestionView(BaseFormView):
    form_class = django_project.forms.Question
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            engine_model = request.POST.get('engine_model')
            mail_admins(
                u'Вопрос по двигателю %s' % engine_model,
                message='simple plain text message',
                html_message=u'%s' % form.as_p()
            )
            return JsonResponse({'success': 'ok'})
        else:
            return JsonResponse({'errors': form.errors})
question = csrf_exempt(QuestionView.as_view())


class ContactView(FormView):
    form_class = django_project.forms.ContactForm
    template_name = 'django_project/contact.html'
    success_url = '/contact/?thanks'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        mail = form.cleaned_data.get('mail')
        message = form.cleaned_data.get('comment')
        mail_admins(
                u'Новое сообщение на сайте',
                message='simple plain text message',
                html_message=u'пользователь: «%s» пишет:\n «%s».\n Его почта: «%s»' % (name, message, mail)
            )

        return super(ContactView, self).form_valid(form)
contract = ContactView.as_view()


def details_search(term):
    lookups = ['articul', 'name', 'proizvoditel', 'engine', 'automobile']
    words = term.split()
    q_objects = []
    if not words:
        return rd.models.Detail.objects.all()

    for word in words:
        q_object = reduce(
            lambda res, lookup: res | Q(**{"%s__icontains" % (lookup,): word}),
            lookups[1:],
            Q(**{"%s__icontains" % lookups[0]: word})
        )
        q_objects.append(q_object)
    Q_all = reduce(operator.and_, q_objects)

    return rd.models.Detail.objects.filter(Q_all)

class SearchAjaxView(BaseFormView):
    def get(self, request, *args, **kwargs):
        details = rd.models.Detail.objects.all()
        term = request.GET.get('term')
        if term:
            details = details_search(term)

        if len(details) > 10:
            all_details_count = len(details)
            details = details[:10]
            res = [{'label': u' '.join([d.articul, d.name, d.engine, d.proizvoditel]), 'href': d.get_absolute_url()} for d in details]
            price_href = reverse('price')+'?search=%s' % term
            res.append({'label': u"Всего %s результатов ..." % all_details_count, 'href': price_href})
        else:
            res = [{'label': u' '.join([d.articul, d.name, d.engine, d.proizvoditel]), 'href': d.get_absolute_url()} for d in details]
        return JsonResponse(res, safe=False)
search_detail_json = SearchAjaxView.as_view()


class DetailAjaxView(BaseFormView):
    def get(self, request, *args, **kwargs):
        details = rd.models.Detail.objects.all()
        engine = request.GET.get('engine')
        if engine:
            details = details.filter(engines__name=engine)
        car = request.GET.get('car')
        if car:
            details = details.filter(cars__name=car)

        res = [[
                d.articul,
                "<a href='http://%s'>%s</a>" % ('www.red-diesel.ru'+reverse('detail', args=(d.url,)), u' '.join([d.name, d.engine, d.proizvoditel])),
                d.automobile,
                d.get_cost() or u"Цену уточняйте",
                d.nalichie
               ]
            for d in details]
        return JsonResponse({'data': res})
detail = DetailAjaxView.as_view()

class DetailPageView(TemplateView):
    template_name = 'django_project/detail_page.html'

    def dispatch(self, request, *args, **kwargs):
        url = self.args[0]
        detail = get_detail_by_url(url)
        old_detail = get_detail_by_old_url(url)
        if not detail and old_detail:
            return redirect(reverse(django_project.views.detail_page, args=(old_detail.url,)))
        return super(DetailPageView,self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        url = self.args[0]
        detail = get_detail_by_url(url)
        if detail:
            return {'detail':detail}
        else:
             raise Http404(u'Нет такой страницы')
detail_page = DetailPageView.as_view()


class CarsView(TemplateView):
    template_name = 'django_project/car_categories/car_categories.html'
    def get_context_data(self, **kwargs):
        return {'cars': rd.models.CarCategory.objects.all()}
cars = CarsView.as_view()

class CarDetailView(TemplateView):
    template_name = 'django_project/car_categories/car_category_detail.html'
    def get_context_data(self, **kwargs):
        car_detail_url = self.args[0]
        car_category = get_car_by_url(car_detail_url)
        if not car_category:
            raise Http404(u'Нет категории автомобиля %s' % car_detail_url)
        return {'car_category': car_category}
car_detail = CarDetailView.as_view()


class EnginesView(TemplateView):
    template_name = 'django_project/engines/engines_list.html'
    def get_context_data(self, **kwargs):
        return {'engines': rd.models.EngineCategory.objects.all()}
engines = EnginesView.as_view()


class EngineDetailView(TemplateView):
    template_name = 'django_project/engines/engine_detail.html'
    def get_context_data(self, **kwargs):
        engine_detail_url = self.args[0]
        engine = get_engine_by_url(engine_detail_url)
        if not engine:
            raise Http404(u'Нет двигателя %s' % engine_detail_url)
        return {'engine': engine}
engine_detail = EngineDetailView.as_view()