import re
# note: l = list(session.query(TagAss).filter(TagAss.value>16))
# and:  l = list(session.query(TagAss).filter(cast(TagAss.value, Integer)>16)) # https://stackoverflow.com/a/12643842/5013267
# and: l = list(session.query(TagAss).filter(and_(cast(TagAss.value, Integer).like("pog"), TagAss.def_id==1)))


def get_query(exp: str):
    """
    Convert a PZCurate expression into SQLAlchemy query
    """
    for sub_query in exp.split(' '):
        print(sub_query)

get_query("art  time<=yesterday genre=roc% rating>3")