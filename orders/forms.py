import re
from django import forms
import re._compiler


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    email = forms.EmailField()
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.CharField(required=True)
    
    region = forms.CharField(required=True)
    city = forms.CharField(required=True)
    warehouse = forms.CharField(required=True)

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        
        #pattern = re.compile(r'^\d(10)$')
        #if not pattern.match(data):
            #raise forms.ValidationError("Неверный формат номера")
        
        return data


#    first_name = forms.CharField(
#       widget=forms.TextInput(
#           attrs={
#               "class": "form-control",
#               "placeholder": "Ведите Ваше имя",
#           }
#       )
#   )
#    last_name = forms.CharField(
#       widget=forms.TextInput(
#           attrs={
#               "class": "form-control",
#               "placeholder": "Ведите Вашу Фамилию",
#           }
#       )
#   )
#    phone_number = forms.CharField(
#       widget=forms.TextInput(
#           attrs={
#               "class": "form-control",
#               "placeholder": "Номер телефона",
#           }
#       )
#   )
#    requires_delivery = forms.ChoiceField(
#       widget=forms.RadioSelect(),
#       choices=[
#           ("0", False),
#           ("1", True),
#       ],
#       initial=0
#   )

#   delivery_address = forms.CharField(
#       widget=forms.Textarea(
#           attrs={
#               "class": "form-control",
#               "id": "delivery-address",
#               "rows": 2,
#               "placeholder": "Введите адрес доставки",
#           }
#       )
#   )

#   payment_on_get = forms.ChoiceField(
#       widget=forms.RadioSelect(),
#       choices=[
#           ("0", False),
#           ("1", True),
#       ],
#       initial=0
#   )
