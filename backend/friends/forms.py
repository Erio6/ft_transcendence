from django import forms

class UserSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Looking for users...',
    }))