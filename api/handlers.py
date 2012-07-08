

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cgi
import jsonpickle
import simplejson
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
    # constants for query params
    
    
    # dictionary for returning JSON results
    ret_dict = dict()
    str_json = ""
    
    logger.debug("parsing qeury string params...") 
    if ( len(request.POST) > 0 ):
        str_json = request.POST.items()
        str_pickle = cgi.escape(jsonpickle.encode(str_json))
        logger.debug("POST len: [%s],  JSON: [%s]" % (len(request.POST), str_json))
        for key, value in request.POST.items():
            dict_json = key
            pydict = simplejson.loads(dict_json)
    else:
        error_msg = "ERROR request method: [%s] but only POST allowed" % (request.method)
        return __http_error_response__(error_msg)
        

    # populate db model
    vote_record = Vote()
    try:
        vote_record.user_id = pydict['user_id']
        vote_record.org_id = pydict['org_id']
        vote_record.campaign_id = pydict['campaign_id']
        vote_record.metric = pydict['metric']
        vote_record.value = pydict['value']
        vote_record.categories = pydict['categories']
    except Exception, e:
        error_msg = "Error while populating record with json data[%s], error: [%s]" % (str_json, e)
        return __http_error_response__(error_msg)
        




        #logger.debug("pydict dict: [%s], type: [%s]" % (pydict, type(pydict)))
            
    
    # convert start date to date
    dt_start_datetime = None
    try: 
        dt_start_datetime = datetime.strptime(dt_start_str, "%Y-%m-%d")
    except Exception, e:
        error_msg = "Error while converting [%s] [%s] to datetime, error: [%s]" % (QRY_DATE_START, dt_start_str, e)
        return __http_error_response__(error_msg)
    
    # convert end date to date
    dt_end_datetime = None
    try: 
        dt_end_datetime = datetime.strptime(dt_end_str, "%Y-%m-%d")
    except Exception, e:
        error_msg = "Error while converting [%s] [%s] to datetime, error: [%s]" % (QRY_DATE_START, dt_end_str, e)
        return __http_error_response__(error_msg)

    
    # work out end date
#    try:
#        period_int = int(period_str)
#    except Exception, e:
#        error_msg = "Error while converting [%s] [%s] to datetime, error: [%s]" % (QRY_PERIOD, period_str, e)
#        return __http_error_response__(error_msg)
    
    
    #dt_end_datetime = dt_start_datetime - timedelta(days=period_int)
    # and convert both datetimes to dates - swapping them around at the same time
    dt_end = dt_end_datetime.date()
    dt_start = dt_start_datetime.date()
#    dt_end = dt_start_datetime.date()
#    dt_start = dt_end_datetime.date()
    logger.debug("%s time period (both inclusive): start: [%s], end: [%s]" % (LOG_INDENT, dt_start, dt_end) ) 
    
    # we can process / pass rest of query params now
    # get data from db
    logger.debug("attempting to retrieve data from database:  start: [%s], end: [%s], query: [%s]" % (dt_start, dt_end, query_dict.urlencode()) ) 
    try: 
        ret_dict = Metrics.get_ui_status_data_for_date_range(dt_start=dt_start, dt_end=dt_end, query_dict=query_dict)
    except Exception, e:
        error_msg = "Error while trying to retrieve trustbaord db data, caught in method: [%s], error: [%s]" % (inspect.stack()[0][3], e)
        return __http_error_response__(error_msg)
    
    
    ret_json = simplejson.dumps(ret_dict)
    response = HttpResponse(status=200, content_type="application/json")
    response.write(ret_json)
    return response


@csrf_exempt
def trustbord_query_metrics(request, version):
    """ get JSON for trusboard UI (metrics)
    """
    logger.debug("%s starting..." %  (inspect.stack()[0][3])) 
    # constants for query params
    QRY_DATE_START = "start_date"
    QRY_DATE_END = "end_date"
    QRY_METRIC = "metric"            # metric="x" where "x" is value of "metric_name" column, all values for "metric_value" will be SUM-ed
    
    # dictionary for returning JSON results
    ret_dict = dict()
    ret_dict["test_key"] = "test_value"
    
    logger.debug("parsing qeury string params...") 
    query_dict = dict()
    if request.method == 'GET':
        query_dict = request.GET
    elif request.method == 'POST':
        query_dict = request.POST
    else:
        error_msg = "Invalid request method: [%s]" % request.method
        return __http_error_response__(error_msg)
    logger.debug("%s %s: number of query string args found: [%s]" % (LOG_INDENT, request.method, len(query_dict)) )
    
    
    # work out date range - start date first
    logger.debug("working out time period...") 
    dt_start_str = query_dict.get(QRY_DATE_START, None)
    dt_end_str = query_dict.get(QRY_DATE_END, None)
    metric = query_dict.get(QRY_METRIC, None)
    
    # validate sum is specified
    if not metric or len(metric.strip(" ")) < 1:
        error_msg = "[%s] query argument is mandatory and must not be empty" % QRY_METRIC
        return __http_error_response__(error_msg)
    
    if ( not dt_start_str or len(dt_start_str) < 10 ):
        logger.warning("%s Supplied [%s] is invalid date: [%s], defaulting to today" % (LOG_INDENT, QRY_DATE_START, dt_start_str) )
        today_date = date.today()
        dt_start_str = today_date.strftime("%Y-%m-%d")
    if ( not dt_end_str or len(dt_end_str) < 10 ):
        logger.warning("%s Supplied [%s] is invalid date: [%s], defaulting to today" % (LOG_INDENT, QRY_DATE_END, dt_end_str) )
        today_date = date.today()
        dt_end_str = today_date.strftime("%Y-%m-%d")
    
    # convert start date to date
    dt_start_datetime = None
    try: 
        dt_start_datetime = datetime.strptime(dt_start_str, "%Y-%m-%d")
    except Exception, e:
        error_msg = "Error while converting [%s] [%s] to datetime, error: [%s]" % (QRY_DATE_START, dt_start_str, e)
        return __http_error_response__(error_msg)
    
    # convert end date to date
    dt_end_datetime = None
    try: 
        dt_end_datetime = datetime.strptime(dt_end_str, "%Y-%m-%d")
    except Exception, e:
        error_msg = "Error while converting [%s] [%s] to datetime, error: [%s]" % (QRY_DATE_START, dt_end_str, e)
        return __http_error_response__(error_msg)

    
    # and convert both datetimes to dates
    dt_end = dt_end_datetime.date()
    dt_start = dt_start_datetime.date()
    logger.debug("%s time period (both inclusive): start: [%s], end: [%s]" % (LOG_INDENT, dt_start, dt_end) ) 
    
    # we can process / pass rest of query params now
    # get data from db
    logger.debug("attempting to retrieve data from database:  start: [%s], end: [%s], query: [%s]" % (dt_start, dt_end, query_dict.urlencode()) ) 
    try: 
        ret_dict = Metrics.get_ui_metric_data_for_date_range(dt_start=dt_start, dt_end=dt_end, query_dict=query_dict)
    except Exception, e:
        error_msg = "Error while trying to retrieve trustbaord db data, caught in method: [%s], error: [%s]" % (inspect.stack()[0][3], e)
        return __http_error_response__(error_msg)
    
    
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
def test(request, version):
    logger.debug("ASZ register")
    
    if ( len(request.POST) > 0 ):
        str_json = request.POST.items()
        str_pickle = cgi.escape(jsonpickle.encode(str_json))
        logger.debug("POST len: [%s],  JSON: [%s]" % (len(request.POST), str_json))
        for key, value in request.POST.items():
            dict_json = key
            pydict = simplejson.loads(dict_json)

        logger.debug("pydict dict: [%s], type: [%s]" % (pydict, type(pydict)))
        #logger.debug("email: [%s]" % pydict["email"])
        for key, value in pydict.items():
            print key + " <--> " + value
        
#        dec = simplejson.JSONDecoder()
#        dec.decode(str_json)
#        for key, value in pydict.items():
#            print key + " <--> " + value
#        
#        logger.debug("user: [%s]" % pydict['user'])
#        for key, value in dict_json.iteritems():
#            print key, value
        
        
        #json = simplejson.loads(str_json)
#    name = request.get('name', default_value=None)
#    description = request.get('description', default_value=None)
#    logger.debug("[%s] [%s]" % (name, description))
    
    return HttpResponse("You're at the register.")


@csrf_exempt
def tracking_jenkins(request, version):
    """ receive Jenkins runtime properties
    """
    logger.debug("tracking_jenkins starting...")
    
    if ( len(request.POST) > 0 ):
        str_json = request.POST.items()
        str_pickle = cgi.escape(jsonpickle.encode(str_json))
        logger.debug("POST len: [%s],  JSON: [%s]" % (len(request.POST), str_json))
        for key, value in request.POST.items():
            dict_json = key
            pydict = simplejson.loads(dict_json)

        #logger.debug("pydict dict: [%s], type: [%s]" % (pydict, type(pydict)))
            
        # PoC - most likely this code will end up somewhere else
        logger.debug("preparing to save PipelineJenkinsJob record...")
        jenk_job_info = PipelineJenkinsJob()
        
        # validate and populate db model
        jenk_job_info.env_id = pydict['env_id']
        jenk_job_info.pipeline_id = pydict['pipeline_id']
        jenk_job_info.build_jobName = pydict['build_jobName']
        
        # build number
        try:
            build_number = long(pydict['build_number'])
        except Exception, e:
            error_msg = "Error while converting build number [%s] to int, record NOT saved, error: [%s]" % (pydict['build_elapsedTime'], e)
            logger.error(error_msg)
            response = HttpResponse(status=500, content_type="text/plain")
            response.write(error_msg)
            return response
        jenk_job_info.build_number = build_number
        
        jenk_job_info.workflow_stage = pydict['workflow_stage']
        
        # sender's timezone info - we might need it
        tzname = pydict['tzname']
        logger.debug("tzname: [%s]" % tzname)
        utc_offset = pydict['utc_offset']
        logger.debug("utc_offset: [%s]" % utc_offset)
        
        # data
        jenk_job_info.build_result = pydict['build_result']
        jenk_job_info.build_user_id = pydict['build_user_id']
        jenk_job_info.build_host = pydict['build_host']
        jenk_job_info.build_slave = pydict['build_slave']
        
        # build started datetime
        # Potential issue - the timezone part is experimentation at this stage
        # needs tuning - revision on live data
        build_started_string = pydict['build_started']           # format: 2012-06-21T11:09:08
        # http://docs.python.org/release/2.5.2/lib/typesseq-strings.html
        build_started_string = build_started_string +  "%(#)+03d:00" % {"#": utc_offset}  
        try:
            #build_started_date = datetime.strptime(build_started_string, '%Y-%m-%dT%H:%M:%S %Z')
            build_started_date = parser.parse(build_started_string)
        except Exception, e:
            error_msg = "Error while converting build_started_date [%s] to datetime, record NOT saved, error: [%s]" % (pydict['build_elapsedTime'], e)
            logger.error(error_msg)
            response = HttpResponse(status=500, content_type="text/plain")
            response.write(error_msg)
            return response
        jenk_job_info.build_started = build_started_date
        
        # elapsed time (miliseconds)
        try:
            build_elapsedTime = long(pydict['build_elapsedTime'])
        except Exception, e:
            error_msg = "Error while converting elapsed time [%s] to int, record NOT saved, error: [%s]" % (pydict['build_elapsedTime'], e)
            logger.error(error_msg)
            response = HttpResponse(status=500, content_type="text/plain")
            response.write(error_msg)
            return response
        jenk_job_info.build_elapsedTime = build_elapsedTime
        
        # build finished datetime - has to be calculated 
        build_finished_date = None
        try:
            build_finished_date = build_started_date + timedelta(seconds=build_elapsedTime/1000)
        except Exception, e:
            error_msg = "Error while calculating Jenkins finished datetime, build_started_date: [%s], build_elapsedTime: [%s], record NOT saved, error: [%s]" % (build_started_date, build_elapsedTime, e)
            logger.error(error_msg)
            response = HttpResponse(status=500, content_type="text/plain")
            response.write(error_msg)
            return response
        
        jenk_job_info.build_finished = build_finished_date
        logger.debug("build_started_date: [%s], build_elapsedTime: [%s], build_finished_date: [%s]" %
                      (jenk_job_info.build_started, jenk_job_info.build_elapsedTime, jenk_job_info.build_finished) )


        jenk_job_info.comments = pydict['comments']
        
        # use lookup table to get all dts for this particular job
        jenkins_job_id = "%s.%s" % (jenk_job_info.build_jobName, jenk_job_info.build_number)
        logger.debug("Looking up [%s] for dts..." % jenkins_job_id)
        dt_list = JenkinsDtLookup.objects.filter(jenkins_job_id=jenkins_job_id)
        if len(dt_list) < 1:
            logger.warning("lookup didn't return any results")
            #  save single record to database
            try:
                jenk_job_info.save()
            except Exception, e:
                error_msg = "Error while trying to save PipelineJenkinsJob record: [%s]" % e
                logger.error(error_msg)
                response = HttpResponse(status=500, content_type="text/plain")
                response.write(error_msg)
                return response
        else:
            logger.info("dt entries found: [%s]" % len(dt_list))
            # save one row per dt
            for lookup_row in dt_list:
                jenk_job_info.id = None
                jenk_job_info.pk = None
                jenk_job_info.dt = lookup_row.dt
                logger.info("saving record for dt: [%s]" % jenk_job_info.dt)      
                try:
                    jenk_job_info.save()
                    logger.info("saving record for dt: [%s] DONE" % jenk_job_info.dt)   
                except Exception, e:
                    error_msg = "Error while trying to save PipelineJenkinsJob record: [%s]" % e
                    logger.error(error_msg)
                    response = HttpResponse(status=500, content_type="text/plain")
                    response.write(error_msg)
                    return response
            logger.info("All records saved")
        
        
    
    return HttpResponse("OK")


@csrf_exempt
def tracking_metrics(request, version):
    """ receive tracking params from Jenkins - this effectively replaces tracking_jenkins method
    but is NOT READY YET - client needs to change as well since composite field requires 11 fields,
    most of which are currently not available in Jenkins
    """
    logger.debug("tracking_metrics starting (DISABLED)...")
    
    # default values where applicable
    DEFAULT_NA = ""
    DEFAULT_CHANNEL = "ALL"
    DEFAULT_ERROR_VALUE = "ERRVAL"
    
    # env / platform lookup: our naming conventions
    # don't have such graniality so we have to work out those two
    # based on ENV_ID - unfortunately that raises a question whether we should
    # derive all  (owner, org, env_string, region) from this...
    dict_envs = {"analytics.fox.prod-cdh.us-east-1": {"env": "PROD", "platform": "CDH"}}
    
    if ( len(request.POST) > 0 ):
        str_json = request.POST.items()
        str_pickle = cgi.escape(jsonpickle.encode(str_json))
        logger.debug("POST len: [%s],  JSON: [%s]" % (len(request.POST), str_json))
        for key, value in request.POST.items():
            dict_json = key
            pydict = simplejson.loads(dict_json)

        #logger.debug("pydict dict: [%s], type: [%s]" % (pydict, type(pydict)))
            
        # PoC - most likely this code will end up somewhere else
        logger.debug("preparing to save Metrics record...")
        metrics = Metrics()
        
        # validate and populate db model
        # break env id into appriopriate parts (ex: analytics.fox.prod-cdh.us-east-1)
        env_id = pydict['env_id']
        (owner, org, env_string, region) = ("", "", "", "")
        try:
            (owner, org, env_string, region) = env_id.split(".")
        except Exception, e:
            error_msg = "Error while trying to break env id into 4 components: [%s]" % (env_id, e)
            logger.error(error_msg)
            response = HttpResponse(status=500, content_type="text/plain")
            response.write(error_msg)
            return response

        metrics.region = region
        metrics.organisation_unit = org.upper()
        metrics.business_unit = DEFAULT_NA
        metrics.product = DEFAULT_NA
        metrics.pipeline_id = pydict['pipeline_id']
        metrics.channel = DEFAULT_CHANNEL
        metrics.env_id = env_id
        
        # look up / get env and platform from env_id
        env = DEFAULT_ERROR_VALUE
        platform = DEFAULT_ERROR_VALUE
        try:
            env = dict_envs[env_id]["env"]
            platform = dict_envs[env_id]["platform"]
        except Exception, e:
            # report error but carry on...
            error_msg = "Error while trying to get env and platform from env_id: [%s], is env_id defined in hardcoded lookup here?, error: [%s]" % (env_id, e)
            logger.error(error_msg)
        metrics.env = env
        metrics.platform = platform
        metrics.workflow_stage = pydict['workflow_stage']
        metrics.metric_name = "jenkins_status"
        metrics.metric_value = pydict['build_result']
        metrics.build_jobName = pydict['build_jobName']
        # build number
        try:
            build_number = long(pydict['build_number'])
        except Exception, e:
            error_msg = "Error while converting build number [%s] to int, record NOT saved, error: [%s]" % (pydict['build_elapsedTime'], e)
            logger.error(error_msg)
            response = HttpResponse(status=500, content_type="text/plain")
            response.write(error_msg)
            return response
        metrics.build_number = build_number
        metrics.comments = pydict['comments']
        
        # use lookup table to get all dts for this particular job
        jenkins_job_id = "%s.%s" % (metrics.build_jobName, metrics.build_number)
        logger.debug("Looking up [%s] for dts..." % jenkins_job_id)
        dt_list = JenkinsDtLookup.objects.filter(jenkins_job_id=jenkins_job_id)
        if len(dt_list) < 1:
            logger.warning("lookup didn't return any results")
            #  save single record to database
            try:
                metrics.save()
            except Exception, e:
                error_msg = "Error while trying to save Metrics record: [%s]" % e
                logger.error(error_msg)
                response = HttpResponse(status=500, content_type="text/plain")
                response.write(error_msg)
                return response
        else:
            logger.info("dt entries found: [%s]" % len(dt_list))
            # save one row per dt
            for lookup_row in dt_list:
                metrics.id = None
                metrics.pk = None
                metrics.dt = lookup_row.dt
                logger.info("saving record for dt: [%s]" % metrics.dt)      
                try:
                    metrics.save()
                    logger.info("saving record for dt: [%s] DONE" % metrics.dt)   
                except Exception, e:
                    error_msg = "Error while trying to save Metrics record: [%s]" % e
                    logger.error(error_msg)
                    response = HttpResponse(status=500, content_type="text/plain")
                    response.write(error_msg)
                    return response
            logger.info("All records saved")
        
        
    
    return HttpResponse("OK")


@csrf_exempt
def tracking_data(request, version):
    """ receive Jenkins runtime properties
    """
    logger.debug("tracking_data starting...")
    
    if ( len(request.POST) > 0 ):
        str_json = request.POST.items()
        str_pickle = cgi.escape(jsonpickle.encode(str_json))
        logger.debug("POST len: [%s],  JSON: [%s]" % (len(request.POST), str_json))
        for key, value in request.POST.items():
            dict_json = key
            pydict = simplejson.loads(dict_json)

        # process data
        if pydict['record_type'] == "JENKINS_DT_LOOKUP":
            logger.debug("recod type: [%s]" % pydict['record_type'])
            line = pydict['line']
            if not line or len(line) < 1:
                error_msg = "sent line empty: [%s]" % line
                logger.error(error_msg)
                response = HttpResponse(status=500, content_type="text/plain")
                response.write(error_msg)
                return response
            # split line into jenkins_id and dt (last param)
            (jenkins_job_id, separator, dt) = line.rpartition('.')
            logger.debug("jenkins_job_id: [%s], dt: [%s]" % (jenkins_job_id, dt) )   
            lookup_row = JenkinsDtLookup()
            lookup_row.jenkins_job_id = jenkins_job_id
            lookup_row.dt = dt
            
            # and save
            try:
                lookup_row.save()
            except Exception, e:
                error_msg = "Error while trying to save JenkinsDtLookup record: [%s]" % e
                logger.error(error_msg)
                response = HttpResponse(status=500, content_type="text/plain")
                response.write(error_msg)
                return response           
                
            
        # PoC - most likely this code will end up somewhere else
        #logger.debug("preparing to save PipelineJenkinsJob record...")
        
        
    return HttpResponse("OK")


@csrf_exempt
def index(request):
    if request.method == 'POST': 
        post = request.POST 
#        raw = request.raw_post_data 
#        remote_media_id = post.get("video_id", "") 
    else:    
        return HttpResponse("Hello, world. You're at the index.")

