from django import forms

from book.models import Book

class MakeOrderForm(forms.Form):
    plated_end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type":"datetime-local", "class":"form-control"}))


class UpdateOrderForm(forms.Form):
    plated_end_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"type":"datetime-local", "class":"form-control"}))
    end_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"type":"datetime-local", "class":"form-control"}))


