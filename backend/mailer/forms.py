from django import forms


class ConfirmUnsubscribeForm(forms.Form):
    confirm = forms.BooleanField()
