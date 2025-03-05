from django import forms
from .models import CustomUser

class CustomUserRegistrationForm(forms.Form):
    email = forms.EmailField(label="Электронная почта", required=True)
    first_name = forms.CharField(label="Имя", max_length=30, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=30, required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Пароли не совпадают!")

        return cleaned_data


    def save(self, commit=True):
        data = self.cleaned_data
        user = CustomUser(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        user.set_password(data["password"])  
        if commit:
            user.save()
        return user
