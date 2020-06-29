import re
import sqlalchemy as sqla
from sqlalchemy.sql.expression import and_, cast
import db

# note: l = list(session.query(TagAss).filter(TagAss.value>16))
# and:  l = list(session.query(TagAss).filter(cast(TagAss.value, Integer)>16)) # https://stackoverflow.com/a/12643842/5013267
# and: l = list(session.query(TagAss).filter(and_(cast(TagAss.value, Integer).like("pog"), TagAss.def_id==1)))

_LEX_REGEX = r"(\w+)\s*" \
             r"(?:(" \
                 r">=|<=|=|!=|>|<" \
             r")\s*(" \
                 r"[\w%\.]+|" \
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

    def _get_tag_def(self, lhs: str):
        for tag_def in self.session.query(db.TagDef).filter(and_(db.TagDef.library_id == self.library_id,
                                                                 db.TagDef.name == lhs)):
            return tag_def  # return the first one

    def _get_filter_clauses(self, lhs, operator, rhs):
        tag_def = self._get_tag_def(lhs)
        yield db.TagAss.def_id == tag_def.id

        if rhs is not None and operator is not None:
            clause_lhs = db.TagAss.value

            # cast clause_lhs into correct type (database-side)
            cast_type = {
                db.TagType.INT: sqla.Integer,
                db.TagType.FLOAT: sqla.Float,
                db.TagType.STR: sqla.String
            }.get(tag_def.tag_type)

            if cast_type is not None:
                clause_lhs = cast(clause_lhs, cast_type)

            # operator on clause_lhs
            if operator == "=":
                # 'LIKE' clause if string
                if tag_def.tag_type == db.TagType.STR:
                    yield clause_lhs.like(rhs)
                else:
                    yield clause_lhs == rhs
            elif operator == "!=":
                # 'NOT LIKE' clause if string
                if tag_def.tag_type == db.TagType.STR:
                    yield clause_lhs.notlike(rhs)
                else:
                    yield clause_lhs != rhs
            elif operator == '>=':
                yield clause_lhs >= rhs
            elif operator == '<=':
                yield clause_lhs <= rhs
            elif operator == ">":
                yield clause_lhs > rhs
            elif operator == "<":
                yield clause_lhs < rhs

    def _get_filter(self, sub_exp, prev_query=None):
        clauses = list(self._get_filter_clauses(*sub_exp))

        if prev_query is not None:
            clauses.append(db.Item.id.in_(prev_query))
        else:
            # implies first filter (innermost subquery)
            # so filter by library_id here
            clauses.append(db.Item.library_id == self.library_id)

        return self.session.query(db.Item.id)\
                   .join(db.TagAss, db.Item.id == db.TagAss.item_id)\
                   .filter(and_(*clauses))

    def query(self, exp: str):
        """
        Convert a PZCurate expression into SQLAlchemy query
        """
        query = None
        for sub_exp in self.lex(exp):
            query = self._get_filter(sub_exp, query)

        # return Item objects (not just iterable of Item ids)
        return self.session.query(db.Item)\
                   .filter(db.Item.id.in_(query))
