from django import forms
from .models import RequestInvite


class RequestInvitationKeyForm(forms.Form):
    email = forms.EmailField()

    def save(self):
        inv = RequestInvite(email=self.cleaned_data.get('email'))
        inv.save()
