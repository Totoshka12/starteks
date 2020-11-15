from django import forms
from django.contrib.auth import get_user_model
from registration.forms import RegistrationFormUniqueEmail

User = get_user_model()


class CustomForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(label='Имя пользователя')
    last_name = forms.CharField(label='Фамилия пользователя')
    patronymic_name = forms.CharField(label='Отчество пользователя')
    address = forms.CharField(label='Адрес пользователя')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email
        if commit:
            user.save()
        return user

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = get_user_model()
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
            "first_name",
            "last_name",
            "patronymic_name",
            "address",
        ]
