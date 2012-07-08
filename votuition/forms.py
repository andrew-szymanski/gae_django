from django.forms import ModelForm
from django import forms
from djangotoolbox.fields import ListField
from django.utils import simplejson
from votuition.models import Vote



class VoteForm(forms.Form):
    email = forms.EmailField(initial='a@b.com', label='email',max_length=250,help_text='valid email address')
    subject = forms.CharField(max_length=100,initial='culica', label='what for',help_text='what the vote is for')
    vote = forms.IntegerField(label='how much',initial=5, help_text='numeric value')
    categories = forms.CharField(required=False,label='list of categories',help_text='optional, comma separated')
    org_id = forms.CharField(required=False,label='org id',max_length=250,help_text='optional')
    campaign_id = forms.CharField(required=False,label='campaign id',max_length=250,help_text='optional')
    
    def json(self):
        """ Hardcoded at the moment but ideally Model fields should be used instead
        """
        ret_dict = dict()
        ret_dict['user_id'] = self.cleaned_data['email']
        ret_dict['org_id'] = self.cleaned_data['org_id']
        ret_dict['campaign_id'] = self.cleaned_data['campaign_id']
        ret_dict['metric'] = self.cleaned_data['subject']
        ret_dict['value'] = self.cleaned_data['vote']
        ret_dict['categories'] = self.cleaned_data['categories'].split(",")
        
        ret_json = simplejson.dumps(ret_dict)
        return ret_json

class JsonForm(forms.Form):
    json = forms.CharField(max_length=250)

#class VoteModelForm(ModelForm):
#    class Meta:
#        model = Vote