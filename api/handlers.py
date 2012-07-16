

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cgi
import jsonpickle
from django.utils import simplejson
from votuition.models import Vote
#import inspect

# Get an instance of a logger
import logging
from django.utils.log import getLogger
logger = getLogger('django')
logger.setLevel(logging.DEBUG)
LOG_INDENT = "   "

@csrf_exempt
def vote(request, version):
    """ get JSON for vote
    """
    method_name = "vote"
    logger.debug("%s starting..." %  (method_name))
    logger.debug("is_secure: [%s]" % request.is_secure())
    if not request.is_secure():
        error_msg = "ERROR: only https:// protocol allowed"
        return __http_error_response__(error_msg)

    # constants for query params
    ip_address = ""
    try:
        ip_address = request.META['REMOTE_ADDR']
    except Exception, e:
        pass
    logger.debug("IP: [%s]" % ip_address)
    
    # dictionary for returning JSON results
    ret_dict = dict()
    ret_dict['status'] = "OK"
    str_json = ""
    
    logger.debug("parsing qeury string params...") 
    if request.method == 'POST':
#        str_json = request.POST.items()
#        str_pickle = cgi.escape(jsonpickle.encode(str_json))
        logger.debug("POST items: [%s]" % (len(request.POST)))
        if len(request.POST) != 1:
            logger.warning("request.POST items not 1 but [%s]" % len(request.POST))
        for key, value in request.POST.items():
            str_json = key
            logger.debug("%s converting JSON string [%s] to dictionary..." % (LOG_INDENT, str_json))
            try:
                pydict = simplejson.loads(str_json)
            except Exception, e:
                error_msg = "ERROR trying to convert JSON string to dictionary, most likely invalid JSON: [%s]" % (str_json)
                return __http_error_response__(error_msg)
    else:
        error_msg = "ERROR request method: [%s] but only POST allowed" % (request.method)
        return __http_error_response__(error_msg)
        

    # populate db model
    vote_record = Vote()
    vote_record.ip = ip_address
    
    # categories are not manadatory
    try:
        vote_record.categories = pydict['categories']
    except Exception, e:
        error_msg = "(%s): Error while trying to get categories from json data[%s], error: [%s]" % (method_name, str_json, e)
        logger.warning(error_msg)
        logger.warning("Setting categories to empty list..")
        vote_record.categories = list()
        vote_record.categories.append(unicode(""))

    # mandatory fields - don't save if any missing / invalid    
    try:
        vote_record.user_id = pydict['user_id']
        vote_record.subject = pydict['subject']
        vote_record.vote = pydict['vote']
    except Exception, e:
        error_msg = "(%s): Error while populating record with json data[%s], error: [%s]" % (method_name, str_json, e)
        return __http_error_response__(error_msg)



    
    logger.debug("trying to save datastore record...")
    try:
        vote_record.save()
    except Exception, e:
        error_msg = "(%s): Error while trying to save Vote record with json data[%s], error: [%s]" % (method_name, str_json, e)
        return __http_error_response__(error_msg)
    logger.debug("trying to save datastore record DONE")
        
    ret_json = simplejson.dumps(ret_dict)
    response = HttpResponse(status=200, content_type="application/json")
    response.write(ret_json)
    return response



    
def __http_error_response__(error_msg, type="json"):
    # dictionary for returning error info in json
    err_dictionary = dict()
    logger.error(error_msg)
    response = HttpResponse(status=500, content_type="application/json")
    err_dictionary["error_msg"] = error_msg
    ret_json_error = simplejson.dumps(err_dictionary)
    response.write(ret_json_error)
    return response
    

    





@csrf_exempt
def index(request):
    if request.method == 'POST': 
        post = request.POST 
#        raw = request.raw_post_data 
#        remote_media_id = post.get("video_id", "") 
    else:    
        return HttpResponse("Hello, world. You're at the index.")

