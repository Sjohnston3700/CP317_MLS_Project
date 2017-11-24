from flask import Flask, redirect, request
from conf_basic import app_config
import requests
import d2lvalence.auth as d2lauth


app = Flask(__name__)
app.config["app_context"] = d2lauth.fashion_app_context(app_id=app_config['app_id'], app_key=app_config['app_key'])
app_url = '{0}://{1}:{2}{3}'.format(app_config['scheme'], app_config['host'], app_config['port'], app_config["route"])
console_url = '{0}://{1}:{2}/console'.format(app_config['scheme'], app_config['host'], app_config['port'])

@app.route("/")
def start():
#    if 'user_context' not in app.config:
#        aurl = app.config["app_context"].create_url_for_authentication(host=app_config['lms_host'], client_app_url=app_url, encrypt_request=app_config['encrypt_requests'])
#        return redirect(aurl)
#    else:
#        return redirect( console_url )
#    return
#    aurl = app.config["app_context"].create_url_for_authentication(host=app_config['lms_host'], client_app_url=app_url, encrypt_request=app_config['encrypt_requests'])
    aurl = app.config["app_context"].create_url_for_authentication(app_config["lms_host"], app_url)
    return redirect(aurl)

@app.route(app_config["route"])
def auth_token_handler():
    uc = app.config["app_context"].create_user_context( result_uri=request.url, host=app_config['lms_host'], encrypt_requests=app_config['encrypt_requests'])

    # store the context's props, so we can rebuild it from these props later
    #app.config['user_context'] = uc.get_context_properties()
    app.config['user_context'] = uc

    return redirect( console_url )


if __name__ == "__main__":
    app.run(port=8080,debug=True)
