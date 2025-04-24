from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginForm(forms.Form):
    def __init__(self,*args, **kwargs): 
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control"})

    username=forms.CharField(max_length=60)
    password=forms.CharField(max_length=14,widget=forms.PasswordInput)



class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
