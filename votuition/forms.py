from django.forms import ModelForm
from django import forms
from djangotoolbox.fields import ListField
from votuition.models import Vote



class VoteForm(forms.Form):
    email = forms.EmailField(initial='a@b.com', label='email',max_length=250,help_text='valid email address')
    subject = forms.CharField(max_length=100,initial='culica', label='what for',help_text='what the vote is for')
    vote = forms.IntegerField(label='how much',initial=5, help_text='numeric value')
    categories = forms.CharField(required=False,label='list of categories',help_text='optional, comma separated')
    org_id = forms.CharField(required=False,label='org id',max_length=250,help_text='optional')
    campaign_id = forms.CharField(required=False,label='campaign id',max_length=250,help_text='optional')

#class VoteModelForm(ModelForm):
#    class Meta:
#        model = Vote