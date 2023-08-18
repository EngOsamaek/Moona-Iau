from django import forms

from Moona.models import Company, Product
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)




class CompanyForm(forms.Form):
    logo = forms.ImageField()
    company_name = forms.CharField(max_length=30)
    type = forms.CharField(max_length=20)
    tax_no = forms.IntegerField()
    is_activated = forms.BooleanField(required=False)
    is_blocked = forms.BooleanField(required=False)
