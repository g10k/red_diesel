# -*- encoding: utf-8 -*-
from django.views.generic import TemplateView
from django import forms


class CallMessage(forms.Form):
    phone = forms.CharField(
        max_length=255,
        min_length=14,
        error_messages={
            'required': u'Укажите телефон',
            'max_length': u'Должно быть короче, чем 255 символов',
            'min_length': u'Должно быть длиннее, чем 14 символов',
        }
    )
    call_message = forms.CharField(
        required=False,
        error_messages={
            'required': u'Вы забыли указать сообщение',
        }
    )

    def as_text(self):
        res = u''
        for name, field in self.fields.items():
            bf = self[name]
            res += u'%s: %s</br>' % (bf.label, bf.value())
        return res


class PartsRequest(forms.Form):
    engine = forms.CharField(required=True)
    car = forms.CharField(required=True)
    name = forms.CharField(required=False)
    city = forms.CharField(required=False)
    phone = forms.CharField(
        required=False,
        max_length=255,
        min_length=14,
        error_messages={
            'required': u'Укажите телефон',
            'max_length': u'Должно быть короче, чем 255 символов',
            'min_length': u'Должно быть длиннее, чем 14 символов',
        }
    )
    mail = forms.EmailField(required=True)
    parts = forms.CharField(required=True)
    comment = forms.CharField(required=False)

    def as_text(self):
        res = u''
        for name, field in self.fields.items():
            bf = self[name]
            res += u'%s: %s</br>' % (bf.label, bf.value())
        return res


class BuyEngine(forms.Form):
    engine_model = forms.CharField(required=False)
    ecology = forms.CharField(required=False)
    car = forms.CharField(required=False)
    name = forms.CharField(required=False)
    city = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    mail = forms.EmailField()
    comment = forms.CharField(required=False)

    def as_text(self):
        res = u''
        for name, field in self.fields.items():
            bf = self[name]
            res += u'%s: %s</br>' % (bf.label, bf.value())
        return res

class Question(forms.Form):
    engine_model = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    mail = forms.EmailField()
    question = forms.CharField()

    def as_text(self):
        res = u''
        for name, field in self.fields.items():
            bf = self[name]
            res += u'%s: %s</br>' % (bf.label, bf.value())
        return res

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=255, min_length=4,
        error_messages={
            'required': u'Укажите ваше Имя',
            'max_length': u'Ваше имя длиннее чем 255 символов',
            'min_length': u'Имя не должно быть короче 4 символов'
        })
    mail = forms.EmailField(
        max_length=255,
        error_messages={
            'required': u'Укажите ваше e-mail',
            'invalid': u'Неверный e-mail'
        }
    )
    comment = forms.CharField(
        error_messages={
            'required': u'Вы забыли указать сообщение',
        }
    )

    def as_text(self):
        res = u''
        for name, field in self.fields.items():
            bf = self[name]
            res += u'%s: %s</br>' % (bf.label, bf.value())
        return res