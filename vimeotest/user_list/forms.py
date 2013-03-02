from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(max_length=400, required=False)
    flter = forms.ChoiceField(choices=((0, 'All'), (1, 'Paying'), (2, 'Uploaded'), (3, 'Staff Pick')), required=False)
