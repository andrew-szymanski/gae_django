from django.db import models
from djangotoolbox.fields import ListField

class Metrics(models.Model):
    """Generic metrics table
    """
    user_id = models.CharField(max_length=250)
    org_id = models.CharField(max_length=250, blank=True)
    campaign_id = models.CharField(max_length=250, blank=True)
    metric = models.CharField(max_length=250)
    value = models.IntegerField()
    categories = ListField()

    def __unicode__(self):
#        strRet = "[%s], [%s], [%s], [%s], [%s], [%s], [%s], [%s]" % (self.pipeline_id, self.step_name, self.step_description, self.type, 
#                                                                     self.input_filename, self.pull_log, self.stage_log, self.load_log)
        strRet = "TBD"
        return strRet   
    

class Vote(models.Model):
    """ Vote specific table for jim
    """
    ip = models.CharField(max_length=250)
    user_id = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    vote = models.IntegerField()
    categories = ListField()    
    last_updated = models.DateTimeField(auto_now=True, 
                                        verbose_name="last update datetime", 
                                        help_text="datetime this record was last updated")
    
    # ...
    def __unicode__(self):
#        strRet = "[%s], [%s], [%s], [%s], [%s], [%s], [%s], [%s]" % (self.pipeline_id, self.step_name, self.step_description, self.type, 
#                                                                     self.input_filename, self.pull_log, self.stage_log, self.load_log)
        strRet = "[%s], [%s], [%s], [%s]" % (self.user_id, 
                                             self.subject, 
                                             self.vote, 
                                             self.categories)
        return strRet   
