from django import forms


class UnsubscribeForm(forms.Form):
    check = forms.BooleanField(label='Check to unsubscribe')
