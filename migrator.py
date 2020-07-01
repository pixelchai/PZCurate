import database as db
from utils import logger

def migrate(session):
    try:
        current_version = session.query(db.InternalMeta.version)[0].version
    except IndexError:
        logger.critical("Fatal error: Database version information is absent!")
        return

    if current_version > db.VERSION:
        logger.warning("Error: Invalid database version: existing={}, latest={}."
                       .format(current_version, db.VERSION))
    elif current_version < db.VERSION:
        logger.warning("Outdated database version: existing={}, latest={}. Attempting migration."
                       .format(current_version, db.VERSION))
        # TODO
