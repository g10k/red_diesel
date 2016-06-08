# encoding: utf-8
from django import forms

class UploadExcel(forms.Form):
    excel_file = forms.FileField(label=u'Ваш excel')
    from_scratch = forms.BooleanField(label=u"Начать все с 0. Все данные категории машин, двигателей и детали будут удалены.", initial=False, required=False)
    compare = forms.BooleanField(label=u"Сравнить. Показать все изменения, которые будут произведены.", initial=False, required=False)
    update_without_groups = forms.BooleanField(label=u"Обновить без категорий", initial=False, required=False)
    update_all = forms.BooleanField(label=u"Обновить полностью. (С группами)", initial=False, required=False)

    def clean_excel_file(self):
        cd = self.cleaned_data
        return cd['excel_file']