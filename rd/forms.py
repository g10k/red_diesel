# encoding: utf-8
from django import forms

class UploadExcel(forms.Form):
    excel_file = forms.FileField(label=u'Ваш excel')

    def clean_excel_file(self):
        cd = self.cleaned_data
        return cd['excel_file']