from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        user.phone_number = form.cleaned_data.get('phone_number', '')
        user.country = form.cleaned_data.get('country', '')

        if commit:
            user.save()
        return user


class CustomSocialAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        extra_data = sociallogin.account.extra_data
        user.country = extra_data.get('locale', '')
        user.phone_number = ''

        user.save()
        return user
