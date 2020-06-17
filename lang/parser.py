from lark import Lark
# note: l = list(session.query(TagAss).filter(TagAss.value>16))
# and:  l = list(session.query(TagAss).filter(cast(TagAss.value, Integer)>16)) # https://stackoverflow.com/a/12643842/5013267
# and: l = list(session.query(TagAss).filter(and_(cast(TagAss.value, Integer).like("pog"), TagAss.def_id==1)))

with open("grammar.lark", "r") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")

def get_query(exp: str):
    """
    Convert a PZCurate expression into SQLAlchemy query
    """
    pass  # TODO