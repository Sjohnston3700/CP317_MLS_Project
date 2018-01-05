import os, logging, logging.config, json
from conf_basic import app_config
from app import app
from views   import *
from actions import *

#Setup logging - Should be moved to a separate function ultimately
logger = logging.getLogger(__name__)
with open('logging_config.json', 'rt') as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 8080))
    app.run(host=app_config['our_host'], port=app_config['port'], debug=app_config["debug"])
