from conf_basic import app_config as app_creds
import pickle
import d2lvalence.auth as d2lauth


ac = d2lauth.fashion_app_context(app_id=app_creds['app_id'], app_key=app_creds['app_key'])


with open('user_data','rb') as f:
    redirect_url = pickle.load(f)
    
uc = ac.create_user_context(result_uri=redirect_url, host=app_creds['lms_host'], encrypt_requests=True)
