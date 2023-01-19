from django import forms
from .models import Request, Order


class RequestToConsultationForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите Имя'}))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+ 7 (999) 000 00 00'}))


    class Meta:
        model = Request
        fields = ('name', 'phonenumber')

    def __init__(self, *args, **kwargs):
        super(RequestToConsultationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'consultation__form_input'


class OrderForm(forms.ModelForm):
    TIME_OF_DELIVERY = [
        ('FAST_AS_POSSIBLE', 'Как можно скорее'),
        ('FROM_10_TO_12', 'С 10:00 до 12:00'),
        ('FROM_12_TO_14', 'С 12:00 до 14:00'),
        ('FROM_14_TO_16', 'С 14:00 до 16:00'),
        ('FROM_16_TO_18', 'С 16:00 до 18:00'),
        ('FROM_18_TO_20', 'С 18:00 до 20:00')
    ]

    customer_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите Имя'}))
    time = forms.ChoiceField(choices=TIME_OF_DELIVERY, widget=forms.RadioSelect())
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+ 7 (999) 000 00 00'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Адрес доставки'}))

    class Meta:
        model = Order
        fields = ('customer_name', 'phonenumber', 'address', 'time' )

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'order__form_input'
        self.fields['time'].widget.attrs['class'] = 'order__form_radio'