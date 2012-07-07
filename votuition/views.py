__author__ = "Andrew Szymanski"
__version__ = "0.1.0"

""" Forms playground
"""
#from django.views.decorators.http import require_safe
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render,render_to_response, get_object_or_404
from django.conf import settings
import inspect
from types import *
from votuition.forms import VoteForm


# Get an instance of a logger
import logging
from django.utils.log import getLogger
logger = getLogger('django')
logger.setLevel(logging.DEBUG)
LOG_INDENT = "   "



#@require_safe
def form_sample(request):
    #logger.debug("entering [%s]:[%s]" % (__file__, inspect.stack()[0][3]) )
    logger.debug("entering [%s]:form_sample" % (__file__) )
    template_file = "debug/form_sample.html" 
    logger.debug("template: [%s]" % template_file)
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/debug/form_sample_result.html') # Redirect after POST
    else:
        form = VoteForm() # An unbound form    
    
    return render(request, template_file, {
            'form': form,    
            })
    
#    return render_to_response(template_file, {
#                                              'view_type': "lala",
#                                              }
#                              )