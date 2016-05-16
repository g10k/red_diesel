# -*- encoding: utf-8 -*-
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import BaseFormView
from django.core.mail import send_mail, mail_admins

import django_project.forms
from rd.models import get_detail_by_url, get_car_by_url, get_engine_by_url

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
    template_name = 'rd/contact.html'
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



import rd.models

class DetailAjaxView(BaseFormView):
    def get(self, request, *args, **kwargs):
        details = rd.models.Detal.objects.all()
        engine = request.GET.get('engine')
        if engine:
            details = details.filter(engine_categories__name=engine)
        car = request.GET.get('car')
        if car:
            details = details.filter(car_categories__name=engine)
        res = [[d.articul, "<a href='http://%s'>%s</a>" % (d.get_full_url(), u' '.join([d.name, d.engine, d.proizvoditel])), d.automobile, d.get_cost() or u"Цену уточняйте", d.nalichie] for d in details]
        return JsonResponse({'data': res})
detail = DetailAjaxView.as_view()


class DetailPageView(TemplateView):
    template_name = 'rd/detail_page.html'
    def get_context_data(self, **kwargs):
        print kwargs, self.request, self.args, self.kwargs
        # print self.args, self.kwargs
        url = self.args[0]
        detail = get_detail_by_url(url)
        if not detail:
            raise Http404(u'Нет такой страницы')
        return {'detail':detail}
detail_page = DetailPageView.as_view()





class CarsView(TemplateView):
    template_name = 'rd/car_categories/car_categories.html'
    def get_context_data(self, **kwargs):

        return {'car_categories': rd.models.CarCategoryDetail.objects.all()}
cars = CarsView.as_view()

class CarDetailView(TemplateView):
    template_name = 'rd/car_categories/car_category_detail.html'
    def get_context_data(self, **kwargs):
        car_detail_url = self.args[0]
        car_category =  get_car_by_url(car_detail_url)
        if not car_category:
            raise Http404(u'Нет категории автомобиля %s' % car_detail_url)
        return {'car_category': car_category}
car_detail = CarDetailView.as_view()



class EnginesView(TemplateView):
    template_name = 'rd/engines/engines_list.html'
    def get_context_data(self, **kwargs):
        return {'engines': rd.models.EngineCategoryDetail.objects.all()}
engines = EnginesView.as_view()


class EngineDetailView(TemplateView):
    template_name = 'rd/engines/engine_detail.html'
    def get_context_data(self, **kwargs):
        engine_detail_url = self.args[0]
        engine = get_engine_by_url(engine_detail_url)
        if not engine:
            raise Http404(u'Нет двигателя %s' % engine_detail_url)
        return {'engine': engine}
engine_detail = EngineDetailView.as_view()