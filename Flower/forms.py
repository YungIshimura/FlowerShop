from django import forms
from .models import Request


class RequestToConsultation(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите Имя'}))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+ 7 (999) 000 00 00'}))


    class Meta:
        model = Request
        fields = ('name', 'phonenumber')

    def __init__(self, *args, **kwargs):
        super(RequestToConsultation, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'consultation__form_input'
