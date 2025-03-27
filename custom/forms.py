from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
CustomUser = get_user_model()

class CustomUserSignupForm(SignupForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    country = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "country", "password1", "password2")

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.country = self.cleaned_data['country']
        user.save()
        return user
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
