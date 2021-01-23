from django import forms
from .models import Book
from author.models import Author


class AddBookForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class":"form-control"})
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class":"form-control"})
    )

    count = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    authors = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class":"form-control"}
        )
    )


class UpdateBookForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class":"form-control"})
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class":"form-control"})
    )

    count = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={"class":"form-control"})
    )

    authors = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class":"form-control"}
        )
    )