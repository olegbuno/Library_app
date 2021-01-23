from django import forms
from .models import Author

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("name", "surname", "patronymic",)
        widgets = { "name" : forms.TextInput(attrs={"class":"form-control"}),
                    "surname" : forms.TextInput(attrs={"class":"form-control"}),
                    "patronymic" : forms.TextInput(attrs={"class":"form-control"})} 

        def __init__(self, *args, **kwargs):
            super(AddAuthorForm, self).__init__(self, *args, **kwargs)


class UpdateAuthorForm(forms.Form):
    name = forms.CharField(required=False ,widget=forms.TextInput(attrs={"class":"form-control", "name":"name"}))
    surname = forms.CharField(required=False ,widget=forms.TextInput(attrs={"class":"form-control", "name":"surname"}))
    patronymic = forms.CharField(required=False ,widget=forms.TextInput(attrs={"class":"form-control", "name":"patronymic"}))