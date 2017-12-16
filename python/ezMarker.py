import os, sys, requests, traceback
import logging, logging.config

from flask import Flask, redirect, request, render_template, url_for, session, jsonify, json, abort

from conf_basic import app_config

from views   import *
from actions import *

#Setup logging - Should be moved to a separate function ultimately
logger = logging.getLogger(__name__)
with open('logging_config.json', 'rt') as f:
    config = json.load(f)
    logging.config.dictConfig(config)





from app import app



       


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host=app_config['host'], port=port, debug=app_config["debug"])
