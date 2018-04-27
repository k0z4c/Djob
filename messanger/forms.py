from django import forms 

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Submit
)

from .models import Message, Conversation

from friendship.models import Friendship 
from django.utils import timezone

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.user = user 
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['recipient'].queryset = Friendship.objects.get_friends(user)

    class Meta:
        model = Message
        fields = ['message',]

    def save(self, commit=True):
        self.instance.sender = self.user
        return super(MessageForm, self).save(commit)
