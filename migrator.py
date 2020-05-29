import db

def migrate(session):
    current_version = session.query(db.InternalMeta.version)[0].version
    if current_version != db.VERSION:
        print("Existing database schema {}")
