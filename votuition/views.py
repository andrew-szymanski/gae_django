__author__ = "Andrew Szymanski"
__version__ = "0.1.0"

""" Forms playground
"""
#from django.views.decorators.http import require_safe
import urllib    
import urllib2
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render,render_to_response, get_object_or_404, redirect
from django.conf import settings
from django.utils import simplejson
from django.http import QueryDict
from django.contrib.sites.models import Site
#import inspect
from types import *
from votuition.forms import VoteForm
from votuition.forms import JsonForm


# Get an instance of a logger
import logging
from django.utils.log import getLogger
logger = getLogger('django')
logger.setLevel(logging.DEBUG)
LOG_INDENT = "   "




def form_response(request):
    #logger.debug("entering [%s]:[%s]" % (__file__, inspect.stack()[0][3]) )
    method_name = "form_response"
    logger.debug("entering [%s]:[%s]" % (__file__, method_name) )
    #logger.debug("entering [%s]:[%s], form=[%s]" % (__file__, method_name, form) )
    template_response = "debug/form_sample_result.html"
    
    host = request.get_host()  # hack - request is made by server so we should get server's url
    logger.debug("host: [%s]" % host)
    api_url = "http://%s/api/v1.0/vote" % host
    
    json_str = ""
    output_lines = list()
    if request.method == 'GET':
        # get json string
        query_dict = request.GET
        json_str = query_dict.get("json", "{}")
        line = "json_str: %s" % json_str
        logger.debug(line) 
        output_lines.append(line) 
        # call API
        line = "preparing to POST to: [%s]" % api_url
        logger.debug(line) 
        output_lines.append(line) 
        #data = simplejson.dumps(values)
        req = urllib2.Request(api_url, json_str, {'Content-Type': 'application/json'})        

        line = "posting data to server..."
        logger.debug(line) 
        output_lines.append(line) 
        return_message = ""
        return_status = True
        try:
            line = "sending request..."
            logger.debug(line) 
            output_lines.append(line) 
            f = urllib2.urlopen(req)
            line = "reading response..."
            logger.debug(line) 
            output_lines.append(line) 
            response = f.read()
            line = "response: [%s]" % response
            logger.debug(line) 
            output_lines.append(line) 
            line = "closing connection..."
            logger.debug(line) 
            output_lines.append(line) 
            f.close()   
        except urllib2.HTTPError, e:
            return_status = False
            return_message = "%s (%s)" % (e.read(), e)
            logger.error(return_message) 
            output_lines.append(return_message) 
        except urllib2.URLError, e:
            return_status = False
            return_message = "%s %s" % (return_message, e)
            logger.error(return_message) 
            output_lines.append(return_message) 
        except Exception, e:
            return_status = False
            return_message = "%s %s" % (return_message, e)
            logger.error(return_message) 
            output_lines.append(return_message) 
            
    
    return render_to_response(template_response, {
                                              'view_type': "lala",
                                              'output_lines': output_lines,
                                              }
                              )
    
def form_json(request):
    #logger.debug("entering [%s]:[%s]" % (__file__, inspect.stack()[0][3]) )
    logger.debug("entering [%s]:form_json" % (__file__) )
    template_form = "debug/form_sample_json.html" 
    template_next = "/debug/form_response" 
    
    logger.debug("template: [%s], request method: [%s]" % (template_form, request.method) )
    show_errors = False
    json_str = "{}"
    if request.method == 'POST': # If the form has been submitted...
        form = JsonForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # convert data to JSON
            json_data = form.cleaned_data['json']
            logger.debug("json_data: [%s]" % json_data)
            # construct query string
            query_dict = QueryDict('json=%s' %  json_data)
            query_string = query_dict.urlencode()
            logger.debug("query_string: [%s]" % query_string)
            #
            full_redirect_url = template_next + "?" + query_string
            logger.debug("full_redirect_url: [%s]" % full_redirect_url)
            return redirect(full_redirect_url )
        else:
            show_errors = True
    else:
        if request.method == 'GET':
            # get json string
            query_dict = request.GET
            json_str = query_dict.get("json", "{}")
            logger.debug("json_str: [%s]" % json_str)
        form = JsonForm({'json': json_str}) # bound form    

        
    
    return render(request, template_form, {
            'form': form,    
            'show_errors': show_errors,
            })
    
#@require_safe
def form_sample(request):
    #logger.debug("entering [%s]:[%s]" % (__file__, inspect.stack()[0][3]) )
    logger.debug("entering [%s]:form_sample" % (__file__) )
    template_form = "debug/form_sample_input.html" 
    template_next = "/debug/form_json" 
    
    logger.debug("template: [%s]" % template_form)
    show_errors = False
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # convert data to JSON
            json_data = form.json()
            logger.debug("json_data: [%s]" % json_data)
            # construct query string
            query_dict = QueryDict('json=%s' %  json_data)
            query_string = query_dict.urlencode()
            logger.debug("query_string: [%s]" % query_string)
            #
            full_redirect_url = template_next + "?" + query_string
            logger.debug("full_redirect_url: [%s]" % full_redirect_url)
            return redirect(full_redirect_url )
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