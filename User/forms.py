from django import forms
from .models import User
class RegistrationForm(forms.ModelForm):
    is_active = forms.BooleanField(required=False)
    class Meta():
        model = User
        fields = ['phone', 'password']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active= False
        user.set_password('1')
        if commit:
            user.save()
        return user
