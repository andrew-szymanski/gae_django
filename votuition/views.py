__author__ = "Andrew Szymanski"
__version__ = "0.1.0"

""" Forms playground
"""
#from django.views.decorators.http import require_safe
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render,render_to_response, get_object_or_404, redirect
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




def form_response(request):
    #logger.debug("entering [%s]:[%s]" % (__file__, inspect.stack()[0][3]) )
    method_name = "form_response"
    form = "aa"
    logger.debug("entering [%s]:[%s], form=[%s]" % (__file__, method_name, form) )
    template_response = "debug/form_sample_result.html"
    return render_to_response(template_response, {
                                              'view_type': "lala",
                                              }
                              )
    

#@require_safe
def form_sample(request):
    #logger.debug("entering [%s]:[%s]" % (__file__, inspect.stack()[0][3]) )
    logger.debug("entering [%s]:form_sample" % (__file__) )
    template_form = "debug/form_sample.html" 
    
    logger.debug("template: [%s]" % template_form)
    show_errors = False
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            return redirect('votuition.views.form_response')
        else:
            show_errors = True

    else:
        form = VoteForm() # An unbound form    
    
    return render(request, template_form, {
            'form': form,    
            'show_errors': show_errors,
            })




    
    
        
#    return render_to_response(template_file, {
#                                              'view_type': "lala",
#                                              }
#                              )