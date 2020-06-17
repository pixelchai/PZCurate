import re
from sqlalchemy.sql.expression import and_, cast
import db

# note: l = list(session.query(TagAss).filter(TagAss.value>16))
# and:  l = list(session.query(TagAss).filter(cast(TagAss.value, Integer)>16)) # https://stackoverflow.com/a/12643842/5013267
# and: l = list(session.query(TagAss).filter(and_(cast(TagAss.value, Integer).like("pog"), TagAss.def_id==1)))

_LEX_REGEX = r"(\w+)\s*" \
             r"(?:(" \
                 r">=|<=|=|!=|>|<" \
             r")\s*(" \
                 r"[\w%]+|" \
                 "\\\"(?:\\\\.|[^\"\\\\\\n])*\\\"+" \
             r"))?"

class Querier:
    def __init__(self, session, library_id):
        self.session = session
        self.library_id = library_id

    @staticmethod
    def lex(exp: str):
        """
        Perform lexical analysis on a PZCurate expression
        """
        for match in re.finditer(_LEX_REGEX, exp):
            yield match.groups()

    def _get_id_clause(self, lhs: str):
        for tag_def in self.session.query(db.TagDef).filter(and_(db.TagDef.library_id == self.library_id,
                                                                 db.TagDef.name == lhs)):
            return db.TagAss.def_id == tag_def.id  # return the first one

    def _get_filter(self, lhs, operator, rhs):
        id_clause = self._get_id_clause(lhs)

        if operator is None and rhs is None:
            return id_clause

    def query(self, exp: str):
        """
        Convert a PZCurate expression into SQLAlchemy query
        """
        base_query = self.session.query(db.TagAss)
        for sub_exp in self.lex(exp):
            base_query = base_query.filter(self._get_filter(*sub_exp))
        return base_query

# query("art  time<=yesterday genre=roc% rating>3")
# q = Querier(None, None)
