import sys
from datetime import datetime
import logging
import os
import platform
from typing import Optional
import filesystem as fs

logger: Optional[logging.Logger] = None

def is_debug():
    return os.environ["DEBUG"] == "1"

def _setup_logger():
    global logger
    logger = logging.getLogger("pzcurate")

    log_path = os.path.join(fs.get_appdata_path(), "log")
    os.makedirs(log_path, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s %(levelname)s (%(module)s:%(lineno)s): %(message)s")

    fh = logging.FileHandler(filename=os.path.join(log_path, datetime.now().strftime("log_%Y_%m_%d.txt")))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)

    if len(logger.handlers) <= 0:
        logger.addHandler(fh)
        logger.addHandler(ch)

        logger.info("PZCurate started!")

# setup actions:
_setup_logger()
