
# This configuration file represents the kind of state information that your
# app should store in a separate, more secure, location away from your web-app
# source. This holds especially true for the App ID/Key pair -- this is
# sensitive information, and you should find a way to keep it under tight
# control, restricting access only to those who need to manage the values (system
# administrators, for example).
#
# Here, we just put the config values into a sample dictionary that the web
# framework in basic.py can import.
#
#   app_id --  App ID as provided by D2L -- DON'T HARDCODE INTO YOUR APP
#   app_key -- App Key as provided by D2L -- DON'T HARDCODE INTO YOUR APP
#   our_host   --  host for the web-app (our server. eg localhost or flungabunga.ca)
#   port   --  port number for the web-app (on our server. eg 8080 for localhost testing or '' for normal webhosting)
#   scheme --  protocol to use for user <--> web-app interaction
#   lms_host -- hostname for the back-end LMS
#   lms_port -- port number for the back-end LMS
#   encrypt_requests -- True: use HTTPS when making API calls to the LMS
#   lms_ver -- product component API versions to call
#   verify -- cert verification flag
#   debug -- debug flag
#   route -- the trusted url
#
# USER_ROLES -- list of roles to filter by. [] for don't care
# ALLOWED_EXTENSIONS -- set of allowed file extensions
# UPLOAD_FOLDER -- where do we temporarily store files when uploaded
# SECRET_KEY -- the key used to encrypt the session values. Make this random and unique
# 

app_config = {
               'app_id': '4cCvnIU0scbTxUqmC9jExw',
               'app_key': 'uKmh_y4cfKsRTpiTZuzjLw',
               'our_host': 'localhost',
               'port': 8080,
               'scheme':'http',
               'lms_host': 'wlutest.desire2learn.com',
               'lms_port': '443',
               'encrypt_requests': True,
               'verify' : False,
               'lms_ver': {'lp':'1.20','le':'1.26','ep':'2.5'},
               'debug': True,
               'route':'/index.py?page=token',
               }

USER_ROLES         = ['TA','Instructor']
ALLOWED_EXTENSIONS = set(['txt','csv'])
UPLOAD_FOLDER      = './Uploaded_Files'
SECRET_KEY         = 'NDNiYTUwZGU3ZWJkYTUyZGE5ZTUxOWVj'
