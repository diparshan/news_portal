from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailValidation(forms.EmailField):
    def validate(self, value):
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("Email already exists.")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Email already exists.")
        except User.DoesNotExist:
            pass


class UserSignUpForm(UserCreationForm):
    email = EmailValidation(required=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')