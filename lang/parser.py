import re
from sqlalchemy.sql.expression import and_, cast
import db

# note: l = list(session.query(TagAss).filter(TagAss.value>16))
# and:  l = list(session.query(TagAss).filter(cast(TagAss.value, Integer)>16)) # https://stackoverflow.com/a/12643842/5013267
# and: l = list(session.query(TagAss).filter(and_(cast(TagAss.value, Integer).like("pog"), TagAss.def_id==1)))

__REGEX = r"(\w+)\s*" \
          r"(?:(" \
              r">=|<=|=|!=|>|<" \
          r")\s*(" \
              r"[\w%]+|" \
              "\\\"(?:\\\\.|[^\"\\\\\\n])*\\\"+" \
          r"))?"

def __lex(exp: str):
    """
    Perform lexical analysis on a PZCurate expression
    """
    for match in re.finditer(__REGEX, exp):
        yield match.groups()

# class Querier:
#     def __init__(self):
#         pass

def __get_id_clause(session, library_id: int, lhs: str):
    for tag_def in session.query(db.TagDef).filter(and_(db.TagDef.library_id == library_id,
                                                        db.TagDef.name == lhs)):
        return db.TagAss.def_id == tag_def.id  # return the first one

def __add_filter(base_query, lhs, operator, rhs):
    return and_(__get_id_clause(library_id))

def query(session, library_id: int, exp: str):
    """
    Convert a PZCurate expression into SQLAlchemy query
    """
    base_query = session.query(db.TagAss)
    for sub_exp in __lex(exp):
        __add_filter(base_query, library_id, *sub_exp)

# query("art  time<=yesterday genre=roc% rating>3")
