from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from .models import UserAbstract
from .models import Request

# Regular expression validator to allow only Latin characters and digits in the username
latin_username_validator = RegexValidator(
    r'^[a-zA-Z0-9]*$',
    'Логин может содержать только латинские буквы и цифры.'
)

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label="ФИО", required=True)
    phone = forms.CharField(max_length=15, label="Телефон", required=True)
    email = forms.EmailField(label="Электронная почта", required=True)
    username = forms.CharField(
        max_length=150,
        label="Логин",
        required=True,
        validators=[latin_username_validator]  # Apply the validator here
    )

    class Meta:
        model = UserAbstract
        fields = ('username', 'full_name', 'phone', 'email', 'password1', 'password2')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['address', 'phone', 'email', 'request_date', 'service', 'preferred_payment_method']
        widgets = {
            'request_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Custom widget for datetime input
        }
