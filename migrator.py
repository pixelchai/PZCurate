import os

import db

def migrate(session):
    try:
        current_version = session.query(db.InternalMeta.version)[0].version
    except IndexError:
        print("Fatal error: Database version information is absent!")
        return

    if current_version != db.VERSION:
        print("Outdated database version: existing={}, latest={}. Attempting migration."
              .format(current_version, db.VERSION))
        # TODO
