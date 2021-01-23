from django import forms

from .models import CustomUser, ROLE_CHOICES


STATUS_CHOICES = (
    (True, 'Active'),
    (False, 'Disabled'),
)

class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'middle_name',)

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()    
        return user


class CustomUserUpdateForm(forms.Form):
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    is_active = forms.ChoiceField(required=False, choices=STATUS_CHOICES)
    role = forms.ChoiceField(required=False, choices=ROLE_CHOICES)


class CustomUserSearchForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
