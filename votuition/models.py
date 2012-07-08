from django.db import models
from djangotoolbox.fields import ListField

class Vote(models.Model):
    

    user_id = models.CharField(max_length=250)
    org_id = models.CharField(max_length=250, blank=True)
    campaign_id = models.CharField(max_length=250, blank=True)
    vote_subject = models.CharField(max_length=250)
    vote_value = models.IntegerField()
    categories = ListField()
    

    
    
    # ...
    def __unicode__(self):
#        strRet = "[%s], [%s], [%s], [%s], [%s], [%s], [%s], [%s]" % (self.pipeline_id, self.step_name, self.step_description, self.type, 
#                                                                     self.input_filename, self.pull_log, self.stage_log, self.load_log)
        strRet = "TBD"
        return strRet   
