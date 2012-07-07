from django.forms import ModelForm
from django import forms
from djangotoolbox.fields import ListField
from votuition.models import Vote



class VoteForm(forms.Form):
    email = forms.EmailField(initial='a@b.com')
    subject = forms.CharField(max_length=100, label='What is the vote for',help_text='100 characters max.')
    vote = forms.IntegerField(label='numeric')
    categories = forms.CharField(max_length=250,required=False,label='comma separated categories')

#class VoteModelForm(ModelForm):
#    class Meta:
#        model = Vote