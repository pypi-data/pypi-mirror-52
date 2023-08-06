from django import forms


class UnsubscribeForm(forms.Form):
    check = forms.BooleanField(label='Do you want to unsubscribe?')
